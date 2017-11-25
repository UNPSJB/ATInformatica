// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});




$(" #btn-eliminar-grupo ").on("click", function () {
    var grupo_id = this.dataset["grupo"]

    var data = {
        'grupo_id': grupo_id
    }

    $.ajax({
        url: this.dataset["ajax"],
        type: "POST",
        data: data,
        dataType: 'json',
        success: function (data) {
            $("#modalEliminarGrupo").modal("toggle")
            location.reload()
        },  
        error: function (data) {
        }
    })
})
