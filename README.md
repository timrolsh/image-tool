# image-tool

Usage of pandas to help opencv ->
Usage of opencv to -> manipulate the images themselves, cropping or background doesn't work yet but resizes and renames, and converts images properly
Usage of excel, a comfortable and familiar workspace for Skim analysts, to get user input (for now)

## Python Version

* This project uses python version 3.12.3. This version, along with all other project dependencies, are defined in the [environment.yml](./environment.yml) file for ease of install and setup using Conda.

## Getting Started/Setup

* To get started with this python project, create a virtual environment using Conda from the configuration file defined in the root of the project: [environment.yml](./environment.yml)

```bash
conda env create -f environment.yml
```

* After the environment has been created, activate it with the following command:

```bash
conda activate image-tool
```

## Working with VSCode

* To avoid any import issues with VSCode and to properly get all syntax highlighting, etc., open your vscode from within the root of the project only after you'e activated the environment and conda has finished installing all of the packages. Then, you can open VSCode for the project using:

```bash
code .
```

## Launching Project

* To launch the project frontend, run the following command from within the activated virtual environment with all packages installed:

```bash
streamlit run front_end.py
```
