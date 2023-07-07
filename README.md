PROYECTO UNIVERSITARIO GPT-UNAM

Consiste en realizar practicas para universitarios de la carrera de informatica y relacionadas, mediante el uso de diversas API's con Inteligencia Artificial, de manera automatizada, en donde los profesores suben los temas de cada una de sus materias, suben sus recursos adicionalmente a la plataforma y se almacenan en la base de datos.
El proposito es solo crear practicas con introduccion, pasos, conclusiones e imagenes de referencia en pdf y diapositivas.

En caso de fallar el entorno virtual se deben instalar algunos paquetes con los siguientes comandos:

Django

    $ python -m pip install Django

MySQL Connector

    $ pip install mysqlclient

-----------

REGISTRO DE CAMBIOS

[230623]
-Commit inicial
-Html de login, signup, index.
-Estilo en css de las vistas antes descritas.
-Modelo del usuario
-Vistas que redireccionan a los html con su URL.
-Aun no tienen funcionalidad.
-Se agregan las imagenes

[230628]
-Se agregaron los html de dashboard y recovery
-Se agrego un virtual environment
-Se agregan los modelos de materias y temas.
-Funcionalidad con mensajes personalizados con alertifyjs
-Se modificaron algunas lineas de los estilos CSS
-Se agrega funcionalidad a las diferentes vistas
-Solo el dashboard sigue incompleto
-Se agrego un proceso de encriptacion a las contraseñas
-Se corrigieron errores en el modelo de usuario.

[230707]
-Ahora los campos del formulario de registro son obligatorios
-Se aumenta la privacidad al quitar mensajes de compilacion durante el registro
-Ahora es posible editar la cuenta de un usuario
-Se agregaron 3 opciones nuevas en el dashboard, crear materias/temas, chat, crud de usuarios (para administrador), estas opciones de momento estan publicas pero en futuras actualizaciones el acceso solo sera para ciertos roles de usuario.
-Se agregaron instrucciones al presente documento para la instalacion de librerias para poder compilar la pagina.