$(document).ready(function(){
    var abstractCavingGameData = {};
    abstractCavingGameData.move_count = abstractCavingGameData_temp.move_count;
    abstractCavingGameData.total_points = abstractCavingGameData_temp.total_points;
    abstractCavingGameData.visited_room_ids = abstractCavingGameData_temp.visited_room_ids;
    abstractCavingGameData.from_title = abstractCavingGameData_temp.from_title;

    function addHidden(theForm, key, value) {
        // Create a hidden input element, and append it to the form:
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;'name-as-seen-at-the-server';
        if (key == 'visited_room_ids' && value.length === 0) {
            input.value = 0;
            }
        else {
            input.value = value;
            }
        theForm.appendChild(input);
    }
    
    function addHiddens(theForm) {
        // Add data:
        addHidden(theForm, 'move_count', abstractCavingGameData.move_count);
        addHidden(theForm, 'total_points', abstractCavingGameData.total_points);
        addHidden(theForm, 'visited_room_ids', 
            JSON.stringify(abstractCavingGameData.visited_room_ids));
        addHidden(theForm, 'from_title', abstractCavingGameData.from_title);
    }
    
    
    /* addHiddens(theForm, current_title); */
    $(".pure-button").click(function() {
        theForm = $(this).parent()[0];
        if ($(this)[0].id != 'high_score_submit') {
            addHiddens(theForm);
            theForm.submit();
        }
    });
    
    $("#high_score_submit").click(function() {
        var csrftoken = csrfToken();
        var high_score_name = $("#high_score_name").val();
        $.ajax({
            type: "POST",
            url: "/save-high-score/",
            beforeSend: function(xhr) {
                xhr.setRequestHeader ("X-CSRFToken", csrftoken);
            },
            data: {
                name: high_score_name,
                move_count: abstractCavingGameData.move_count,
                total_points: abstractCavingGameData.total_points,
            },
            dataType: "html",
            success: function(data) {
                $("#alert_window_main").html(data);
            }
        });
    });
}
);


// POST requests will be thrown back in your face if you don't do this stuff
    // https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#how-to-use-it
    // because of cross-site request forgery concerns
function csrfToken() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    return csrftoken;
}