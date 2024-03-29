# Connect Four
[![Build Status](https://app.travis-ci.com/rsouthwi/connect-four.svg?branch=main)](https://app.travis-ci.com/rsouthwi/connect-four)
<p align="center" width="100%">
<img src="c4.jpg">
</p>

Connect four of your checkers in a row while preventing your opponent from doing the same.
The game Connect Four is played by two players taking turns dropping a red or black piece into one of the columns.
When there are four of one color in a straight line (including diagonals), that player wins.
Try it out on [my website](https://ronsouthwick.com/connect4).

## AWS Lambda
I've created a version to run this app on an AWS Lambda.  It uses [Chalice](https://github.com/aws/chalice).
#### Run locally:
* `poetry install`
* `poetry run chalice local`

#### Deploy:
* `poetry run chalice deploy`

## Web
The web version uses [Flask](https://flask.palletsprojects.com/en/2.2.x/).
#### Run locally:
* `poetry install`
* `cp .env-example .env`  (create a .env file)
* `flask run`  (runs a development server on port 8001)
* `poetry run gunicorn web.app:app --reload -c conf.py` (runs a production server on port specified in conf.py)

### Running Unit Tests
* `poetry run pytest`

## Notebook
There is a version in the `notebook` directory built to be played in a [Jupyter Notebook](https://github.com/jupyter/notebook).
#### Install
* `poetry install`
* `poetry run jupyter notebook`