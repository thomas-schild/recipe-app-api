# recipe-app-api
Receipe app api source code
Check Udemy Course [Build a Backend REST API with Python & Django](https://www.udemy.com/course/django-python-advanced/) by Mark Winterbottom

## Python/Django templating

    * run python/django's management tool to create an app module, e.g. for the app's core module:
        > docker-compose run --rm app sh -c "python manage.py startapp core"
    * the modules are:
      - core
      - user
      - recipe
      - ...

## cleanup and extend the created stuff

    * models are only kept in the core module => therefore remove models.py elsewhere
    * migrations only needed for models => remove migrations sub-folder else where
    * use a designated test folder instead of tests.py => remove tests.py, mkdir tests, touch tests/__init__.py
    * ...
    * enable app module in app/settings.py

## Django-Admin

    * run the recipe-app 
        > docker-compose up
    * access Django Admin page in browser
        http://localhost:8000/admin/
    * ensure a 'superuser' is/was created 
        > docker-compose run app sh -c "python manage.py createsuperuser"

## Django REST Endpoints

    * Django renders a Web-UI for the REST endpoints
    * ensure recipe-app is running
        > docker-compose up
    * check for supported URLs
        http://localhost:8000/
    * ensure _NO_ token is provided without user
        > curl -d "email=none@demo.org&password=anything" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8000/api/user/token/
    * create user
        > curl -d "email=test.demo@demo.org&password=secret&name='Demo User'" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8000/api/user/create/
    * ensure token is provided with right credentials for this user
        > curl -d "email=test.demo@demo.org&password=secret" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8000/api/user/token/

    * access the user's profile for an authenticaed user
        > curl -H "Authorization: Token f6f46a1c8160fedcc53174302e6ef929198732fb" -X GET http://localhost:8000/api/user/me/
