# imports
import os
import csv
import sys
import codecs
import re
from SmilesPE.tokenizer import *

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))
checkpoint = os.path.abspath(os.path.join(root,"..", "..","checkpoints", "SPE_ChEMBL.txt"))

spe_vob = codecs.open(checkpoint)
spe = SPE_Tokenizer(spe_vob)

# my model
def my_model(smiles_list):
    return [spe.tokenize(smi) for smi in smiles_list]


# read SMILES from .csv file, assuming one column with header
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    smiles_list = [r[0] for r in reader]

# run model
temp_outputs = my_model(smiles_list)

outputs= []
MAX_TOKENS = 50
for item in temp_outputs:
    tokens = item.split()
    tokens = tokens[:MAX_TOKENS]
    tokens += [''] * (MAX_TOKENS - len(tokens))
    outputs.append(tokens)

N_SAMPLES = max(len(tokens) for tokens in outputs)

#check input and output have the same lenght
input_len = len(smiles_list)
output_len = len(outputs)
assert input_len == output_len

# write output in a .csv file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    header = ["token_{:02}".format(i) for i in range(50)]
    writer.writerow(header)  # header
    for o in outputs:
        writer.writerow(o)
