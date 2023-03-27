## Finsure Lenders

## Overview

Rather than write this as a typical readme I will explain what I did and how I found the process. It has been
a while since I've done django and python in this way, so it took me a while to set things up. It took me longer
than I'd like to setup mariadb, and django I had refresh my knowledge there.

Nonetheless, I found the task quite enjoyable and it was good to get my hands dirty in some python code again. I do like
the way django has batteries included and a lot of good libraries such as the one I describe below for doing json:api.

## Things to consider doing differently or improving.

* I'd have a dev and test database in databases rather than just the mariadb settings in settings.py
* I used the [django rest framework for json:api](https://django-rest-framework-json-api.readthedocs.io/en/stable/) and
  it gave me a lot for free.
* I'd like to add more test cases but given the time constraints focussed on functionality and there is still no test
  for downloading and more tests are required for edge cases

## Setup and Running

One should be able to checkout the code and install using pipenv from the root dir. The database needs the appropriate
user and database setup. See the script db_setup.sql. Then one would run the migrations. `python manage.py migrate`.

You can run the tests via `python manage.py test`