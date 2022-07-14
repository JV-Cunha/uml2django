<script lang="ts">
  import { browserStorageGet, browserStorageSet } from '$lib/browserStorage';
  import { goto } from '$app/navigation';
  import { BASE_API_URI } from '$lib/constants';
  import { notifications_data } from '$lib/stores/notificationsStore';
  import { onMount } from 'svelte';
  import { webuser_data } from '$lib/stores/webuserStore';
  let email = 'j@jjoao.com',
    password = '137Trimetl',
    password_confirmation = '137Trimetl',
    form_errors = {};
  let password_confirmation_error_msg = 'Passwords are not the same.';

  $: {
    if (password != password_confirmation) {
      form_errors.password_confirmation = [password_confirmation_error_msg];
      form_errors.password = [password_confirmation_error_msg];
    } else {
    }
  }

  const handleSignup = async () => {
    if (browserStorageGet('refreshToken')) {
      localStorage.removeItem('refreshToken');
    }
    const jsonRes = await fetch(`${BASE_API_URI}/auth/signup`, {
      method: 'POST',
      body: JSON.stringify({
        email: email,
        password: password,
        password_confirmation: password_confirmation,
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    let response_status_code = await jsonRes.status;
    let json_response = await jsonRes.json();
    if (response_status_code == 201) {
      webuser_data.set(json_response);
      console.log('logged in');
    } else {
      console.log(json_response);
      form_errors = json_response;
      console.log(json_response.non_field_errors);
    }
  };

  onMount(() => {});
</script>

<svelte:head>
  <title>Signup</title>
</svelte:head>

<div class="flex-1 flex justify-center">
  <form on:submit|preventDefault={handleSignup}>
    <div class="flex flex-col mt-5">
      <h1 class="text-xl text-primary-focus">Create Your account</h1>
      <div>
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
      </div>

      <div>
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
              <span class="label-text-alt text-error">{error_msg}</span>
            </label>
          {/each}
        {/if}
      </div>

      <div>
        <label class="label" for="id_password_confirmation">
          <span class="label-text">Password Confirmation</span>
        </label>
        <input
          id="id_password_confirmation"
          type="password"
          bind:value={password_confirmation}
          placeholder=""
          class="bg-base-200 input input-sm input-bordered"
          class:input-error={form_errors.password_confirmation}
        />
        {#if form_errors.password_confirmation}
          {#each form_errors.password_confirmation as error_msg}
            <label class="label" for="id_password">
              <span class="label-text-alt text-error">{error_msg}</span>
            </label>
          {/each}
        {/if}
      </div>
      <button type="submit" class="btn btn-primary my-4">Signup</button>

      <h1 class="text-md text-base-content">Already have an account?</h1>
      <a href="/accounts/signup" class="btn btn-accent my-4">Login</a>
    </div>
  </form>
</div>
