import { UserData } from './config';
import { getCookie } from './utils';

export const state = reactive({
    username: getCookie('username'),
    token: getCookie('token'),
    expiredTime: getCookie('expiredTime'),
});

export const items = ref<UserData[]>([]);
export const paths = ref<{ id: string, name: string }[]>([])
