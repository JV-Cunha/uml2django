import {notifications_data} from "./stores/notificationsStore"
import {v4 as uuidv4 } from "./stores/notificationsStore"

export function addNotification(type: string, message:string){
    $notifications_data[uuidv4()] = {
        type,
        message
      };
}