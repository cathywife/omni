/**
 * Created by fmc on 16/10/1.
 */
var pnotify_stack_style = {
    'stack_topleft': {"dir1": "down", "dir2": "right", "push": "top"},
    'stack_bottomleft': {"dir1": "right", "dir2": "up", "push": "top"},
    'stack_modal': {"dir1": "down", "dir2": "right", "push": "top", "modal": true, "overlay_close": true},
    'stack_bar_top': {"dir1": "down", "dir2": "right", "push": "top", "spacing1": 5, "spacing2": 5},
    'stack_bar_bottom': {"dir1": "up", "dir2": "right", "spacing1": 0, "spacing2": 0},
    'stack_bottomright': {"dir1": "up", "dir2": "left", "firstpos1": 25, "firstpos2": 25}
};

function pnotify_alert_from_top_center(title, text, type) {
    var opts = {
        title: title ? title : "title为空",
        text: text ? text : "text为空.",
        type: type ? type : "notice",
        addclass: "stack-bar-top alert-dismissible",
        cornerclass: "",
        width: "60%",
        stack: pnotify_stack_style['stack_bar_top'],
        styling: "fontawesome"
    };
    return new PNotify(opts);
}

function pnotify_alert_for_ajax(response_obj, url) {
    var alert_msg;
    var alert_level;
    if(response_obj == 404){
        alert_msg = '异步接口<a href=' + url + '>' + url + '</a>调用失败. Http状态码: ' + response_obj.status +
            '错误类型: ' + response_obj.statusText;
        alert_level = 'notice';
    } else if($.inArray(response_obj.status, [500, 501, 502, 503, 504, 401, 403]) >= 0) {
        alert_msg = '异步接口<a href=' + url + '>' + url + '</a>调用失败. Http状态码: ' + response_obj.status +
            '错误类型: ' + response_obj.statusText + '. 错误信息: '+ response_obj.responseJSON;
        alert_level = 'error';

    } else if($.inArray(response_obj.status, [400]) >= 0) {
        alert_msg = '异步接口<a href="' + url + '">' + url + '</a>调用失败. Http状态码: ' + response_obj.status +
            '错误类型: ' + response_obj.statusText;
        alert_level = 'notice';

    } else {
        alert_msg = '异步接口<a href=' + url + '>' + url + '</a>调用失败. Http状态码: ' + response_obj.status +
            '错误类型: ' + response_obj.statusText;
        alert_level = 'error';
    }
    pnotify_alert_from_top_center('失败', alert_msg, alert_level);
    return [alert_msg, alert_level]
}

function alert_success_for_form(title, msg, url, visible_name, form_obj) {
    title = title ? title :'Success!!';
    msg = msg ? msg :'默认消息,请从合适的描述覆盖.';
    url = url ? url :'#';
    visible_name = visible_name ? visible_name :url;

    alert_clear_error_label_for_form_field(form_obj);
    pnotify_alert_from_top_center(title, msg + '<a href="' + url + '">' + visible_name + '</a>', 'success')
}

function alert_failed_for_form(response_obj, status, url, form_obj) {
    alert_clear_error_label_for_form_field(form_obj);
    //当form的ajax请求失败时, 展示form错误信息
    pnotify_alert_for_ajax(response_obj, url);
    if($.inArray(response_obj.status, [400]) >= 0) {
        alert_error_for_form_field(form_obj, response_obj.responseJSON)
    }
}

function alert_error_for_form_field(form_obj, data) {
    $.each(data, function (key, value) {
        var field_obj = $("#id_" + key);
        $.each(value, function (index, err_msg) {
            var lable_html = '<label class="control-label"><i class="fa fa-bell-o"></i> ' +
            err_msg + '</label>';
            field_obj.before(lable_html).parent().parent().addClass('has-error');
        })
    })
}

function alert_clear_error_label_for_form_field(form_obj) {
    form_obj.children(".form-group").removeClass('has-error has-warning has-success');
    form_obj.find('.form-group div label').remove();
}
