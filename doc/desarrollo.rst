Desarrollo - Aspectos técnicos
==============================

Se presenta a continuación un resumen de cada subsección de esta parte del documento.

El código fuente se encuentra disponible en `GitHub (link) <https://github.com/UNPSJB/ATInformatica>`_.

*Índice de contenido:*

.. toctree::
    desarrollo/web
    desarrollo/apps
    desarrollo/dominio

-------------

Plataforma web
    Se eligió basar el desarrollo en Web pensando en el modo de trabajo de AT-Informática, en que
    los técnicos realizan, principalmente, dos tipos de trabajos:

    1) Reparaciones en taller
    2) Diagnósticos y/o reparaciones on-site

    Considerando que todos los trabajos generan un documento central, la Orden de Trabajo, y que la disponibilidad
    tecnológica hoy en día lo permite con medios de conexión móvil como las redes 2G/3G/4G, se optó por emplear
    la plataforma web como medio para el flujo de información que necesita soportar la organización.

    Ver sección completa: :doc:`Plataforma web <desarrollo/web>`

-------------

Django y apps del sistema
    El sistema se basa en la arquitectura propuesta por Django de acuerdo a su filosofía, que pretende ser sencilla,
    entendible, mantenible, extensible y amigable.

    Cada app cumple una función, alberga modelos relacionados y contiene su propia tabla de ruteo para las URLs,
    de modo que la legibilidad y organización del código, propiamente, presenta constantemente la posibilidad
    de escalar y expandir la funcionalidad general del sistema.
    
    Ver sección completa: :doc:`Django - Apps <desarrollo/apps>`

-------------

Dominio y modelos
    El relevamiento inicial de la organización permitió listar y modelar conceptualmente la mayoría de los elementos
    involucrados en el dominio de la operatoria de la empresa. No obstante, estas "clases conceptuales" debieron
    sufrir modificaciones a lo largo del desarrollo para poder mejorar el entendimiento del dominio de aplicación
    y ayudar a que el producto final pueda integrarse de forma efectiva en el mismo. También fue necesario
    efectuar adaptaciones propias de la tecnología empleada.

    Se presenta, en esta subsección, los cambios más significativos en el dominio entre las clases conceptuales
    del relevamiento inicial y los modelos finalmente implementados en el producto desarrollado.

    Ver sección completa: :doc:`Dominio y modelos <desarrollo/dominio>`
