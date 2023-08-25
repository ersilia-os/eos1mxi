__all__ = ["index", "modules", "custom_doc_links", "git_url"]

index = {"atomwise_tokenizer": "00_pretokenizer.ipynb",
         "kmer_tokenizer": "00_pretokenizer.ipynb",
         "tokens_to_mer": "00_pretokenizer.ipynb",
         "randomize_smiles": "01_learner.ipynb",
         "corpus_augment": "01_learner.ipynb",
         "get_vocabulary": "01_learner.ipynb",
         "update_pair_statistics": "01_learner.ipynb",
         "get_pair_statistics": "01_learner.ipynb",
         "replace_pair": "01_learner.ipynb",
         "prune_stats": "01_learner.ipynb",
         "learn_SPE": "01_learner.ipynb",
         "SPE_Tokenizer": "02_tokenizer.ipynb",
         "encode": "02_tokenizer.ipynb",
         "isolate_glossary": "02_tokenizer.ipynb",
         "Corpus": "03_spe2vec.ipynb",
         "learn_spe2vec": "03_spe2vec.ipynb",
         "load_spe2vec": "03_spe2vec.ipynb",
         "SPE2Vec": "03_spe2vec.ipynb"}

modules = ["pretokenizer.py",
           "learner.py",
           "tokenizer.py",
           "spe2vec.py"]

doc_url = "https://XinhaoLi74.github.io/SmilesPE/"

git_url = "https://github.com/XinhaoLi74/SmilesPE/tree/master/"

def custom_doc_links(name): return None