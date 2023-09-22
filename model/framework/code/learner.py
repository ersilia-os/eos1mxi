# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks_build/01_learner.ipynb (unless otherwise specified).

__all__ = ['randomize_smiles', 'corpus_augment', 'get_vocabulary', 'update_pair_statistics', 'get_pair_statistics',
           'replace_pair', 'prune_stats', 'learn_SPE']

# Cell

import os
import sys
import inspect
import copy
import io
import warnings
import re
from collections import defaultdict, Counter
from fastprogress.fastprogress import master_bar, progress_bar

from pretokenizer import *

def randomize_smiles(smiles):
    """
    Require `RDKit` library.

    Generate a new SMILES string for the same molecule.

    Perform a randomization of a SMILES string must be RDKit sanitizable.
    """
    import random
    import numpy as np
    from rdkit import Chem

    m = Chem.MolFromSmiles(smiles)
    ans = list(range(m.GetNumAtoms()))
    np.random.shuffle(ans)
    nm = Chem.RenumberAtoms(m,ans)
    return Chem.MolToSmiles(nm, canonical=False, isomericSmiles=True, kekuleSmiles=False)

def corpus_augment(infile, outdir, cycles):
    '''
    infile: line separated SMILES file
    outdir: directory to save the  augmented SMILE file.
        Each round of augmentation will save as a separated file, named as `infile_Ri`.
    cycles: number of rounds for SMILES augmentation
    '''
    if cycles <= 0:
        raise ValueError("Invalid option,  cycle should be larger than 0")

    with open(infile, "r") as ins:
        can_smiles = []
        for line in ins:
            can_smiles.append(line.split('\n')[0])

    fname = os.path.basename(infile).split('.')[0]
    ftype = os.path.basename(infile).split('.')[1]

    mb = master_bar(range(cycles))
    for i in mb:
        with open(f'{outdir}/{fname}_R{i}.{ftype}', 'a') as outfile:
            for smi in progress_bar(can_smiles, parent=mb):
                randomized_smi = randomize_smiles(smi)
                outfile.write(randomized_smi + '\n')

def get_vocabulary(smiles, augmentation=0, exclusive_tokens = False):
    """Read text and return dictionary that encodes vocabulary
    """
    print('Counting SMILES...')
    vocab = Counter()

    for i, smi in enumerate(smiles):
        vocab[smi] += 1

    print(f'{len(vocab)} unique Canonical SMILES')

    if augmentation>0:
        print(f'Augmenting SMILES...({augmentation} times)')
        mb = master_bar(range(augmentation))
        for i in mb:
            for smi in progress_bar(smiles, parent=mb):
                randomized_smi = randomize_smiles(smi)
                vocab[randomized_smi] += 1

        print(f'{len(vocab)} unique SMILES (Canonical + Augmented)')
    return dict([(tuple(atomwise_tokenizer(x)) ,y) for (x,y) in vocab.items()])

def update_pair_statistics(pair, changed, stats, indices):
    """Minimally update the indices and frequency of symbol pairs
    if we merge a pair of symbols, only pairs that overlap with occurrences
    of this pair are affected, and need to be updated.
    """
    stats[pair] = 0
    indices[pair] = defaultdict(int)
    first, second = pair
    new_pair = first+second
    for j, word, old_word, freq in changed:

        # find all instances of pair, and update frequency/indices around it
        i = 0
        while True:
            # find first symbol
            try:
                i = old_word.index(first, i)
            except ValueError:
                break
            # if first symbol is followed by second symbol, we've found an occurrence of pair (old_word[i:i+2])
            if i < len(old_word)-1 and old_word[i+1] == second:
                # assuming a symbol sequence "A B C", if "B C" is merged, reduce the frequency of "A B"
                if i:
                    prev = old_word[i-1:i+1]
                    stats[prev] -= freq
                    indices[prev][j] -= 1
                if i < len(old_word)-2:
                    # assuming a symbol sequence "A B C B", if "B C" is merged, reduce the frequency of "C B".
                    # however, skip this if the sequence is A B C B C, because the frequency of "C B" will be reduced by the previous code block
                    if old_word[i+2] != first or i >= len(old_word)-3 or old_word[i+3] != second:
                        nex = old_word[i+1:i+3]
                        stats[nex] -= freq
                        indices[nex][j] -= 1
                i += 2
            else:
                i += 1

        i = 0
        while True:
            try:
                # find new pair
                i = word.index(new_pair, i)
            except ValueError:
                break
            # assuming a symbol sequence "A BC D", if "B C" is merged, increase the frequency of "A BC"
            if i:
                prev = word[i-1:i+1]
                stats[prev] += freq
                indices[prev][j] += 1
            # assuming a symbol sequence "A BC B", if "B C" is merged, increase the frequency of "BC B"
            # however, if the sequence is A BC BC, skip this step because the count of "BC BC" will be incremented by the previous code block
            if i < len(word)-1 and word[i+1] != new_pair:
                nex = word[i:i+2]
                stats[nex] += freq
                indices[nex][j] += 1
            i += 1

def get_pair_statistics(vocab):
    """Count frequency of all symbol pairs, and create index"""

    # data structure of pair frequencies
    stats = defaultdict(int)

    #index from pairs to words
    indices = defaultdict(lambda: defaultdict(int))

    for i, (word, freq) in enumerate(progress_bar(vocab)):
        prev_char = word[0]
        for char in word[1:]:
            stats[prev_char, char] += freq
            indices[prev_char, char][i] += 1
            prev_char = char

    return stats, indices

def replace_pair(pair, vocab, indices):
    """Replace all occurrences of a symbol pair ('A', 'B') with a new symbol 'AB'"""
    first, second = pair
    pair_str = ''.join(pair)
    pair_str = pair_str.replace('\\','\\\\')
    changes = []
    pattern = re.compile(r'(?<!\S)' + re.escape(first + ' ' + second) + r'(?!\S)')
    if sys.version_info < (3, 0):
        iterator = indices[pair].iteritems()
    else:
        iterator = indices[pair].items()
    for j, freq in iterator:
        if freq < 1:
            continue
        word, freq = vocab[j]
        new_word = ' '.join(word)
        new_word = pattern.sub(pair_str, new_word)
        new_word = tuple(new_word.split(' '))

        vocab[j] = (new_word, freq)
        changes.append((j, new_word, word, freq))

    return changes

def prune_stats(stats, big_stats, threshold):
    """Prune statistics dict for efficiency of max()
    The frequency of a symbol pair never increases, so pruning is generally safe
    (until we the most frequent pair is less frequent than a pair we previously pruned)
    big_stats keeps full statistics for when we need to access pruned items
    """
    for item,freq in list(stats.items()):
        if freq < threshold:
            del stats[item]
            if freq < 0:
                big_stats[item] += freq
            else:
                big_stats[item] = freq

def learn_SPE(infile, outfile, num_symbols, min_frequency=2, augmentation=0, verbose=False, total_symbols=False):
    """
    Learn num_symbols SPE operations from infile and write to outfile.

    *infile*: a list of SMILES

    *num_symbols*: maximum total number of SPE symbols

    *min_frequency*: the minimum frequency of SPE symbols appears.

    *augmentation*: times of SMILES augmentation

    *verbose*: if True, print the merging process

    *total_symbols*: if True; the maximum total of SPE symbols = num_symbols - number of atom-level tokens
    """



    vocab = get_vocabulary(infile, augmentation=augmentation)
    sorted_vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=True)

    print('Gettting Pair Statistics')
    stats, indices = get_pair_statistics(sorted_vocab)
    big_stats = copy.deepcopy(stats)

    if total_symbols:
        uniq_char = set()
        for word in vocab:
            for char in word:
                uniq_char.add(char)
        sys.stderr.write(f'Number of unique characters & Reducing number of merge operations by: {len(uniq_char)}\n')
        sys.stderr.write(f'Unique characters: {(uniq_char)}\n')
        num_symbols -= len(uniq_char)

    # threshold is inspired by Zipfian assumption, but should only affect speed
    threshold = max(stats.values()) / 10
    for i in range(num_symbols):
        if stats:
            most_frequent = max(stats, key=lambda x: (stats[x], x))

        # we probably missed the best pair because of pruning; go back to full statistics
        if not stats or (i and stats[most_frequent] < threshold):
            prune_stats(stats, big_stats, threshold)
            stats = copy.deepcopy(big_stats)
            most_frequent = max(stats, key=lambda x: (stats[x], x))
            # threshold is inspired by Zipfian assumption, but should only affect speed
            threshold = stats[most_frequent] * i/(i+10000.0)
            prune_stats(stats, big_stats, threshold)

        if stats[most_frequent] < min_frequency:
            sys.stderr.write('no pair has frequency >= {0}. Stopping\n'.format(min_frequency))
            break

        if verbose:
            sys.stderr.write('pair {0}: {1} {2} -> {1}{2} (frequency {3})\n'.format(i, most_frequent[0], most_frequent[1], stats[most_frequent]))
        outfile.write('{0} {1}\n'.format(*most_frequent))
        changes = replace_pair(most_frequent, sorted_vocab, indices)
        update_pair_statistics(most_frequent, changes, stats, indices)
        stats[most_frequent] = 0
        if not i % 100:
            prune_stats(stats, big_stats, threshold)