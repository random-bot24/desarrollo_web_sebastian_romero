# Actividades DCC .
### Projecto de Desarrollo de Aplicaciones Web


#### 1.Funcionamiento de la app en la actualidad.
La aplicacion web posee 4 paginas para acceder e interactuar, con las siguientes funcionalidades:

- Portada o menu: Posee un menu de bienvenida con una imagen y una lista de los 5 ultimos miembros. Imagen sacada de Unsplash.com.

- Registro de miembros: Formulario de registro de miembros. Los campos del formulario son los mismos que se pedian en la base de datos. Incluye sus respectivas validaciones en js.

- Registro de actividades: Se accede mediante el registro de miembros, una vez se hace el registro como miembro, este te redirecciona al registro de actividades. Incluye sus respectivas validaciones en js

- Lista de miembros: Se incluye una lista de miembros con el metodo de paginacion. Cada pagina incluye 5 miembros, esto se hizo como prueba para probar si funcionaba. 

- Estadisticas: Dos graficos hechos con highcharts y AJAX. Se utilizó fetch para el manejo de las APIS.

- Comentarios: Implementación de comentarios para la actividad de cada miembro. También se utilizó AJAX para mayor comodidad.

- Busqueda de Actividades: Busqueda de actividades implementadas en SpringBoot. En este se incluye AJAX para mayor fluidez.

#### 2.Decisiones tomadas

#### Decisiones implementadas Tarea 1
- Para comenzar, las primeras decisiones que se tomaron es utilizar una navbar para usar las redirecciones, ya que es lo primero que el usuario ve, y asi le permite cambiar de pagina facilmente.

- Para mostrar los errores en validaciones, se usó una lista de errores que aparece en el principio de la pagina. En el momento que se envia el formulario de registro con errores, te envía al comienzo del formulario, ya que si no se hacia esto no se podia ver los errores, por lo que era incomodo para el usuario.
 
- Para la validacion del correo (la mas complicada) se usó una expresion regular donde el correo debe contener texto antes del arroba, despues del arroba debe contener texto y tambien el punto que corresponde.

#### Decisiones implementadas Tarea 2
- El registro de actividades se accede una vez terminado el registro de miembros, esto se debe a que solo los miembros pueden registrar actividades. Este acceso, se hace mediante una redireccion una vez terminado el registro. 

- No se hicieron cambios a la base de datos entregada por el equipo docente. Se añadieron y se hicieron cambios en los formularios para facilitar el proceso.

#### Deciones implementadas Tarea 3
- Se usó fetch y try/catch para el manejo de las APIS y las funciones asincronas, para implementar los comentarios y los graficos. Esto para mayor comodidad.

#### Decisiones implementadas en la Tarea 4:
Se utilizaron las siguientes herramientas para la Tarea4:
+ Maven
+ ThymeLeaf
+ MySqlDriver
+ JPA
+ Spring Web
+ DevTools
+ Validate

- Se usó fetch y encadenamiento para las funciones de JavaScript con asincronizacion.

- Al momento de agregar una nueva evaluación. En su lugar, se implementó una consulta JPQL personalizada en el archivo NotaRepository.

- Se reutilizó el CSS que se utilizó en Flask




