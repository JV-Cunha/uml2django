import { browser } from '$app/env';





export const browserStorageGet = (key: string): string | undefined => {
  if (browser) {
    const item = localStorage.getItem(key);
    if (item) {
      return item;
    }
  }
  return undefined;
};

export const browserStorageSet = (key: string, value: string): void => {
  if (browser) {
    localStorage.setItem(key, value);
  }
};

export const browserStorageGetAuthRefreshToken = () => {
    return browserStorageGet('auth_refresh');
}
export const browserStorageSetAuthRefreshToken = (token:string) => {
    return browserStorageSet('auth_refresh', token);
}

export const browserStorageGetAuthAccessToken = () => {
    return browserStorageGet('auth_access');
}
export const browserStorageSetAuthAccessToken = (token:string) => {
    return browserStorageSet('auth_access', token);
}
