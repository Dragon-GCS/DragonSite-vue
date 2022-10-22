import { ref } from 'vue'

type Menu = {
    name: string;
    icon: string;
    logRequire: string;
}
type FileType = {
    name: string;
    icon: string;
    type: string;
}

// http://www.fontawesome.com/
// https://icon-sets.iconify.design/
// https://www.aconvert.com/image/svg-to-png/
const getIconUrl = (icon: String) => {
    return `https://api.iconify.design/${icon}?color=currentColor`
}

// 一级目录名以及图标
export const menus: Array<Menu> = [
    { name: "公共网盘", logRequire: 'false', icon: getIconUrl("fxemoji:harddisk.svg") },
    { name: "个人网盘", logRequire: 'true', icon: getIconUrl("arcticons:password.svg") },
]
// 二级目录名以及图标
export const subMenus: Array<FileType> = [
    { name: "全部", icon: getIconUrl("flat-color-icons:database.svg"), type: "" },
    { name: "图片", icon: getIconUrl("vscode-icons:file-type-image.svg"), type: "image" },
    { name: "视频", icon: getIconUrl("vscode-icons:file-type-video.svg"), type: "video" },
    { name: "音频", icon: getIconUrl("vscode-icons:file-type-audio.svg"), type: "audio" },
    { name: "文档", icon: getIconUrl("emojione-v1:document-with-text.svg"), type: "document" },
    { name: "文本", icon: getIconUrl("vscode-icons:file-type-text.svg"), type: "text" },
    { name: "其他", icon: getIconUrl("flat-color-icons:answers.svg"), type: "other" },
]
// 左上角网站名称
export const siteName = "DragonSite"

export const username = ref(localStorage.getItem("username") || "")
export const token = ref(localStorage.getItem("token") || "")
export const expiredTime = ref(localStorage.getItem("expired_time") || "")
export const loginState = ref(false || username.value !== "")

export const previewable = ["image", "video"] // 可在线预览的文件类型
export const items = ref<UserData[]>([])

export interface UserData {
    path: string,
    name: string,
    is_dir: boolean,
    category: string,
    create_time: Date,
    size: number,
    modified_time: Date,
    digest: string,
    mime_type: string,
    parent_path: string
    select?: boolean
}