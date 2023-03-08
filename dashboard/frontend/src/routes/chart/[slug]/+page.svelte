<script>
    export let data;
    import { Line } from 'svelte-chartjs';

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
</script>

<hgroup>
    <h2>{data.app.appName}</h2>
    <h4><strong>Language: </strong>{data.app.language}</h4>
</hgroup>

<div class=grid>
    <div>
        <span>CPU Usage</span>
        <Line 
            data={{
                labels: data.cpu.labels,
                datasets: [{
                    data: data.cpu.data,
                    label: 'CPU Usage %',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
            }]
            }}
        />
    </div>

    <div>
        <span>RAM Usage</span>
        <Line 
            data={{
                labels: data.ram.labels,
                datasets: [{
                    data: data.ram.data,
                    label: 'RAM Usage bytes',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
            }]
            }}
        />
    </div>
</div>

<br>

<div class=grid>
    <div>
        <span>Disk I/O</span>
        <Line 
            data={{
                labels: data.disk.labels,
                datasets: [{
                    data: data.disk.data,
                    label: 'Disk I/O bytes',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
            }]
            }}
        />
    </div>

    <div>
        <span>GPU Usage</span>
        <Line 
            data={{
                labels: data.gpu.labels,
                datasets: [{
                    data: data.gpu.data,
                    label: 'GPU Usage %',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
            }]
            }}
        />
    </div>

    <div>
        <span>VRAM Usage</span>
        <Line 
            data={{
                labels: data.vram.labels,
                datasets: [{
                    data: data.vram.data,
                    label: 'VRAM Usage bytes',
                    fill: true,
                    backgroundColor: 'rgba(225, 204,230, .3)',
                    borderColor: 'rgb(205, 130, 158)',
                    pointBorderColor: 'rgb(205, 130,1 58)',
                    pointBackgroundColor: 'rgb(255, 255, 255)',
            }]
            }}
        />
    </div>
</div>