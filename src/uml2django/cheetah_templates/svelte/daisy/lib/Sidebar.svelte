<script>
    import SidebarMenuTitle from "./SidebarMenuTitle.svelte"
	import SidebarMenuItem from './SidebarMenuItem.svelte';
    export let is_sidebar_open;
</script>

<div class="drawer-side">
      <label for="my-drawer-2" class="drawer-overlay"></label> 
      <ul id="menu-list" class="menu  menu-compact overflow-y-auto bg-base-200 ">
        #for $app_name in $apps_and_its_models:
        <SidebarMenuTitle>$app_name.capitalize</SidebarMenuTitle>
        #for $model in $apps_and_its_models[$app_name]:
        <SidebarMenuItem href="/$model.app_name/$model.name_lower/list">$model.name</SidebarMenuItem>
        #end for
        #end for
      </ul>
    
    </div>

<style>
#menu-list {
    max-width: fit-content;
}
</style>