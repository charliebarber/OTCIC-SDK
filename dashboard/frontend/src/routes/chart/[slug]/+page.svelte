<script>
      export let data;
      import { fetchMetrics } from '../../../utils';
      import { Line } from 'svelte-chartjs';
      import { onMount } from 'svelte';
  
      import {
      Chart as ChartJS,
      Title,
      Tooltip,
      Legend,
      LineElement,
      LinearScale,
      PointElement,
      CategoryScale,
    } from 'chart.js';
  
    ChartJS.register(
      Title,
      Tooltip,
      Legend,
      LineElement,
      LinearScale,
      PointElement,
      CategoryScale
    );

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

<hgroup>
    <h2>{data.app.appName}</h2>
    <h4><strong>Language: </strong>{data.app.language}</h4>
    <a href="" role="button" on:click={handleReload}>Reload data</a>
</hgroup>

<div class=grid>
    <div>
        <span>CPU Usage</span>
        {#if cpu != {}}
        <Line 
            data={{
                labels: cpu.labels,
                datasets: [{
                    data: cpu.data,
                    label: 'CPU Usage %',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
                 }]
            }}
        />
        {:else}
        <span>Loading data...</span> 
        {/if}
    </div>

    <div>
        <span>RAM Usage</span>
        {#if ram != {}}
        <Line 
            data={{
                labels: ram.labels,
                datasets: [{
                    data: ram.data,
                    label: 'RAM Usage bytes',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
                }]
            }}
        />
        {:else}
        <span>Loading data...</span>
        {/if}
    </div>
</div>

<br>

<div class=grid>
    <div>
        <span>Disk I/O</span>
        {#if disk != {}}
        <Line 
            data={{
                labels: disk.labels,
                datasets: [{
                    data: disk.data,
                    label: 'Disk I/O bytes',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
                }]
            }}
        />
        {:else}
        <span>Loading data...</span>
        {/if}
    </div>

    <div>
        <span>GPU Usage</span>
        {#if gpu != {}}
        <Line 
            data={{
                labels: gpu.labels,
                datasets: [{
                    data: gpu.data,
                    label: 'GPU Usage %',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
                }]
            }}
        />
        {:else}
        <span>Loading data...</span>
        {/if}
    </div>

    <div>
        <span>VRAM Usage</span>
        {#if vram != {}}
        <Line 
            data={{
                labels: vram.labels,
                datasets: [{
                    data: vram.data,
                    label: 'VRAM Usage bytes',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
                }]
            }}
        />
        {:else}
        <span>Loading data...</span>
        {/if}
    </div>
</div>
