#!/bin/bash

docker exec -it django-server python manage.py runserver 0.0.0.0:8000
