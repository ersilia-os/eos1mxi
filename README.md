# SmilesPE: tokenizer algorithm for SMILES, DeepSMILES, and SELFIES

The Smiles Pair Encoding method generates smiles substring tokens based on high-frequency token pairs from large chemical datasets. This method is well-suited for both QSAR activities as well as generative models. The model provided here has been pretrained using ChEMBL.

## Identifiers

* EOS model ID: `eos1mxi`
* Slug: `smiles-pe`

## Characteristics

* Input: `Compound`
* Input Shape: `Single`
* Task: `Generative`
* Output: `Compound`
* Output Type: `String`
* Output Shape: `Flexible List`
* Interpretation: A data-driven tokenization method for SMILES-based deep learning models in cheminformatics, demonstrating high performance in molecular generation and QSAR prediction tasks compared to atom-level tokenization

## References

* [Publication](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.0c01127)
* [Source Code](https://github.com/XinhaoLi74/SmilesPE)
* Ersilia contributor: [Richiio](https://github.com/Richiio)

## Ersilia model URLs
* [GitHub](https://github.com/ersilia-os/eos1mxi)
* [AWS S3](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos1mxi.zip)
* [DockerHub](https://hub.docker.com/r/ersiliaos/eos1mxi) (AMD64, ARM64)

## Citation

If you use this model, please cite the [original authors](https://pubs.acs.org/doi/abs/10.1021/acs.jcim.0c01127) of the model and the [Ersilia Model Hub](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff).

## License

This package is licensed under a GPL-3.0 license. The model contained within this package is licensed under a Apache-2.0 license.

Notice: Ersilia grants access to these models 'as is' provided by the original authors, please refer to the original code repository and/or publication if you use the model in your research.

## About Us

The [Ersilia Open Source Initiative](https://ersilia.io) is a Non Profit Organization ([1192266](https://register-of-charities.charitycommission.gov.uk/charity-search/-/charity-details/5170657/full-print)) with the mission is to equip labs, universities and clinics in LMIC with AI/ML tools for infectious disease research.

[Help us](https://www.ersilia.io/donate) achieve our mission!