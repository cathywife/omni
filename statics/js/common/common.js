/**
 * Created by fmc on 16/10/8.
 */
function isArrayFn(value){
    if (typeof Array.isArray === "function") {
        return Array.isArray(value);
    } else {
        return Object.prototype.toString.call(value) === "[object Array]";
    }
}

