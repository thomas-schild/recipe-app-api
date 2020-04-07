# recipe-app-api
Receipe app api source code

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
