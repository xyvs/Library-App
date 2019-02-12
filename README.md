# Library App

A complete library app built with Django in Python 3.* and Boostrap 4.

## Features

- Conection with the Goodreads API.
- News board.
- Books Categories.
- Books rents managment.
- Books requests managment.
- Books likes and bookmarks.
- Books reviews.
- User profiles.

## Installation

Clone the repository

    git clone https://github.com/xyvs/library-app

Enter the app folder

	cd library-app/

Access the virtual enviroment

    pipenv shell

Install the requeriments

    pipenv install

Create Super User

    python manage.py createsuperuser

Run the app

    python manage.py runserver

## Usage

Visit localhost:8000 to use the app as a non registered user.

To use the app as an admin login with the credentials you introduced before in localhost:8000/accounts/login/.

## Screenshots

![Index](https://i.imgur.com/JYZ7nyH.png)
![Search](https://i.imgur.com/BmdqqGG.png)
![Book](https://i.imgur.com/wdNTwJW.png)
![Rent](https://i.imgur.com/93ZaYxv.png)
