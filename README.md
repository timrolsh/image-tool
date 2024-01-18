# image-tool

Usage of pandas to help opencv ->
Usage of opencv to -> manipulate the images themselves, cropping or background doesn't work yet but resizes and renames, and converts images properly
Usage of excel, a comfortable and familiar workspace for Skim analysts, to get user input (for now)

## Getting Started/Setup

* To get started with this python project, create a virtual enviornment (conda or venv) with a command like this:

```bash
conda create --name image-tool python=3.10
```

* This project uses python version 3.10
* After the environment has been created, activate it with a command like this:

```bash
conda activate image-tool
```

* Once the environment has been activated, install the necessary project dependencies from the requirements.txt by running this command from the root of the project using:

```bash
pip install -r requirements.txt
```

## Working with VSCode

* To avoid any import issues with VSCode and to properly get all syntax highlighting, etc., open your vscode from within the root of the project only after you'e activated the environment and installed the packages, in that order. Then, you can open VSCode for the project using:

```bash
code .
```

## Launching Project

* To launch the project frontend, run the following command:

```bash
streamlit run frontend.py
```
