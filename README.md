PROYECTO UNIVERSITARIO GPT-UNAM

Consiste en realizar practicas para universitarios de la carrera de informatica y relacionadas, mediante el uso de diversas API's con Inteligencia Artificial, de manera automatizada, en donde los profesores suben los temas de cada una de sus materias, suben sus recursos adicionalmente a la plataforma y se almacenan en la base de datos.
El proposito es solo crear practicas con introduccion, pasos, conclusiones e imagenes de referencia en pdf y diapositivas.

En caso de fallar el entorno virtual se deben instalar algunos paquetes con el siguiente comando:

    $ pip install -r requirements.txt

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

[230721]
-Se agrego requirements.txt para agilizar el despliegue de la aplicación.
-Se agregaron vistas para agregar y eliminar materias, temas y subtemas.
-Se corrigio el problemas de los roles de usuario, no se puede acceder a ciertas paginas si no se es administrador o profesor.
-Se agrego una funcion para que los alumnos se puedan registrar a una materia, los profesores pueden ver la lista de los alumnos inscritos a su materia.
-Los alumnos tambien pueden ver sus materias inscritas.
-En el dashboard ahora se muestran materias, temas y subtemas.
-En la vista de los subtemas se puede elegir entre generar un video relacionado al azar, atraves de youtube y generar una practica con inteligencia artificial mediante la API de OpenAI (para esta funcionalidad es necesario poner tu API KEY en settings.py).
-El modulo de chat aun no funciona.
-Es la primer version que puede usar un usuario final, aunque aun esta en beta, las funciones escenciales estan listas para su uso.

[231008]
-Se cambiaron algunas vistas para hacer la interfaz mas llamativa e intuitiva.
-Aunque se cambiaron algunas vistas, no se ha eliminado ninguna hasta terminar la fase beta.
-Se agregaron modelos para mejorar la experiencia y funcionalidad de la plataforma.
-Los modelos creados funcionaran para poder registrar mejores estadisticas para lograr los objetivos.
-Se agrego una vista para el chat (aun sin funcionalidad).
-Se agrego una encuesta inicial para entender las preferencias de aprendizaje del usuario.
-Se planea remover la api de chatgpt para comenzar a usar llama de meta.