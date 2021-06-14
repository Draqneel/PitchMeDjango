# PitchMeDjango

### At first, update database refs in *settings.py* in:

```python
DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'draqneel',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Load dependencies and apply migrations in database:
```sh
╰─$ pip install -r requirements.txt
╰─$ python manage.py makemigrations
╰─$ python manage.py migrate  
```

### Create super user:
```sh
╰─$ python manage.py createsuperuser 
```

### Run application:
```sh
╰─$ python manage.py runserver
```
