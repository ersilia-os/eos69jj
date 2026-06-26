# N.gonorrhoeae antimicrobial activity

Deep learning graph neural network (D-MPNN) that predicts the probability of a small molecule inhibiting Neisseria gonorrhoeae growth. This is the retrained Round 2 model, trained on duplicate growth-inhibition screening at 50 uM against N. gonorrhoeae ATCC 49226 for 1755 clinically approved drugs (Pharmakon), an internal 37K-compound library, and a first round of experimentally validated hits. It was used to rescreen the Broad 800K library and identify compound A1, which reduced N. gonorrhoeae titers in an in vivo mouse vaginal infection model.

This model was incorporated on 2026-06-24.Last packaged on 2026-06-26.

## Information
### Identifiers
- **Ersilia Identifier:** `eos69jj`
- **Slug:** `neisseria-gonorrhoeae-activity`

### Domain
- **Task:** `Annotation`
- **Subtask:** `Activity prediction`
- **Biomedical Area:** `Gonorrhea`, `Antimicrobial resistance`
- **Target Organism:** `Neisseria gonorrhoeae`
- **Tags:** `Antimicrobial activity`, `Gram-negative bacteria`, `Chemical graph model`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `1`
- **Output Consistency:** `Fixed`
- **Interpretation:** Higher score indicates greater predicted probability of growth inhibition against Neisseria gonorrhoeae.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| activity_score | float | high | Predicted probability that the molecule inhibits Neisseria gonorrhoeae growth |


### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos69jj](https://hub.docker.com/r/ersiliaos/eos69jj)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos69jj.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos69jj.zip)

### Resource Consumption
- **Model Size (Mb):** `442`
- **Environment Size (Mb):** `4095`
- **Image Size (Mb):** `4966.4`

**Computational Performance (seconds):**
- 10 inputs: `39.61`
- 100 inputs: `69.74`
- 10000 inputs: `-1`

### References
- **Source Code**: [https://github.com/jackievaleri/ngonorrhoeae_abx_ml_discovery](https://github.com/jackievaleri/ngonorrhoeae_abx_ml_discovery)
- **Publication**: [https://doi.org/10.1126/scitranslmed.ads4699](https://doi.org/10.1126/scitranslmed.ads4699)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2026`
- **Ersilia Contributor:** [GemmaTuron](https://github.com/GemmaTuron)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [MIT](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos69jj
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos69jj
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
