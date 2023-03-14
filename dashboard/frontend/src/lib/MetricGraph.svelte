<script>
  export let metric;
  export let label;


  import { Line } from 'svelte-chartjs'
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

<div>
  <span>{label}</span>
  {#if metric != {}}
  <Line 
      data={{
          labels: metric.labels,
          datasets: [{
              data: metric.data,
              label: label,
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
