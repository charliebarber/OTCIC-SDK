<script>
	import { lastApp } from '../stores';

	export let data;
</script>

<h1>Home</h1>

<p>
	OTCIC supports viewing in two different modes. List view allows all apps to be viewed at once.
	Chart view provides an in-depth view and provides graphs with live metrics. Click on an entry to
	see the corresponding charts.
</p>
<!-- 
<div class="grid">
    <div>
        <a rel='external' href="/list" role="button" style="width: 100%">List view</a>
    </div>

    <div>
        <a rel='external' href={`/chart/${$lastApp}`} role="button" style="width: 100%">Chart view</a>
    </div>
</div> -->

<h2>List view</h2>

<figure>
	<table>
		<thead>
			<th scope="col">#</th>
			<th scope="col">App</th>
			<th scope="col">SCI Score</th>
			<th scope="col">CPU %</th>
			<th scope="col">RAM MB</th>
			<th scope="col">Disk MB</th>
			<th scope="col">GPU %</th>
			<th scope="col">VRAM MB</th>
		</thead>

		<tbody>
			{#each data.apps as app, i}
				<tr>
					<th scope="row">{i + 1}</th>
					<td id={`${app.name}-appName`}><a href={`/chart/${app.url}`}>{app.name}</a></td>
					<td id={`${app.name}-score`}>{app.score}</td>
					<td id={`${app.name}-cpu`}>{app.cpu}</td>
					<td id={`${app.name}-ram`}>{app.ram}</td>
					<td id={`${app.name}-disk`}>{app.disk}</td>
					<td id={`${app.name}-disk`}>{app.gpu}</td>
					<td id={`${app.name}-disk`}>{app.vram}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</figure>

