<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import { notifications_data } from '$lib/stores/notificationsStore';
  import { Icon } from '@steeze-ui/svelte-icon';
  import { XCircle } from '@steeze-ui/heroicons';
  import { fly } from 'svelte/transition';

  interface Notification {
    uuid: { type: "success" | "error" | "info"; message: String };
  }
  export let notification_uuid: string,
    timeout = 4000;

   let notification = $notifications_data[notification_uuid];
   $: notification_class_type = 'alert-' + notification.type;
  console.log(notification_class_type);
  
   const dispatch = createEventDispatcher();
  function removeNotification() {
    dispatch('removeNotification', { notification_uuid });
  }
  onMount(() => {
    if (timeout > 0) {
      setTimeout(() => {
        removeNotification();
      }, timeout);
    }
  });
</script>

<div
  in:fly={{ x: 200, duration: 300 }}
  out:fly={{ x: 200, duration: 300 }}
  class="alert {notification_class_type} shadow-lg rounded-none mb-2 p-2"
>
  <div>
    <button
      on:click={() => removeNotification()}
      class="btn btn-sm btn-ghost btn-circle"
    >
      <Icon src={XCircle} size="24" />
    </button>
    <span>{notification.message}</span>
  </div>
</div>
