/**
 * Created by fmc on 16/10/1.
 */

$("#id_dev_user_group").select2({
ajax: {
  url: "/restapi/user/groups/",
  dataType: 'json',
  delay: 250,
  data: select2_data_func,
  processResults: select2_process_results,
  cache: true
}});

$("#id_ops_user_group").select2({
ajax: {
  url: "/restapi/user/groups/",
  dataType: 'json',
  delay: 250,
  data: select2_data_func,
  processResults: select2_process_results,
  cache: true
}});

$("#id_product").select2({
ajax: {
  url: "/restapi/arch/products/?page=off",
  dataType: 'json',
  delay: 250,
  data: select2_data_func('name'),
  processResults: select2_process_results('name'),
  cache: true
}
});

$("#id_dev_department").select2({
ajax: {
  url: "/restapi/cmc/departments/?page=off",
  dataType: 'json',
  delay: 250,
  data: select2_data_func('name'),
  processResults: select2_process_results('name'),
  cache: true
}});


var projects_url = '/restapi/arch/projects/';

$("#SubmitButton").click(function () {
    var form_obj = $("#ProjectForm");
    var form_data = form_obj.serializeArray();
    var post_data = $.each(form_data, function (index, field_obj) {
        var data = {};
        data[field_obj.name] = field_obj.value;
        return data
    });

    $.post(projects_url, post_data, function (data) {
        alert_success_for_form('成功!!', '添加项目成功!!', '/arch/projects/' + data.id + '/', data.name)
    }).fail(function (response_obj, status) {
        alert_failed_for_form(response_obj, status, projects_url, form_obj)
    });

});

$("#CancelButton").click(function () {
    window.location.reload();
});

