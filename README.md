# TODO List Website


![banner-todo2](https://github.com/arenaf/todo-list-website/assets/169451601/d22f35c5-b1ea-48b6-b908-fced73396bd4)



## Sobre el desarrollo
Sitio web que permite planificar tareas que vamos a realizar y las lista según su estado (pendientes o completadas).

Este proyecto fue desarrallado con ***Python*** y se utilizaron los siguientes frameworks y librerías:
- El framework ***Flask*** para la creación de la web.
- La librería ***SQLAlchemy*** para la manipulación de los datos.
- ***WTForms*** para la generación y validación de los formularios.
- El framework de ***Bootstrap*** como herramienta para hacer el diseño responsive.

## Manejo de la web
### Pantalla de inicio

![init-todo](https://github.com/arenaf/todo-list-website/assets/169451601/90240236-fdd0-4852-8196-a8e260f9e7f6)



Los usuario deben estar logueados para poder ver sus tareas. Si no hay ningún usuario logueado, en la barra de menú se muestran dos posibilidades: **Login** o **Registro**.
Ambas categorías contemplan errores mediante mensajes *flash*: 
- El formulario de **Registro** muestra error si un usuario ya exite o si el email no es válido.
- El formulario de **Login** vuelca un mensaje si no existe el email, la contraseña es incorrecta o el email no es válido.
  

![password-todo](https://github.com/arenaf/todo-list-website/assets/169451601/38e464ba-0cc9-4beb-92b5-dd55598d9fba)


### Usuario activo
Tras loguearse un usuario, se muestra una lista con sus tareas, o una tabla vacía en caso de que aún no haya creado ninguna, y un botón para añadir una nueva tarea. 
A su vez, se activan varias opciones en la barra de navegación:
- **TODO**: tabla con las tareas *Pendientes*.
- **Todas las tareas**: tabla con las tareas *Pendientes* y las *Completadas*.
- **Completadas**: tabla con las tareas que ya han sido realizadas.
- **Nueva tarea**: redirige a la página para registrar una tarea.
- **Vista tarjeta**: muestra las tareas *Pendientes*, *Completadas* o *Todas las tareas* con formato tarjeta.
- A la derecha de la barra de navegación, desparecen las opciones de **Login** y **Registro** y aparece la opción de **Logout**.

![tareas-pendientes](https://github.com/arenaf/todo-list-website/assets/169451601/3a141a45-023e-4655-b310-08dfa07279e4)


### Funcionalidades

Cada tarea se puede modificar :pencil2:, eliminar :wastebasket: o cambiar su estado de *Pendiente* a *Completa*.

![todas-tareas](https://github.com/arenaf/todo-list-website/assets/169451601/d1646cf0-7691-406e-ba3d-2950a30fea73)


Ejemplo de cambio de vista de las tareas a modo tarjeta en vez de en una sola línea.

![pendientes-tarjeta](https://github.com/arenaf/todo-list-website/assets/169451601/c5fa3b7b-1822-4d72-92b3-2ab3435487a3)


### Responsive

El texto se ajusta a pantallas más pequeñas.

![responsive](https://github.com/arenaf/todo-list-website/assets/169451601/c08f894a-5eb0-4af4-a101-e29213945fa2)



## Requerimientos
Son necesarias las siguientes librerías:
- Flask
- Bootstrap
- SQLAlchemy
- Werkzeug
- Wtforms


