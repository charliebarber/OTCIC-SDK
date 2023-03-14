<script>
    export let data;
    import { fetchMetrics } from '../../../utils';
    import { onMount } from 'svelte';
    import MetricGraph from '$lib/MetricGraph.svelte';
  
    let cpu = {}
    let ram = {}
    let disk = {}
    let gpu = {}
    let vram = {}

    onMount(async () => {
        ({cpu, ram, disk, gpu, vram} = await fetchMetrics(data.slug));
        let interval = setInterval(async () => {
            ({cpu, ram, disk, gpu, vram} = await fetchMetrics(data.slug));
        }, 10000);

        return () => clearInterval(interval);
    })
    
  
    async function handleReload(event) {
        ({cpu, ram, disk, gpu, vram} = await fetchMetrics(data.slug));
    }
</script>

<div class="grid">
    <div>
        <hgroup>
            <h2>{data.app.appName}</h2>
            <h4><strong>Language: </strong>{data.app.language}</h4>
        </hgroup>
        <a href="" role="button" on:click={handleReload} class="outline">Reload data</a>
    </div>

    <div>
        <span><strong>Forecast Carbon Intensity: </strong>{data.carbonIntensity.forecast} gCO2/kWh</span>
        <br>
        <span><strong>Actual Carbon Intensity: </strong>{data.carbonIntensity.actual} gCO2/kWh</span>
    </div>
</div>

<br>

<div class=grid>
    <MetricGraph 
        label="CPU Usage %"
        metric={cpu}
    />

    <MetricGraph
        label="RAM Usage bytes"
        metric={ram}
    />
</div>

<br>

<div class=grid>
    <MetricGraph
        label-="Disk I/O bytes"
        metric={disk}
    />

    <MetricGraph
        label="GPU Usage %"
        metric={gpu}
    />

    <MetricGraph
        label="VRAM Usage bytes"
        metric={vram}
    />
</div>
