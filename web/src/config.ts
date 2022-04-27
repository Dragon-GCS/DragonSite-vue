type Menu = {
    name: string;
    icon: string;
    logRequire: string;
}
type Cate = {
    name: string;
    icon: string;
    by: string;
}
export const subMenus: Array<Menu> = [
    { name: "公共网盘", icon: "fxemoji:harddisk.svg", logRequire: 'false' },
    { name: "个人网盘", icon: "arcticons:password.svg", logRequire: 'true' },
]
export const cates: Array<Cate> = [
    { name: "全部", icon: "flat-color-icons:database.svg", by: "" },
    { name: "图片", icon: "vscode-icons:file-type-image.svg", by: "image" },
    { name: "视频", icon: "vscode-icons:file-type-video.svg", by: "video" },
    { name: "文档", icon: "emojione-v1:document-with-text.svg", by: "document" },
    { name: "其他", icon: "flat-color-icons:answers.svg", by: "other" },
]