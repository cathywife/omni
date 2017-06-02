/**
 * Created by fmc on 16/10/8.
 */

function init_object_detail(obj, nested_fields) {
    $.each(obj, function (field, value) {
        var element_id = 'id_' + field;
        var element_obj = $('#' + element_id);
        if (element_obj.length === 0){
            return true
        }
        var element_type = element_obj.get(0).tagName;
        init_object_detail_element[element_type](field, value, element_obj, nested_fields)
    })
}


var init_object_detail_element = {
    'INPUT': init_object_detail_input_element,
    'SELECT': init_object_detail_select_element,
    'TEXTAREA': init_object_detail_textarea_element,
};


function init_object_detail_input_element(field, value, element_obj, nested_fields) {
    element_obj.val(value)
}


function init_object_detail_textarea_element(field, value, element_obj, nested_fields) {
    element_obj.val(value)
}


function init_object_detail_select_element(field, value, element_obj, nested_fields) {
    if ($.inArray(typeof value, ['number', 'string']) >= 0) {
        append_option_to_select_element(element_obj, field, value, true)
    } else if (typeof value === 'object'){
        if (value === null) {
            return
        }
        // 获取nested field
        var nested_id_field, nested_text_field;
        if (nested_fields && field in nested_fields && nested_fields[field]){
            nested_id_field = nested_fields[field]['id'];
            nested_text_field = nested_fields[field]['text'];
        } else {
            nested_id_field = 'id';
            nested_text_field = 'visible_name';
        }

        var select_type = element_obj[0].type;
        if (select_type === 'select-multiple') {
            $.each(value, function (i, nested_obj) {
                append_option_to_select_element(element_obj, nested_obj[nested_id_field], nested_obj[nested_text_field], true)
            })
        } else {
            append_option_to_select_element(element_obj, value[nested_id_field], value[nested_text_field], true)
        }
    }
}


function append_option_to_select_element(element_obj, id, text, selected) {
    var option_obj = _create_select_option(id, text, selected);
    element_obj.append(option_obj).trigger('change');
}


function _create_select_option(id, text, selected) {
    var option_obj;
    if (selected) {
        option_obj = $('<option selected>Loading...</option>').val(id).text(text)
    } else {
        option_obj = $('<option>Loading...</option>').val(id).text(text)
    }
    return option_obj
}
