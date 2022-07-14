import { writable } from "svelte/store";
interface WebUser {
        email: string
}
export const webuser_data = writable<WebUser>({email: ""})


