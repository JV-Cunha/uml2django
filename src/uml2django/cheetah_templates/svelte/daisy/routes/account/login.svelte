<script lang="ts">
  import { browserStorageSetAuthRefreshToken } from '$lib/browserStorage';
  import { goto } from '$app/navigation';
  import { BASE_API_URI } from '$lib/constants';
  import { notifications_data } from '$lib/stores/notificationsStore';
  import { onMount } from 'svelte';
  import { webuser_data } from '$lib/stores/webuserStore';
  import { addNotification } from '$lib/notifications';
  import { get as get_store_value } from 'svelte/store';
  if (webuser_data.email) {
    console.log(webuser_data.email);
    
  }
  let email = 'j@jjoao.com',
    password = '137Trimetl',
    form_errors = {};

  const handleLogin = async () => {
    // if (browserStorageGetAuthRefreshToken()) {
    //   localStorage.removeItem('refreshToken');
    // }
    const jsonRes = await fetch(`${BASE_API_URI}/auth/login`, {
      method: 'POST',
      body: JSON.stringify({
        email: email,
        password: password,
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    let json_response = await jsonRes.json();
    if (json_response.tokens) {
      webuser_data.set(json_response);
      console.log('refresh_token: ' + json_response.tokens.refresh);

      browserStorageSetAuthRefreshToken(json_response.tokens.refresh);
      //   success notification
      addNotification('success', 'Welcome back.');
      console.log(get_store_value(notifications_data));

      //   await goto('/');
    } else {
      form_errors = json_response;
      addNotification('error', 'Login Failed.');
    }
  };

  onMount(() => {});
</script>

<svelte:head>
  <title>Login</title>
</svelte:head>

<div class="flex-1 flex justify-center">
  <form on:submit|preventDefault={handleLogin}>
    <div class="flex flex-col mt-5">
      <h1 class="text-xl text-primary-focus">Access Your account</h1>
      <label class="label" for="id_email">
        <span class="label-text">Email</span>
      </label>
      <input
        id="id_email"
        type="text"
        placeholder=""
        class="bg-base-200 input input-sm input-bordered"
        class:input-error={form_errors.email}
        bind:value={email}
      />
      {#if form_errors.email}
        {#each form_errors.email as error_msg}
          <label class="label" for="id_password">
            <span class="label-text-alt text-error">{error_msg}</span>
          </label>
        {/each}
      {/if}
      <label class="label" for="id_password">
        <span class="label-text">Password</span>
      </label>
      <input
        id="id_password"
        type="password"
        bind:value={password}
        placeholder=""
        class="bg-base-200 input input-sm input-bordered"
        class:input-error={form_errors.password}
      />
      {#if form_errors.password}
        {#each form_errors.password as error_msg}
          <label class="label" for="id_password">
            <span class="label-text-alt text-error"
              >{form_errors.password[0]}</span
            >
          </label>
        {/each}
      {/if}
      <button type="submit" class="btn btn-accent my-4">Login</button>

      <h1 class="text-md text-base-content">Does not have an account?</h1>
      <a href="/accounts/signup" class="btn btn-primary my-4">Signup</a>
    </div>
  </form>
</div>
