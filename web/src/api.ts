import axios from "axios"
import { UserData, loginState, username as user } from "./config"

export const get_tokens = () => {
    return {
        token: localStorage.getItem("token") || "",
        username: localStorage.getItem("username") || "",
        expired_time: localStorage.getItem("expired_time") || 0
    }
}

export const loadResource = async (
    path: string,
    login_require: boolean,
    category: string) => {
    return axios.get("/api/disk", {
        params: { path, login_require, category },
        headers: get_tokens()
    }).then((res) => {
        return res
    }, (err) => {
        console.log("err", err)
        return err
    })
}

export const removeResource = async (
    path: string,
    name: string[],
    is_dir: boolean[],
    login_require: boolean,
) => {
    return axios.delete("/api/disk", {
        params: { path, login_require, name, is_dir },
        headers: get_tokens()

    }).then((res) => {
        return res
    }).catch((err) => {
        return err
    })
}

export const createFolder = async (
    path: string,
    name: string,
    login_require: boolean): Promise<UserData[]> => {
    return axios.post(`/api/disk`, {}, {
        params: {
            path: path,
            name: name,
            login_require: login_require
        },
        headers: get_tokens()
    }).then((res) => {
        return res.data
    })
}

export const downloadFile = (full_path: string, login_require: boolean = false) => {
    window.open(`/api/disk/download?path=${full_path}&preview=false&login_require=${login_require}`, "_self")
}

export const previewFile = (full_path: string, login_require: boolean = false) => {
    return axios.get("/api/disk/download", {
        params: { path: full_path, preview: true, login_require },
        headers: get_tokens()
    }).then((res) => {
        return res.data
    })
}

export const renameResource = (path: string, target: string, is_dir: boolean, login_require: boolean) => {
    return axios.patch("/api/disk", {}, {
        params: { path, target, is_dir, login_require },
        headers: get_tokens()
    }).then((res) => {
        return res.data
    })
}

export const login = (username: string, password: string) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    return axios.post(
        "/api/auth/login",
        params,
    ).then((res) => {
        if (res.status === 200) {
            localStorage.setItem("token", res.data.token)
            localStorage.setItem("username", res.data.username)
            localStorage.setItem("expired_time", res.data.expired_time)
            loginState.value = true
            user.value = res.data.username
            return true
        }
    })
}

export const logout = () => {
    // return axios.post("/api/auth/logout").then((res) => {
    //     if res.
    //     return res
    // })
    localStorage.removeItem("token")
    localStorage.removeItem("username")
    localStorage.removeItem("expired_time")
    loginState.value = false
    user.value = ""
}