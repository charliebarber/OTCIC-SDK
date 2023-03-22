<script>
	export let score;
	export let handleOpen;
</script>

<div>
	<div class="scoreSpan">
		<strong>SCI Score:</strong>
		{#if score > 300}
			<button class="bad">{score}</button>
		{:else if score > 200}
			<button class="medium">{score}</button>
		{:else}
			<button class="good" on:click={handleOpen}>{score}</button>
		{/if}
	</div>
</div>

<style>
	.scoreSpan {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
		font-size: 1.5rem;
		margin-bottom: 0px;
	}

	button {
		font-size: 1.5rem;
		width: auto;
		margin-bottom: 0px;
	}

	.good {
		background-color: #40ff00;
	}

	.medium {
		background-color: #ffbf00;
	}

	.bad {
		background-color: #ff0040;
	}
</style>
