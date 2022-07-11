export function breadcrumb(path: string): Array<[string, string]> {
    // concatenate the path to breadcrumb
    if (path == '/') {
        return [["Home", path]]
    } else {
        // not consider the ending '/'
        var breadcrumb: [string, string][]= [['Home', '']];
        var path_array = path.split('/');
        for (var i = 1; i < path_array.length; i++) {
            breadcrumb.push([path_array[i], breadcrumb[i - 1][1] + '/' + path_array[i]]);
        }
        breadcrumb[0][1] = '/'
        return breadcrumb
    }
}