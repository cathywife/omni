/**
 * Created by fmc on 16/10/4.
 */

function product_select2_data_func(params) {
    return {
      search: {'name': params.term},
      page: params.page
    };
}