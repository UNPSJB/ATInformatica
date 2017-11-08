Django - Apps
=============

Las apps desarrolladas para este sistema en Django son las siguientes:
    
* websas
    App principal, contiene la configuración del servidor y las opciones generales del proyecto.
* sas
    App inicial, contiene la ruta y vista de la pantalla principal.
* usuario
    Define el modelo de usuario y comportamientos para la autenticación en el sistema.
* persona
    Define el modelo de persona y los comportamientos relativos al mismo. Es el eje central del patrón roles
    desarrollado en esta parte del sistema.
* servicio
    Define el modelo de Tipo de Servicio para la categorización de órdenes de trabajo y tarifado de tareas.
* rubro
    Define el modelo de Rubro para clasificar tareas, equipos y órdenes de trabajo.
* tarea
    Define el modelo de Tipo de Tarea para describir las unidades de trabajo que componen las órdenes de trabajo.
* tarifa
    Define el modelo que permite asignar el precio a un Tipo de Tarea en base al Rubro y Tipo de Servicio
    al que pertenece.
* producto
    Define el modelo de producto o insumo que puede ser gestionado de acuerdo a la modalidad ABM, o bien
    por medio del empleo como repuesto en alguna Tarea de una Orden de Trabajo.
* orden
    App central del sistema. Define varios modelos relacionados a la Orden de Trabajo, como así también el modelo
    de Equipo. Configura comportamiento para dicho documento en el sistema y para las Tareas que contiene, como así
    también el estado en que se encuentran.
* lela
    Plantilla `Gentelella Alela! por puikinsh (link) <https://github.com/puikinsh/gentelella>`_ adaptada como una `Django app por GiriB (link) <https://github.com/GiriB/django-gentelella>`_.
    Contiene los templates en base a los cuales se generaron los de WebSAS.

----------------

.. todo::
    Listar apps. Docstrings. Descripciones. Python.