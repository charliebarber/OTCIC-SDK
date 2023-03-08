<script>
    import { lastApp } from '../stores';

    export let data;
</script>

<h1>Home</h1>

<p>
    OTCIC supports viewing in two different modes.
    List view allows all apps to be viewed at once. Chart view provides an in-depth view and provides graphs with live metrics.
    Click on an entry to see the corresponding charts.
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
            <th scope="col">RAM bytes</th>
            <th scope="col">Disk bytes</th>
            <th scope="col">GPU %</th>
            <th scope="col">VRAM bytes</th>
        </thead>

        <tbody>
            {#each data.apps as app, i}
                <tr>
                    <th scope="row">{i+1}</th>
                    <td><a href={`/chart/${app.url}`}>{app.name}</a></td>
                    <td>{app.score}</td>
                    <td>{app.cpu}</td>
                    <td>{app.ram}</td>
                    <td>{app.disk}</td>
                    <td>{app.gpu}</td>
                    <td>{app.vram}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</figure>