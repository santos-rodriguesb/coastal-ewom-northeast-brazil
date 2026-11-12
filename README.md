# Coastal eWOM and Digital Accountability in Northeast Brazil

This repository contains the replication code and processed aggregated dataset for empirical analyses investigating User-Generated Content (UGC), electronic Word-of-Mouth (eWOM), and managerial accountability in coastal tourist destinations in Northeast Brazil.

This work supports the study:
> **Relationship Strategy and Digital Accountability: eWOM in Coastal Tourism**  
> *Breno dos Santos-Rodrigues & André Riani Costa Perinotto* (2026)

## Repository Structure

- `data/`: Contains the processed and aggregated dataset (`dataset_metrico_agregado.csv`) used to run the statistical models and NLP pipeline, preserving the confidentiality of the raw corpus texts in compliance with open science and platform guidelines.
- `scripts/`: 
  - `01_econometric_hc3_and_chisq.R`: R script executing robust multiple linear regression (HC3 standard errors via `estimatr`) and Chi-Square contingency tests for managerial silence.
  - `02_nlp_lda_leia_pipeline.py`: Python script executing lexical sentiment intensity analysis (LeIA) and Latent Dirichlet Allocation (LDA) probabilistic topic modeling.
- `requirements.txt`: Python dependencies required to reproduce the computational environment.
- `LICENSE`: Open-source licensing terms.

## Requirements and Reproducibility

### R Environment
To install the required R packages, run the following command in your R console:

    install.packages(c("readxl", "stringr", "lubridate", "dplyr", "writexl", "car", "lmtest", "nortest", "estimatr"))

### Python Environment
To install the required Python libraries, run the following command in your terminal:

    pip install -r requirements.txt

## Citation
If you use these scripts or data in your research, please cite:

    @article{rodrigues2026relationship,
      title={Relationship Strategy and Digital Accountability: eWOM in Coastal Tourism},
      author={Rodrigues, Breno dos Santos and Perinotto, André Riani Costa},
      year={2026}
    }

## License
This project is licensed under the terms of the [MIT License](LICENSE).
