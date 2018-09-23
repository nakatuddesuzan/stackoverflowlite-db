[![Build Status](https://travis-ci.org/nakatuddesuzan/stackoverflowlite-db.svg?branch=challenge-three)](https://travis-ci.org/nakatuddesuzan/stackoverflowlite-db)
[![Coverage Status](https://coveralls.io/repos/github/nakatuddesuzan/stackoverflowlite-db/badge.svg?branch=challenge-three)](https://coveralls.io/github/nakatuddesuzan/stackoverflowlite-db?branch=challenge-three)
# StackOverflow-lite
StackOverflow-lite is a platform where people can ask questions and provide answers.

- This branch contains API endpoints for the above application intergrated with a database

## Built-with
- `Python3.6` - Programming language that lets you work more quickly
- `Flask` - Python based web framework
- `Virtualenv` - A tool to create isolated virtual environment
- `PostgreSQL` - A general purpose and object-relational database management system
- `Psycopg2`   - A DB API 2.0 compliant PostgreSQL driver 

## Running the tests
To run tests run this command below in your terminal

```
nosetests -v --with-coverage
```

## Installation
**Clone this _Repository_**
```
$ https://github.com/nakatuddesuzan/StackOverflow-lite.gite
$ cd StackOverflow-lite
```
**Create virtual environment and install it**
```
$ virtualenv --python=python3 venv
$ source /venv/bin/activate
```
**Install all the necessary _dependencies_ by**
```
$ pip install -r requirements.txt
$ Install PostgreSQL
$ CREATE DATABASE stackover flow
$ CREATE TABLE users
$ CREATE TABLE questions
$ CREATE TABLE replies

```
**Run _app_ by**

```
Run the server At the terminal or console type
$ Python run.py
```
## Versioning
```
This API is versioned using url versioning starting, with the letter 'v'
This is version one"v1" of the API
```
## End Points
|           End Point                      |     Functionality     |   Access   | Requirements|
|   -------------------------------------- |-----------------------|------------|-------------|
|     POST   api/v1/users/signup           | Registers a new user  |   PUBLIC   | email, password, username
|     POST api/v1/question/user_id         | Post User Questions   |   PRIVATE  | description, title, subject, user_id |
|     GET  api/v1/question/user_id/qtn_id  | Get one user Question |   PRIVATE  |user_id, question_id
|     GET  api/v1/questions/user_id        | Get users Question    |    PRIVATE  |user_id
|     PUT api/v1/question/user_id/qtn_id   | Edit user Question    |   PRIVATE  |user_id, question_id
|    DELETE api/v1/question/user_id/qtn_id | Delete user Question  |   PRIVATE  |user_id, question_id
|    POST   api/v1/users/login             | Login User            |   PUBLIC   |Email, password
|POST api/v1/question/qtnid/answer         | Post areply for a question|PRIVATE |user_id, question_id
|DELETE api/v1/question/qtnid/answer/reply_id|Delete a user reply  | PRIVATE    |user_id, qtn_id, reply
|PUT api/v1/question/qtnid/answer/reply_id|Update user reply       |PRIVATE |user_id, reply_id, qtn_id

## Contributors
- [Sue](https://github.com/nakatuddesuzan)

## Acknowledgements
- [Sue](https://github.com/nakatuddesuzan)
- Team Bruno

> *If you don't make it through the first time call it v1*

> *Don't stop because you are tired, Stop because you are done*

> *Learning is a continous process*

> *If i had six hours to chop down the tree i would take the first four hours sharpening the axe*
