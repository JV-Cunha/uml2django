<script lang="ts">
  import { notifications_data } from '$lib/stores/notificationsStore';
  import NotificationAlert from './NotificationAlert.svelte';
  
  function removeNotification(event: any) {
    console.log(`'removeNotification' ${event.detail.notification_uuid}`);
    delete $notifications_data[event.detail.notification_uuid];
    $notifications_data = $notifications_data
    // if ($notifications_data.length ==1) {
    // $notifications_data = []
    // }
    // $notifications_data.splice(event.detail.index, 1);
    // $notifications_data = $notifications_data;

    // $notifications_data = $notifications_data.filter( value =>  $notifications_data.indexOf(value) != event.detail.index )
    console.log($notifications_data);
  }
</script>

{#if Object.keys($notifications_data).length > 0}
  <!-- content here -->
  <div class="notifications-container flex flex-col max-w-sm">
    {#each Object.keys($notifications_data) as notification_uuid (notification_uuid)}
      <NotificationAlert
        on:removeNotification={removeNotification}
        {notification_uuid}
      />
    {/each}
  </div>
{/if}

<style>
  .notifications-container {
    width: fit-content;
    height: 40px;
    right: 0;
    top: 70px;
    position: fixed;
    line-height: 2;
    z-index: 999;
  }
</style>
