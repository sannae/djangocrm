# djangocrm
A little project to create a CRM web application with [Django](https://www.djangoproject.com/) using [Dennis Ivy](https://github.com/divanov11)'s [YouTube tutorial](https://youtube.com/playlist?list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO).

The CRM is a web application that lets you:
* Perform CRUD operations on Customers, Products, Orders and Users
* Manage the database, user logins as an administrator
* Check the status of the whole context with a dashboard

## Requirements
* [Python](https://www.python.org/downloads/)
* [Django](https://www.djangoproject.com/download/)
All the required Python packages are listed in `requirements.txt` (to be updatable with `pip freeze > requirements.txt`), run `pip install -r requirements.txt` to load them in your environment.

## Notes
* The project structure is created with `py -m django startproject`
* Within the project, there may be several *apps*: each app structure is created with `py -m django startapp`; in our case the main and only app is called `accounts`
* The live web server is started with `py -m django manage runserver`
* The views of the app call the templates saved in `accounts/templates/accounts` (according to a Django's convention)
* The templates use a combination of HTML/CSS/JS and Django's `{% block %}` syntax: this lets you modularize the code
* The HTML/CSS/JS templates use [Bootstrap](https://getbootstrap.com/docs/5.1/getting-started/introduction/)
* Bootstrap was not installed, we just copied/edited some templates found online
* Oversimplifying, to add a feature you
  1) Update the model in `models.py` (if needed)
  2) Create or update the corresponding view in `views.py`
  3) If the new feature opens a new page, create the new html page in `templates/` and add it to `urls.py`
* :warning: Do _not_ comment Django template tags with usual HTML comments, as described [here](https://stackoverflow.com/questions/62793267/reverse-for-create-order-with-no-arguments-not-found)!! 
```html
<!-- this is the usual HTML comment -->
<!-- {% This is a Django tag %} -->
<!-- {#% This is a commented Django tag %#} -->
```

### About database and relationships
* To initiate the database, run `py -m manage migrate`: the database's settings are in `SETTINGS.py` and SQLite3 is the default.
* To run progressive migrations, edit your models then run `py -m manage makemigrations` to create your migration files (preparation files before actual migration) in `/APPNAME/migrations/`. Remember to register your models in the _admin_ panel to see them.
* To retrieve data from the db, use [this reference guide](https://docs.djangoproject.com/en/2.2/ref/models/querysets):
  1) Open your Django shell (`py -m manage shell`)
  2) Import all your models (`from APPNAME.models import *`)
  3) Specific tables are then available as objects with `TABLENAME.objects.all()` and other methods. 
     1) Example: to retrieve all the customers saved with the `Customer` method, run `Customer.objects.all()`
     2) Example: to retrieve all the customers with a specific name, run `Customer.objects.all().filter(name="YOURNAME")`

## Usage
* To debug the application with live rendering, run `py -m manage runserver` from the root folder and browse to *http://localhost:8000*

## **Definitely** review:
* [Forms](https://docs.djangoproject.com/en/3.2/topics/forms/) and [Formsets](https://docs.djangoproject.com/en/3.2/topics/forms/formsets/)

## Next
* :whale: [Dockerize the project](https://docs.docker.com/samples/django/)!
* :ocean: Deploy on [Azure Web App](https://docs.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app?tabs=bash%2Cclone&pivots=postgres-single-server) 
* :toolbox: Deploy on [ACS](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-using-azure-container-registry)