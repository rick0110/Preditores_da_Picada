# Preditores_da_Picada

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Poetry](https://img.shields.io/badge/poetry-v1.8.3-blue.svg)](https://python-poetry.org/)

## Overview
This repository hosts a machine learning project to predict dengue cases across Brazilian states using historical data, weather patterns, and demographic information. The goal is to develop state-specific predictive models to assist public health officials in managing dengue outbreaks. Models are saved as `.pkl` files for reusability.

## Table of Contents
- [Project Description](#project-description)
- [Repository Structure](#repository-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Data](#data)
- [Contributing](#contributing)
- [GitHub Workflow](#github-workflow)
- [License](#license)

## Project Description
This project uses machine learning to predict dengue case counts per Brazilian state. Jupyter notebooks in `notebooks/states/` handle exploratory data analysis, modeling, and evaluation.

## Repository Structure
```
dengue-prediction/
├── data/                    # Datasets (raw and processed, ignored by Git)
├── notebooks/               # Jupyter notebooks for analysis and modeling
│   └── states/            # State-specific notebooks for EDA, modeling, and evaluation
├── src/                     # Reusable scripts for preprocessing, modeling, and evaluation
│   ├── __init__.py         # Makes src a Python module
├── models/                  # Trained models saved as .pkl files (ignored by Git)
├── project.toml             # Poetry configuration file for dependencies
├── initialize_directories.sh # Script to create project directories
├── README.md                # Project documentation (this file)
├── .gitignore               # Files and folders to ignore (e.g., *.csv, *.pyc, models/, data/)
└── LICENSE                  # MIT License
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
Execute scripts from the `src/` directory:
```bash
poetry shell
python src/main.py
```

### Models
Train and save state-specific models as `.pkl` files in `models/` using scripts in `src/models.py`.

## GitHub Workflow
- **Issues**: Report bugs or suggest features via GitHub Issues.
- **Branches**:
  - `main`: Stable code.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file.