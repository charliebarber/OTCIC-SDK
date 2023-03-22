<script>
	import { goto } from '$app/navigation';
	import { Modals, closeModal } from 'svelte-modals';
	export let data;

	function handleClick(e) {
		goto(e.target.href);
	}
</script>

<Modals>
	<div slot="backdrop" class="backdrop" on:click={closeModal} />
</Modals>

<details role="list">
	<summary aria-haspopup="listbox" role="button">Choose software</summary>
	<ul role="listbox">
		{#each data.apps as app}
			<li>
				<a rel="external" on:click={handleClick} href={app.url}>{app.name}</a>
			</li>
		{/each}
	</ul>
</details>

<slot />

<style>
	.backdrop {
		position: fixed;
		top: 0;
		bottom: 0;
		right: 0;
		left: 0;
		background: rgba(0, 0, 0, 0.5);
	}
</style>
