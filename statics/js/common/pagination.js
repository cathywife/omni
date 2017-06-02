/**
 * Created by fmc on 16/11/2.
 */

function pagination_wrapper(options) {
    var dataSource = options.dataSource;
    var $pagination = options.pagination;

    var defaults = {
        displayedPages: options.displayedPages ? options.displayedPages : 5,
        cssStyle: options.cssStyle ? options.cssStyle : 'pagination pagination-sm',
        onInit: function () {

        },
        onPageClick: function (pageNumber, event) {
            $.ajax({
                url: dataSource,
                type: 'get',
                data: $.extend({}, {
                  'page': pageNumber,
                  'page-size': options.pageSize ? options.pageSize : 10
                }, options.dataSourceData),
                cache: false,
                error: function (response_obj, status, errorThrown) {
                    pnotify_alert_from_top_center('失败', '获取"' + dataSource + '"失败.')
                },
                success: function (data, textStatus, jqXHR) {
                    $pagination.pagination('destroy');
                    $pagination.pagination($.extend({}, defaults, {
                      pages: data.page_total,
                      currentPage: pageNumber
                    }));
                    options.callback(data.results)
                }
            });
        }
    };

    $pagination.pagination($.extend({}, defaults, options));
    $pagination.pagination('selectPage', 1)
}
