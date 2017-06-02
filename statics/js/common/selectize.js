/**
 * Created by fmc on 16/10/31.
 */


function selectize_init_for_select(opts, ajax_opts) {
    var label_field = opts.labelField ? opts.labelField : 'name';
    var visible_field = opts.visibleField ? opts.visibleField : 'visible_name';
    var init_options, init_items;
    if (opts.options && isArrayFn(opts.options) && opts.options.length > 0){
        init_options = opts.options
    } else if (opts.options && ! isArrayFn(opts.options)){
        init_options = [opts.options]
    } else {
        init_options = []
    }

    if (opts.items && isArrayFn(opts.items) && opts.items.length > 0){
        init_items = opts.items
    } else if (opts.items && ! isArrayFn(opts.items)){
        init_items = [opts.items]
    } else {
        init_items = []
    }

    return {
      valueField: opts.valueField ? opts.valueField : 'id',
      labelField: label_field,
      searchField: opts.searchField ? opts.searchField : 'name',
      create: false,
      preload: 'focus',
      options: init_options,
      items: init_items,
      maxItems: opts.maxItems ? opts.maxItems : 1,
      render: {
        option: function (item, escape) {
          return "<div>" + escape(item[label_field]) + "<small>" + escape(eval('item.' + visible_field) ? eval('item.' + visible_field) : item[label_field]) + "</small></div>"
        }
      },
      load: function (query, callback) {
        $.ajax({
          url: ajax_opts.url,
          type: ajax_opts.type ? ajax_opts.type : 'GET',
          dataType: 'json',
          data: {
            'name': query,
            'page-size': ajax_opts.page_size ? ajax_opts.page_size : 10
          },
          cache: true,
          error: function () {
            callback()
          },
          success: function (res) {
            if (res.results.length < 1){
                pnotify_alert_from_top_center('数据为空', ajax_opts.type ? ajax_opts.type : 'GET' + " : " + ajax_opts.url);
                return callback()
            }
            callback(res.results)
          }
        });
      }

    }
}

function selectize_init_for_text(opts) {
    return {
        delimiter: ',',
        persist: false,
        create: function(input) {
            return {
                value: input,
                text: input
            }
        }
    }
}
