import qs from 'qs';
import router from './router'
import { getCookie } from './utils';
import { UserData } from './config';
import { state } from './states';


const request = async (
    path: string,
    method: string,
    params?: any,
    body?: FormData | string
) => {
    if (params && !(params.path)) { delete params.path }
    const searchParams = new URLSearchParams(window.location.search)
    const personal = searchParams.get('personal') === 'true'

    const url = `${path}?${qs.stringify({ ...params, personal }, { arrayFormat: 'repeat' })}`;
    const headers = new Headers();
    if (method !== 'GET' && typeof body === 'string') {
        headers.append('Content-Type', 'application/json');
    }
    let resp = await fetch(url, { headers, method, body })

    const isJson = resp.headers.get('Content-Type')?.includes('application/json')
    if (resp.ok) { return isJson ? await resp.json() : resp }

    const detail = isJson ? (await resp.json()).detail : await resp.text() || resp.statusText

    ElMessage.error(detail);
    console.log(resp.status, resp.statusText);

    if (resp.status === 401) { router.push('/login') }
    else {router.push('/notfound')}
    return {}
}

export const loadResource = async (
    path: string,
    category: string
): Promise<UserData[]> => {
    return await request('/api/disk/resources', 'GET', { path, category })
}

export const removeResource = async (
    path: string,
    names: string[],
) => {
    return await request('/api/disk/resources', 'DELETE', { path, names })
}
export const renameResource = async (
    path: string,
    src: string,
    name: string,
): Promise<UserData[]> => {
    return await request(
        '/api/disk/resources',
        'PATCH',
        { path },
        JSON.stringify({ src: [src], names: [name] })
    )
}

export const createFolder = async (
    path: string,
    name: string,
): Promise<UserData[]> => {
    return await request('/api/disk/resources', 'POST', { path, name })
}

type Folder = { name: string, id: string, parent: { name: string, id: string }[] }
export const currentPaths = async () => {
    const searchParams = new URLSearchParams(window.location.search)
    const path = searchParams.get('path') || ''
    const folder: Folder = await request('/api/disk/item', 'GET', { path, parents: true })
    const paths = [{ name: folder.name, id: folder.id }]
    if (folder.parent instanceof Array) { paths.unshift(...folder.parent.reverse()) }
    paths[0].name = 'Home'
    return paths
}

export const downloadFile = async (
    filename: string,
    path: string,
) => {
    const res = await request('/api/disk/item', 'GET', { path, preview: false })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(await res.blob())
    a.style.display = 'none'
    a.setAttribute('download', filename)
    document.body.appendChild(a)
    a.click()
    URL.revokeObjectURL(a.href)
}

export const previewFile = async (
    path: string,
    thumbnail: boolean = false
): Promise<{ type: string, name: string, res: Blob }> => {
    const res = await request('/api/disk/item', 'GET', { path, preview: true, thumbnail })
    const name = res.headers.get('Content-Disposition')?.split('filename=')[1] || ''
    const type = res.headers.get('Content-Type')?.split('/')[0] || ''
    return { type, name, res: await res.blob() }
}

const loadState = () => {
    state.token = getCookie('token')
    state.username = getCookie('username')
    state.expiredTime = getCookie('expiredTime')
}

export const login = async (username: string, password: string) => {
    const form = new FormData()
    form.append('username', username)
    form.append('password', password)
    await request('/api/auth/login', 'POST', {}, form)
    loadState()
}

export const logout = async () => {
    console.log('logout');
    await request('/api/auth/logout', 'POST')
    loadState()
}