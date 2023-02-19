<script>
    export let data;
</script>

<details role="list">
    <summary aria-haspopup="listbox">Choose software</summary>
    <ul role="listbox">
        {#each data.appNames as appName}
            <li><a href={appName}>{appName}</a></li>
        {/each}
    </ul>
</details>

<slot />