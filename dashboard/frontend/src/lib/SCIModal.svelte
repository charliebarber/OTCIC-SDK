<script>
	import { closeModal } from 'svelte-modals';

	// provided by <Modals />
	export let isOpen;

	export let sci;
</script>

{#if isOpen}
	<div role="dialog" class="modal">
		<article>
			<header>SCI Score Breakdown</header>
			<p>
				<strong>CPU:</strong>
				{sci.cpu.cores} cores * {sci.cpu.tdp} W (TDP) * Log({sci.cpu.loadAvg} (load average) * 100) /
				Log(200) = <strong>{sci.cpu.score}</strong>
			</p>
			<p>
				<strong>RAM:</strong> 0.3725 W/GB * {sci.memory.average / 1024.0} GB (average memory use) =
				<strong>{sci.memory.score}</strong>
			</p>
			<p>
				<strong>Disk:</strong> 0.65 * {sci.disk.average / 1024.0} GB (average disk use) =
				<strong>{sci.disk.score}</strong>
			</p>
			<br /><br />
			<p><strong>Total of above scores: {sci.score}</strong></p>
		</article>
	</div>
{/if}

<style>
	.modal {
		position: fixed;
		top: 0;
		bottom: 0;
		right: 0;
		left: 0;
		display: flex;
		justify-content: center;
		align-items: center;

		/* allow click-through to backdrop */
		pointer-events: none;
	}
</style>
