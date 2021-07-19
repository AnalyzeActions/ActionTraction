<p align="center">
  <img src="ActionTraction.png" />
</p>

![example workflow](https://github.com/AnalyzeActions/ActionTraction/actions/workflows/main.yml/badge.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/AnalyzeActions/WorkKnow/graphs/commit-activity)

## **ActionTraction** allows you to further understand how GitHub repositories are adopting GitHub Actions

### Learn more about:

- Adoption practices
- Workflow complexity
- Diff metrics
- Contributions
- Workflow steps & contents

## If you are interested in using ActionTraction for research, please follow the steps below:

### Cloning ActionTraction

Navigate to your preferred directory and clone the respository via your terminal.

1. With HTTPS: `git clone https://github.com/AnalyzeActions/ActionTraction.git`

2. With SSH: `git clone git@github.com:AnalyzeActions/ActionTraction.git`

### Install Poetry

Poetry is the tool that ActionTraction uses for dependency management. If you do not already have poetry installed on your machine, follow the installation steps within its [documentation](https://python-poetry.org/docs/#installation).

- osx / linux / bashon windows install instructions: 
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

- windows powershell install instructions:

```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

### Install Dependencies

Once ActionTraction has been cloned onto your machine, navigate into ActionTraction and install dependencies with `poetry`.

1. `cd ActionTraction`

2. `cd action-traction`

3. `poetry install`

### Running ActionTraction

ActionTraction can be run using Poetry.

1. Navigate into the `action_traction` directory: 
```
cd action_traction
```

2. Display all ActionTraction commands: `poetry run action-traction`

### ActionTraction Commands

_PLEASE NOTE:_ A user must run the _download_ and _repository-metrics_ commands before performing other analysis commands.

**download**

Download each repository that you would like to analyze. Files must be in a `.csv` file with a column labeled `url` with each of the repository urls that you are interested in. These repositories will be saved in a user-specified directory that is on your personal machine.

```
poetry run action-traction download csv_file_path.csv save_directory
```

**repository-metrics**

Metrics for the repository, must be generated using this command. Metrics are determined by using `PyDriller`, which mines each repository in the user-specified directory that is on your personal machine.

```
poetry run action-traction repository-metrics save_directory
```

**determine-diffs**

Look at the diffs of GitHub Actions workflows over time, including change in size, lines added, and lines removed. These diffs are calculated for every repository in the user-specified directory that is on your personal machine.

```
poetry run action-traction determine-diffs save_directory 
```

**contents-analysis**

Understand the contents of a repository's GitHub Actions worflows, including:

- Defined actions
- User specified commands
- Operating systems
- Environments
- Languages

```
poetry run action-traction contents-analysis save_directory
```

**contributors**

Understand which individuals are collaborating on GitHub Actions workflows, including:

- Name of collaborator
- Amount of commits per collaborator
- Percentage of overall contribution per collaborator

```
poetry run action-traction contributors save_directory
```

**determine-complexity**

Understand the complexity of GitHub Actions workflows, including 3 metrics:

- Halstead metrics
- Cyclomatic complexity
- Maintainability index

```
poetry run action-traction determine-quality save_directory
```
