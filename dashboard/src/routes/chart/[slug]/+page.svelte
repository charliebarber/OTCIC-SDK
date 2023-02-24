<script>
    export let data;
    import { Line } from 'svelte-chartjs';
</script>

<hgroup>
    <h2>{data.app.name}</h2>
    <h4><strong>Language: </strong>{data.app.language}</h4>
</hgroup>

<div class=grid>
    <div>
        <span>CPU Usage</span>

        <Line data={data.app.metrics.cpu} />
    </div>

    <div>
        <span>RAM Usage</span>
    </div>
</div>

<br>

<div class=grid>
    <div>
        <span>Disk Usage</span>
    </div>

    <div>
        <span>GPU Usage</span>
    </div>
</div>