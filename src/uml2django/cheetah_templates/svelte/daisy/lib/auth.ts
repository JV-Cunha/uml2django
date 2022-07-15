import { get } from 'svelte/store';
import {
  browserStorageGetAuthRefreshToken,
  browserStorageSetAuthAccessToken,
  browserStorageSetAuthRefreshToken,
} from './browserStorage';
import { BASE_API_URI } from './constants';
import { webuser_data } from './stores/webuserStore';

export const refreshTokenIsValid = async (): Promise<boolean> => {
  const res = await fetch(`${BASE_API_URI}/auth/token/refresh`, {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      refresh: browserStorageGetAuthRefreshToken(),
    }),
  });

  let json_response = await res.json();
  let access_token = json_response['access'];
  //   let refresh_token = json_response['refresh'];
  if (access_token !== undefined) {
    browserStorageSetAuthAccessToken(access_token);
    let webuser = get(webuser_data);
    webuser.email = 'xx';
    webuser_data.set(webuser);
    return true;
  }
  return false;
};
