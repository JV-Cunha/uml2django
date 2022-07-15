import {notifications_data} from "./stores/notificationsStore"
import {v4 as uuidv4 } from "uuid"
import {get as get_store_value} from "svelte/store"
export function addNotification(type: string, message:string){
    let notifications = get_store_value(notifications_data)
    notifications[uuidv4()] = {
        type,
        message
      };
      notifications_data.set(notifications)
}