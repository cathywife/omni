/**
 * Created by fmc on 16/9/26.
 */

function table_gen_td(objInfo, key, subKey, verboseUrl) {
    if (!objInfo || !key || objInfo[key] == null || !String(objInfo[key]).length) {
        return '<td></td>'
    }
    verboseUrl = verboseUrl == true ? verboseUrl : false;
    var realObjInfo = subKey ? objInfo[key] : objInfo;
    var realKey = subKey ? subKey : key;
    var a_element;
    if (verboseUrl) {
        a_element = realObjInfo['__url__'] ? '<a href="' + realObjInfo['__url__'] + '">' + realObjInfo[realKey] +'</a>' : '';
    } else {
        a_element = '';
    }

    return a_element ? '<td>' + a_element + '</td>' : '<td>' + realObjInfo[realKey] + '</td>'
}
