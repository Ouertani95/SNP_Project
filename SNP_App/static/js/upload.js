$(document).ready(function () {
    $("label").addClass("form-label");
});

$(document).on('submit', "#upload_form", function (e) {
    e.preventDefault();
    $('#waiting_row').removeClass("d-none");
    $('#success_row').addClass("d-none");
    $('#error_row').addClass("d-none");
    var data = new FormData();
    var csrf = document.getElementById("upload_script").getAttribute("data-name");
    data.append('file', $("input[id^='id_file']")[0].files[0]);
    data.append('csrfmiddlewaretoken', csrf);
    $.ajax({
        url: "/upload/",
        type: 'POST',
        method: 'POST',
        processData: false,
        contentType: false,
        data: data,
        success: function (data) {
            document.getElementById('upload_form').reset();
            if (data["error"] !== "") {
                $('#waiting_row').addClass("d-none");
                $('#success_row').addClass("d-none");
                $('#error_row').removeClass("d-none");
                $('#error').html(data["error"]);
            } else {
                $('#waiting_row').addClass("d-none");
                $('#error_row').addClass("d-none");
                $('#success_row').removeClass("d-none");
                $('#success').html(data["success"]);
            }
        },
        error: function () {
            console.log("error")
        }
    })

})