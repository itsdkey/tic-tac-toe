# tic-tac-toe

* [Intuition](#intuition)
* [Local development](#local-development-using-virtualenv)
    * [using virtualenv](#local-development-using-virtualenv)
    * [using docker compose](#local-development-using-docker-compose)
* [Project conventions](#project-conventions)

## Intuition
Just a fun project to code a simple Tic-Tac-Toe game. However, I created two games actually:
- the console version (in console package)
- the desktop version using [PyGame](https://www.pygame.org/news) (in desktop package)

I wanted to test out the PyGame lib and also practise some design patterns. Thanks to this motive I
was able to add the following design patterns:
- State (The game class can have 3 states: PRE_GAME, GAME, POST_GAME based on which the game behaves differently
(shows different windows))


## Local development using virtualenv
First, check which Python version is used in the Dockerfile.
If you do not have the current version please install it.
Then create a python virtual env:
```shell
python3.12 -m venv env/
```

Activate the env and set PYTHONPATH:
```shell
source env/bin/activate
export PYTHONPATH=`pwd`
```

Install the requirements:
```shell
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
```

Start the console app by:
```shell
cd console/
python main.py
```
Or the desktop version just by (from the root directory):
```shell
python main.py
```


## Local development using docker compose
NOTE: the only works for the console version because for PyGame we need to be able to show the app itself.

Start the application with the following:
```shell
docker compose up --build
```
Enter the container:
```shell
docker compose run --rm app bash
```
And run the console version with:
```shell
cd console/
python main.py
```

## Project conventions
The project follows some specific conventions thanks to pre-commit:
- isort
- black
- flake8
- no-commit-to-branch (main branch)
- bandit
- docformatter
- python-safety-dependencies-check

To install the GitHub pre-commit hooks. This can be done in your virtual
environment by:
```shell
pre-commit install
```