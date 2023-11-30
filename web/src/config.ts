// http://www.fontawesome.com/
// https://icon-sets.iconify.design/
// https://www.aconvert.com/image/svg-to-png/
const getIconUrl = (icon: String) => {
    return `https://api.iconify.design/${icon}?color=currentColor`
}

// 一级目录名以及图标
export const menus: Array<Menu> = [
    { name: '公共网盘', personal: 'false', icon: getIconUrl('fxemoji:harddisk.svg') },
    { name: '个人网盘', personal: 'true', icon: getIconUrl('arcticons:password.svg') },
]
// 二级目录名以及图标
export const subMenus: Array<FileType> = [
    { name: '全部', icon: getIconUrl('flat-color-icons:database.svg'), type: '' },
    { name: '图片', icon: getIconUrl('vscode-icons:file-type-image.svg'), type: 'image' },
    { name: '视频', icon: getIconUrl('vscode-icons:file-type-video.svg'), type: 'video' },
    { name: '音频', icon: getIconUrl('vscode-icons:file-type-audio.svg'), type: 'audio' },
    { name: '文档', icon: getIconUrl('emojione-v1:document-with-text.svg'), type: 'document' },
    { name: '文本', icon: getIconUrl('vscode-icons:file-type-text.svg'), type: 'text' },
    { name: '其他', icon: getIconUrl('flat-color-icons:answers.svg'), type: 'other' },
]
// 左上角网站名称
export const siteName = 'DragonSite'
export const previewable = ['image', 'video'] // 可在线预览的文件类型

type Menu = {
    name: string;
    icon: string;
    personal: string;
}
type FileType = {
    name: string;
    icon: string;
    type: Category;
}
type Category = 'image' | 'video' | 'audio' | 'document' | 'text' | 'other' | ''

export interface UserData {
    id: string,
    is_dir: boolean,
    meta: { digest: string, size: number, category: Category } | null
    modified_time: string
    name: string
    parent: { id: string, name: string } | null
    size: string
    selected?: boolean
}
