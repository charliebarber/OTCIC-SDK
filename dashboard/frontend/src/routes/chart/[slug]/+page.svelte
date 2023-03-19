<script>
    export let data;
    import { fetchMetrics } from '../../../utils';
    import { onMount } from 'svelte';
    import MetricGraph from '$lib/MetricGraph.svelte';
    import SCIScore from '$lib/SCIScore.svelte';

    console.log(data)
  
    let cpu = {}
    let ram = {}
    let disk = {}
    let gpu = {}
    let vram = {}
    let loadAvg = 0.0
    let sci = 0

    onMount(async () => {
        ({cpu, ram, disk, gpu, vram, loadAvg} = await fetchMetrics(data.slug));
        let interval = setInterval(async () => {
            ({cpu, ram, disk, gpu, vram, loadAvg, sci} = await fetchMetrics(data.slug));
        }, 10000);

        return () => clearInterval(interval);
    })
    
  
    async function handleReload(event) {
        ({cpu, ram, disk, gpu, vram, sci} = await fetchMetrics(data.slug));
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
        <br>
        <br>
        <span><strong>CPU model: </strong>{data.app.cpuModel}</span>
        <br>
        <span><strong>CPU TDP: </strong>{data.tdp} W</span>
        <br>
        <span><strong>CPU Load Avg: </strong>{loadAvg}</span>
    </div>
</div>

<br>

<SCIScore score={sci} />

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
        label="Disk I/O bytes"
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
