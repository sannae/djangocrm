# djangocrm
A little project to create a CRM web application with [Django](https://www.djangoproject.com/) using [Dennis Ivy's tutorial](https://youtube.com/playlist?list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO).

## Requirements
* [Python](https://www.python.org/downloads/)
* [Django](https://www.djangoproject.com/download/)

## Notes
* The project structure is created with `py -m manage startproject`
* Within the project, there may be several *apps*: each app structure is created with `py -m manage startapp`; in our case the main and only app is called `accounts`
* The views of the app call the templates saved in `accounts/templates/accounts` (according to a Django's convention)
* The templates use a combination of HTML/CSS/JS and Django's `{% block %}` syntax: this lets you modularize the code
* The HTML/CSS/JS templates use [Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
* Bootstrap was not installed, we just copied/edited some templates found online

## Usage
* To debug the application with live rendering, run `py -m manage runserver` from the root folder and browse to *http://localhost:8000*
