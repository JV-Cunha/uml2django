<script lang="ts">
  import { Icon } from '@steeze-ui/svelte-icon';
  import { User } from '@steeze-ui/heroicons';

</script>

<div class="dropdown dropdown-end">
  <span tabindex="0" class="btn btn-ghost btn-circle avatar">
    <Icon src={User} size="24" />
  </span>
  <ul
    tabindex="0"
    class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
  >
    <li>
      <a href="/" class="justify-between">
        Profile
        <span class="badge">New</span>
      </a>
    </li>
    <li><a href="/">Settings</a></li>
    <li><a href="/">Logout</a></li>
  </ul>
</div>
