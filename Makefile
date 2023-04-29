install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

start:
	python manage.py runserver

test:
	pytest