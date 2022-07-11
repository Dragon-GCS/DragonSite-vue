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

const getIconUrl = (icon: String) => {
    return `https://api.iconify.design/${icon}?color=currentColor`
}

export const menus: Array<Menu> = [
    { name: "公共网盘", logRequire: 'false', icon: getIconUrl("fxemoji:harddisk.svg") },
    { name: "个人网盘", logRequire: 'true', icon: getIconUrl("arcticons:password.svg") },
]
export const subMenus: Array<FileType> = [
    { name: "全部", icon: getIconUrl("flat-color-icons:database.svg"), type: "" },
    { name: "图片", icon: getIconUrl("vscode-icons:file-type-image.svg"), type: "image" },
    { name: "视频", icon: getIconUrl("vscode-icons:file-type-video.svg"), type: "video" },
    { name: "文档", icon: getIconUrl("emojione-v1:document-with-text.svg"), type: "document" },
    { name: "其他", icon: getIconUrl("flat-color-icons:answers.svg"), type: "other" },
]
export const siteName = "DragonSite"