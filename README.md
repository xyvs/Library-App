# Library App

Esta es una aplicación diseñada para el uso de una librería, en ella se pueden agregar/solicitar libros (gracias a la conexión de la API de Goodreads, no es necesario ingresar la información del libro desde cero), los usuarios pueden solicitar rentas de libros para recogerlos en la librería, crear marcadores, likear libros, manejar rentas, ver retrasos y plazos de entrega, entre otros. como administrador se puede agregar libros, manejar rentas, manejar solicitudes de libros, editar inventarios, cantidades, crear usuarios, entre otros. La aplicación está diseñada en el Framework Django y utiliza Python 3.* para el lado del servidor. En esta también se manejan conceptos como OOP y MVC, ademas de el framework de Boostrap 4.

## Instalación

```git clone https://github.com/xyvs/Library-App && cd Library-App/```

```pip install -r requeriments.txt```

```python3 manage.py runserver```

## Uso

Visitar http://localhost:8000/ para utilizar el sistema como usuario no registrado.

Para utilizar el sistema como administrador ingresar como admin:admin en http://localhost:8000/master/.

## Capturas


![Index](https://i.imgur.com/JYZ7nyH.png)
![Search](https://i.imgur.com/BmdqqGG.png)
![Book](https://i.imgur.com/wdNTwJW.png)
![Rent](https://i.imgur.com/93ZaYxv.png)
