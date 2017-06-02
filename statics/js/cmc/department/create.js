/**
 * Created by fmc on 16/10/1.
 */

var departments_url = '/restapi/cmc/departments/';

$("#SubmitButton").click(function () {
    var form_obj = $("#UserDepartmentForm");
    var form_data = form_obj.serializeArray();
    var post_data = $.each(form_data, function (index, field_obj) {
        var data = {};
        data[field_obj.name] = field_obj.value;
        return data
    });

    $.post(departments_url, post_data, function (data) {
        alert_success_for_form('成功!!', '添加部门成功!!', '/cmc/departments/' + data.id + '/', data.name)
    }).fail(function (response_obj, status) {
        alert_failed_for_form(response_obj, status, departments_url, form_obj)
    });

});

$("#CancelButton").click(function () {
    window.location.reload();
});

