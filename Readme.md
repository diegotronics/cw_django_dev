# Claritywave challenge

Author: CW-TEAM

## Instrucciones:

### How to

1. Genera un fork de este proyecto para que puedas trabajar en tu propio espacio.
2. Una vez finalizado, esperamos que nos envíes el enlace a tu repositorio y el tiempo estimado que te llevó hacerlo. Si no quieres hacer público tu fork, nos puedes contactar y te decimos como lo solucionamos.

### Constraints

Esperamos que dejes una app funcional.

- En la página principal se tienen que mostrar las mejores 20 preguntas ordenadas según el siguiente ranking:
  1. Cada respuesta suma 10 puntos al ranking
  2. Cada like suma 5 puntos al ranking
  3. Cada dislike resta 3 puntos al ranking
  4. Las preguntas del día de hoy, tienen un extra de 10 puntos

_Ejemplo_:
Una pregunta que tiene 6 respuesta de usuarios, 2 likes y 1 dislike:  
ranking: `6*10 + 2*5 - 1*3 = 60 + 10 - 3 = 67`  
Si además es del día de la hoy:  
ranking: `6*10 + 2*5 - 1*3 + 10 = 60 + 10 - 3 +10 = 77`

### A tener en cuenta:

- Modifica todo lo que creas necesario. Dejamos errores voluntariamente.
- Evaluaremos no solo la funcionalidad, también esperamos una buena performance ante la posibilidad de que escale el proyecto
- El sistema de login/logout no es necesario modificarlo. Genera los usuarios para probar desde la consola.

### Extras

- Si puedes levantar un entorno con docker, te invitamos a que lo hagas.
- Nos gustaría ver que puedes generar un test con los casos de usos básicos.

###

### Ejemplo

Este es un ejemplo de como queda el listado con su ranking y se ve como respondió/votó el usuario actual.

![Example](example.png)

# Solución

## Descripción de la solución

Los cambios realizados para resolver la prueba técnica fueron los siguientes:

- Agregar linter y formatter para prevenir errores de sintaxis y estandarizar el código.
- Correr makemigrations y migrate para crear las tablas necesarias para el proyecto.
- Corregir que cada url terminara con un slash.
- Corrección de la vista "answer_question" para registrar correctamente las respuestas.
- Agregar modelo LikeDislike para registrar los likes y dislikes de las preguntas.
- Agregar vista "like_question" para registrar los likes y dislikes de las preguntas.
- Agregar método para calcular el ranking de las preguntas.
- Evitar que los usuarios no autenticados puedan votar o responder preguntas.
- Impedir que los usuarios puedan editar preguntas que no son de su propiedad.
- Ordenar la lista de preguntas por ranking de mayor a menor.
- Agregar la lógica en javascript para que el usuario pueda votar y responder preguntas.
- Agregar paginador para mostrar las preguntas, 10 por página.
- Añadir Dockerfile para crear la imagen de la aplicación.
- Creación de las pruebas unitarias para los modelos y algunas vistas de Survey

**Bonus:**

- Agregar una nueva vista para que los usuarios puedan ver sus preguntas. (mis preguntas)
- Nueva rama "heroku" para desplegar la aplicación en Heroku con conexión a una base de datos PostgreSQL.

## Requerimientos para ejecutar la aplicación en local

- Python 3.10

## Ejecutar la aplicación en local

1. Crear un entorno virtual con python 3.10
2. Instalar las dependencias del proyecto con el comando `pip install -r requirements.txt`
3. correr las migraciones con el comando `python manage.py migrate`
4. Crear varios super usuario con el comando `python manage.py createsuperuser`
5. Correr el servidor con el comando `python manage.py runserver`

## Ejecutar las pruebas unitarias

En el archivo requirements.txt se encuentra la dependencia coverage para ejecutar las pruebas unitarias y obtener el porcentaje de cobertura de código.

1. Ejecutar el comando `coverage run manage.py test`

## Ejecutar la aplicación con Docker

1. Crear la imagen de la aplicación con el comando `docker build -t claritywave .`
2. Crear el contenedor con el comando `docker run -p 8000:8000 claritywave`
3. Abrir el navegador en la dirección http://localhost:8000

## Interacción con la aplicación en Heroku

1. Ingresar a la dirección https://clarity-test-63d73cdd6c60.herokuapp.com/
2. Ingresar con el usuario "admin" y contraseña "admin123"
