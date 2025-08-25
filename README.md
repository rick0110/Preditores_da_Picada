# Preditores_da_Picada

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/badge/license-Apache2.0-green.svg)](LICENSE)
[![Poetry](https://img.shields.io/badge/poetry-v1.8.3-blue.svg)](https://python-poetry.org/)

## Overview
This repository hosts a machine learning project to predict dengue cases across Brazilian states using SARIMA (Seasonal AutoRegressive Integrated Moving Average) time series modeling. The goal is to develop state-specific predictive models to assist public health officials in managing dengue outbreaks using historical epidemiological data and climatic variables. The results obtained here can be visualized in [mosqlimate dashboard plataform](https://api.mosqlimate.org/vis/dashboard/?dashboard=sprint), including some evaluations metrics.

## Table of Contents
- [Project Description](#project-description)
- [Methodology](#methodology)
- [Validation and forecast](#validation-and-forecast)
- [Repository Structure](#repository-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Data](#data)
- [Contributing](#contributing)
- [License](#license)

## Project Description
This project uses SARIMA time series modeling to predict dengue case counts per Brazilian state. The methodology uses temporal patterns to achieve this. Jupyter notebooks in `notebooks/states/` handle exploratory data analysis, and modeling, with detailed implementation shown in `rio_de_janeiro_arima.ipynb`.

## Methodology

### SARIMAX Model Framework
The prediction model is built using SARIMA (Seasonal ARIMA without eXogenous variables), implemented as described in `/notebooks/states/rio_de_janeiro_arima.ipynb`. This approach combines:

1. **Seasonal ARIMA Components**:
   - **AutoRegressive (AR)**: Past dengue cases influence current cases
   - **Integrated (I)**: Differencing to achieve stationarity
   - **Moving Average (MA)**: Past forecast errors improve current predictions
   - **Seasonal**: Weekly and yearly seasonal patterns (52-week cycle)

### Data Processing Pipeline

1. **Data Extraction**: InfoDengue API integration for epidemiological surveillance data
2. **Aggregation**: Municipal to state-level aggregation
   - Cases: Sum across municipalities
   - Climatic variables: Mean across municipalities
   - Population and receptivity: Average values

3. **Preprocessing**:
   - Log transformation: `log(cases + 0.1)` for variance stabilization
   - Weekly temporal resolution
   - Handling of zero values and missing data

4. **Time Series Analysis**:
   - STL Decomposition (Seasonal-Trend decomposition using LOESS)
   - Stationarity testing with Augmented Dickey-Fuller test
   - Autocorrelation autocorrelation analysis

### Model Configuration
- **Order**: SARIMAX(2,1,2) x (2,1,2,52)
  - Non-seasonal: AR(2), I(1), MA(2)
  - Seasonal: AR(2), I(1), MA(2) with 52-week periodicity
- **Validation**: Out-of-sample forecasting performance

### Mathematical Foundation
The SARIMAX model follows the equation:
```
φ(B)Φ(B^s)(1-B)^d(1-B^s)^D y_t = θ(B)Θ(B^s)ε_t
```
Where:
- φ(B), Φ(B^s): Non-seasonal and seasonal AR polynomials
- θ(B), Θ(B^s): Non-seasonal and seasonal MA polynomials
- d, D: Non-seasonal and seasonal differencing orders

### Validation Framework
- **Temporal validation**: Sequential train-test splits respecting time order
- **Epidemiological weeks**: EW 41 2010 to EW 25 for training periods
- **Forecast horizons**: 52-week ahead predictions

## Validation and forecast
The validation and forecast were done in four stages:
1. **Validation test 1.** We predicted the weekly number of dengue cases by state (UF) in the 2022-2023 season [EW 41 2022- EW40 2023], using data covering the period from EW 40 2010 to EW 25 2022;
2. **Validation test 2.** We predicted the weekly number of dengue cases by state (UF) in the 2023-2024 season [EW 41 2023- EW40 2024], using data covering the period from EW 40 2010 to EW 25 2023;
3. **Validation test 3.** We predicted the weekly number of dengue cases by state (UF) in the 2024-2025 season [EW 41 2024- EW40 2025], using data covering the period from EW 40 2010 to EW 25 2024;
4. **Forecast.** And finally we predicted the weekly number of dengue cases in Brazil, and by state (UF), in the 2025-2026 season [EW 41 2025- EW40 2026], using data covering the period from EW 40 2010 to EW 25 2025;

## Repository Structure
```
dengue-prediction/
├── data/                    # Datasets (raw and processed, ignored by Git)
├── notebooks/               # Jupyter notebooks for analysis and modeling
│   └── states/            # State-specific notebooks for EDA, modeling, and evaluation
├── src/                     # Reusable scripts for preprocessing, modeling, and evaluation    
├── models/                  # Trained models saved as .pkl files (ignored by Git)
├── project.toml             # Poetry configuration file for dependencies
├── initialize_directories.sh # Script to create project directories
├── README.md                # Project documentation (this file)
├── .gitignore               # Files and folders to ignore (e.g., *.csv, *.pyc, models/, data/)
└── LICENSE                  # Apache License
```

## Setup Instructions
This project uses four main folders. To create them, run the `initialize_directories.sh` script from the `Preditores_da_Picada/` directory:
```bash
bash initialize_directories.sh
```

The first folder is `src/`, containing all reusable scripts. All scripts should be written and saved in this folder.

The second folder is `data/`, where datasets are stored. This folder is ignored by Git to avoid uploading data. Before running the project, place your raw data files in `data/`.

The third folder is `models/`, where trained models are saved preferably as `.pkl` files. if the model is very large avoid commit.

### Install pyenv and Poetry
Install `pyenv` to manage Python versions:
```bash
curl https://pyenv.run | bash
```

Open `~/.bashrc` (or `~/.zshrc` for Zsh) with an editor (e.g., `vim ~/.bashrc`) and add:
```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
export PATH="$HOME/.local/bin:$PATH"
```

Install Python 3.12 and set it as the active version:
```bash
pyenv install 3.12
pyenv shell 3.12
```

Install Poetry for dependency management:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Restart your terminal to apply changes.

Install Poetry's shell plugin and configure virtual environments:
```bash
poetry self add poetry-plugin-shell
poetry config virtualenvs.in-project true
```

Install project dependencies:
```bash
poetry install
```

Install a filter for Jupyter notebooks to strip outputs before committing(this step is optional):
```bash
poetry shell
nbstripout --install --attributes .gitattributes
```

Activate the virtual environment:
```bash
poetry shell
```

Periodically update dependencies:
```bash
poetry update
```

Add new packages with:
```bash
poetry add package-name
```

To open in VS Code, run:
```bash
code .
```
Ensure the `.venv/bin/python` interpreter is selected in VS Code.

## Usage
### Notebooks
Run Jupyter notebooks for state-specific analysis:
```bash
poetry shell
jupyter notebook notebooks/states/
```

### Scripts
Execute the SARIMAX forecasting script from the `src/` directory:
```bash
poetry shell
python src/Sarima.py
```

This script generates forecasts for multiple validation periods, upload the predictions to [mosqlimate dashboard plataform](https://api.mosqlimate.org/vis/dashboard/?dashboard=sprint), and saves the results in the `forecasts/` directory.

### usage for forecasting
This work can be used for forecasting new data by only adding the data in `./data` and your `APY_key`of [masqlimate data plataform](https://api.mosqlimate.org/) in `./src/Sarima.py`. Your results can be visualized in [mosqlimate dashboard plataform](https://api.mosqlimate.org/vis/dashboard/?dashboard=sprint).

### Models
The SARIMAX model implementation is detailed in `notebooks/states/minas_gerais_arima.ipynb`, which demonstrates:
- Complete methodology and mathematical foundation
- Data preprocessing and feature engineering
- Model fitting and parameter selection
- Validation and performance evaluation
- Forecast generation and confidence intervals

## Data
The project uses data from the InfoDengue surveillance system, which provides:
- **Epidemiological data**: Weekly dengue cases, population data
- **Climatic variables**: Temperature and humidity measurements
- **Vector indices**: Mosquito receptivity indicators
- **Temporal coverage**: 2010-2025 with weekly resolution
- **Geographical scope**: All Brazilian states and municipalities
In the final predictions uploaded, we used the data dengue.csv.gz available in [info.dengue.mat.br](info.dengue.mat.br)

## Contributing
Contributions are welcome! Please follow these guidelines:
- Fork the repository and create a feature branch
- Test your changes with the provided datasets
- Submit a pull request with a clear description of modifications

For questions about the SARIMAX methodology, refer to the detailed implementation in `notebooks/states/minas_gerais_arima.ipynb`.

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
