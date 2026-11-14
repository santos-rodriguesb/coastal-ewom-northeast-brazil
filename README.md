# coastal-ewom-northeast-brazil

This repository contains the replication code and processed dataset for empirical analyses investigating User-Generated Content (UGC), electronic Word-of-Mouth (eWOM), and tourist loyalty in coastal tourist destinations in Northeast Brazil.

This work supports the Master's dissertation:
> **A experiência turística como preditor da fidelização em destinos turísticos costeiros: uma abordagem multimétodo de avaliações online**  
> *Breno dos Santos-Rodrigues* (2026)  
> *Universidade Federal do Paraná (UFPR)*

## Repository Structure

- `data/`: Contains the primary structured TripAdvisor dataset (`dados_nordeste.xlsx`, $N = 24,638$) covering coastal destinations across all nine states of Northeast Brazil (2011–2025).

- `scripts/`:  
  - `01_econometric_analysis_study1.R`: R script executing data cleaning, feature engineering, multiple linear regression with HC3 robust standard errors (`estimatr`), and Chi-Square contingency tests for managerial silence.  
  - `02_nlp_lda_leia_study2.py`: Python script executing text preprocessing, LeIA lexical sentiment analysis, and Latent Dirichlet Allocation (LDA) probabilistic topic modeling.

- `requirements.txt`: Python dependencies required to reproduce the computational environment.

- `LICENSE`: Open-source licensing terms.

## Requirements and Reproducibility

### R Environment
To install the required R packages for Study 1, run the following command in your R console:

    install.packages(c("readxl", "stringr", "lubridate", "dplyr", "writexl", "car", "lmtest", "nortest", "estimatr"))

### Python Environment
To install the required Python libraries for Study 2, run the following command in your terminal:

    pip install -r requirements.txt

## Citation
If you use these scripts or data in your research, please cite:

    @mastersthesis{rodrigues2026experiencia,
      author  = {Rodrigues, Breno dos Santos},
      title   = {A experi{\^e}ncia tur{\'i}stica como preditor da fideliza{\c{c}}{\~a}o em destinos tur{\'i}sticos costeiros: uma abordagem multim{\'e}todo de avalia{\c{c}}{\~o}es online},
      school  = {Universidade Federal do Paran{\'a} (UFPR)},
      year    = {2026},
      address = {Curitiba, PR, Brazil}
    }

## License
This project is licensed under the terms of the [MIT License](LICENSE).
