<script>
	import { goto } from "$app/navigation";
  export let data;

  function handleClick(e) {
    goto(e.target.href);
  }
</script>

<details role="list">
    <summary aria-haspopup="listbox" role="button">Choose software</summary>
    <ul role="listbox">
        {#each data.apps as app}
            <li>
                <a rel='external' on:click={handleClick} href={app.url}>{app.name}</a>
            </li>
        {/each}
    </ul>
</details>

<slot />
