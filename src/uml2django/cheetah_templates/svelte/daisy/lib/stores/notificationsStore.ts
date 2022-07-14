import { writable } from 'svelte/store';

interface NotificationInterface {
    uuid: { type: "success" | "error" | "info"; message: String };
  }
export const notifications_data = writable<Notification>({});


