$(document).ready( function() {

    var busqueda_permiso = $('#busqueda_permiso'),
        busqueda_usuario = $('#busqueda_usuario'),
		titulo_usuario = $('.lista-perm-user.user'),
		titulo_permiso = $('.lista-perm-user.perm');


    var buscar = function (input){
        input = input
        return function(){
            var li = $(this);
      // console.log(li)
            //si presionamos la tecla
            input.keyup(function(){
                //cambiamos a minusculas
                this.value = this.value.toLowerCase();
                //
                var clase = $('.search i');
                if($(busqueda).val() != ''){
                    $(clase).attr('class', 'fa fa-times');
                }else{
                    $(clase).attr('class', 'fa fa-search');
                }
                if($(clase).hasClass('fa fa-times')){
                    $(clase).click(function(){
                        //borramos el contenido del input
                        $(busqueda).val('');
                        //mostramos todas las listas
                        $(li).parent().show();
                        //volvemos a añadir la clase para mostrar la lupa
                        $(clase).attr('class', 'fa fa-search');
                    });
                }
                //ocultamos toda la lista
                $(li).hide();
                //valor del h3
                var txt = $(this).val();

                /* 
                *  funcion para filtrar los elementos usuando lo que se ingresó
                *  en la search bar
                */
                var match_texto = function(index){
                    return $(this).text().toLowerCase().indexOf(txt) > -1
                    }

                // Los que cumplen con la condición se muestran
                $(li).filter(match_texto).show()


            });
        }

    }

    // generamos cada función para utilizar en cada elemento
    var b_usuario = buscar(busqueda_usuario)
    var b_permiso = buscar(busqueda_permiso)

    // Apply!
    $(titulo_usuario).each(b_usuario);
    $(titulo_permiso).each(b_permiso);
});

