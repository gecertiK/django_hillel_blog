$(function () {

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal .modal-content").html("");
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        console.log(form)
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#modal").modal("hide");
                } else {
                    $("#modal-contact .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    $(".js-contact").click(loadForm);
    $("#modal-contact").on("submit", ".js-contact-form", saveForm);

});
