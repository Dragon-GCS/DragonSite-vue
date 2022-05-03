export function breadcrumb(path: String): Array<[String, String]> {
    // concatenate the path to breadcrumb
    if (path == '/') {
        return [["Home", path]]
    } else {
        // not consider the ending '/'
        var breadcrumb: Array<[String, String]> = [['Home', '']];
        var path_array = path.split('/');
        for (var i = 1; i < path_array.length; i++) {
            breadcrumb.push([path_array[i], breadcrumb[i - 1][1] + '/' + path_array[i]]);
        }
        breadcrumb[0][1] = '/'
        return breadcrumb
    }
}

export function getIconUrl(icon: String, color: String = 'currentColor') {
    // https://icones.js.org/
    return `https://api.iconify.design/${icon}?color=${color}`
}