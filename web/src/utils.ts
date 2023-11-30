import { removeResource } from './api';
import { UserData } from './config';
import { items } from './states';

export function getCookie(name: string): string {
    var arr, reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)');
    if (arr = document.cookie.match(reg))
        return decodeURIComponent(arr[2]);
    else
        return '';
}

export function sortFunc(a: UserData, b: UserData): number {
    if (a.is_dir != b.is_dir) return a.is_dir ? -1 : 1
    return a.name.localeCompare(b.name)
}

export function remove  (data?: UserData) {
    const resources = data ? [data] : items.value.filter(e => e.selected)
    if (!resources.length) return
    const message = data ? `确定删除${data.name}?` : `确定删除选中的${resources.length}个资源?`
    const url = new URLSearchParams(location.search)
    const folder = url.get('path')

    ElMessageBox.confirm(message, '确认提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        removeResource(folder||'', resources.map(e => e.name)).then((res) => {
            items.value = res.sort(sortFunc)
            ElMessage.success('删除成功')
        })
    }).catch((e) => { console.log('取消删除:' + e) })
}