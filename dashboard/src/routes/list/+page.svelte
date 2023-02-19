<script>
    export let data;
</script>

<h1>List view</h1>

<figure>
    <table>
        <thead>
            <th scope="col">#</th>
            <th scope="col">App</th>
            <th scope="col">SCI Score</th>
            <th scope="col">CPU %</th>
            <th scope="col">RAM %</th>
            <th scope="col">Disk %</th>
            <th scope="col">GPU %</th>
        </thead>

        <tbody>
            {#each data.apps as app, i}
                <tr>
                    <th scope="row">{i+1}</th>
                    <td>{app.name}</td>
                    <td>{app.score}</td>
                    <td>{app.cpu}</td>
                    <td>{app.ram}</td>
                    <td>{app.disk}</td>
                    <td>{app.gpu}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</figure>