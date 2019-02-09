# Library App

Una completa aplicación de librería hecha con Django en Python 3.* y Boostrap 4.

## Caracteristicas

- Conexión con la API de Goodreads.
- Tablero de noticias.
- Categoría para los libros.
- Manejo de rentas.
- Solicitudes de libros.
- Likes y marcadores de libros.
- Reseñas de libros.
- Perfiles de usuario.

## Instalación

Clona el repositorio

    git clone https://github.com/xyvs/library-app

Ingresa a la carpeta de la aplicación

	cd library-app/

Inicia el entorno virtual

    pipenv shell

Instala los requerimientos

    pipenv install

Crear superusuario

    python manage.py createsuperuser

Ejecuta la aplicación

    python manage.py runserver

## Uso

Visitar http://localhost:8000/ para utilizar el sistema como usuario no registrado.

Para utilizar el sistema como administrador ingresar como admin:admin en http://localhost:8000/accounts/login/.

## Capturas

![Index](https://i.imgur.com/JYZ7nyH.png)
![Search](https://i.imgur.com/BmdqqGG.png)
![Book](https://i.imgur.com/wdNTwJW.png)
![Rent](https://i.imgur.com/93ZaYxv.png)