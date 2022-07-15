import { writable } from 'svelte/store';

interface WebUser {
  email: string;
  tokens: {
    access: string;
    refresh: string;
  };
}

export const webuser_data = writable<WebUser>({
  email: '',
  tokens: {
    access: '',
    refresh: '',
  },
});
