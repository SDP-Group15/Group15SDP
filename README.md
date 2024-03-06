# Boehringer Ingelheim MeSH Senior Design Project

Most flask operations are conducted from `UserInterface.py` and much of the frontend development takes place in `templates/index.html`.

In order to run this web application, start a local PostgreSQL server and use the following terminal command:
```sh
flask --app UserInterface.py run
```

Some specific information for various components of this project is included in `README_Files`.

## Dependencies

1. Flask
```sh
pip install Flask
```
2. psycopg2
```sh
pip install psycopg2
```
3. simplejson
```sh
pip install simplejson
```
or
```sh
python3 -m pip install simplejson
```
4. scipy
```sh
pip install scipy
```
