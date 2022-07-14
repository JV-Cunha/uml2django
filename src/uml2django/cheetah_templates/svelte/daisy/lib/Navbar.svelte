<script lang="ts">
  import { Icon } from '@steeze-ui/svelte-icon';
  import { X, MenuAlt1, ShoppingCart, Search } from '@steeze-ui/heroicons';
  import { webuser_data } from './stores/webuserStore';
  import NavbarUserDropdown from './NavbarUserDropdown.svelte';
  import { refreshTokenIsValid } from './auth';
  export let is_sidebar_open: any;
  
</script>

<div class="navbar bg-base-300">
  <div class="navbar-start">
    <div class="dropdown">
      <label for="my-drawer-2" class="btn btn-ghost lg:hidden">
        <Icon
          class={is_sidebar_open ? 'text-error' : 'text-primary-focus'}
          src={is_sidebar_open ? X : MenuAlt1}
          size="24"
        />
      </label>

      <ul
        tabindex="0"
        class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
      />
    </div>
    <a href="https://daisyui.com/" class="btn btn-ghost normal-case text-xl"
      >daisyUI</a
    >
  </div>
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal p-0" />
  </div>
  <div class="navbar-end">
    <button class="btn btn-ghost btn-circle">
      <Icon src={Search} size="24" />
    </button>
    <div class="dropdown dropdown-end">
      <span tabindex="0" class="btn btn-ghost btn-circle">
        <div class="indicator">
          <Icon src={ShoppingCart} size="24" />
          <span class="badge badge-sm indicator-item">8</span>
        </div>
      </span>
      <div
        tabindex="0"
        class="mt-3 card card-compact dropdown-content w-52 bg-base-100 shadow"
      >
        <div class="card-body">
          <span class="font-bold text-lg">8 Items</span>
          <span class="text-info">Subtotal: $999</span>
          <div class="card-actions">
            <button class="btn btn-primary btn-block">View cart</button>
          </div>
        </div>
      </div>
    </div>

    {#await refreshTokenIsValid()}
      <button class="btn btn-ghost text-info loading" />
    {:then}
      {#if $webuser_data.email}
        <NavbarUserDropdown />
      {:else}
        <a href="/account/login" class="btn btn-accent ml-3">Login </a>
        <a href="/account/signup" class="btn btn-primary ml-3">Signup </a>
      {/if}
    {/await}
  </div>
</div>
