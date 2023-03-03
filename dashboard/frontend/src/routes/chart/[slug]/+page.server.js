import { error } from '@sveltejs/kit';
import { hyphenateStr } from "../../../utils";

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    const res = await fetch('http://api:54321/api/apps')
    const apps = await res.json()
    const app = await apps.applications.find((app) => hyphenateStr(app.appName) === params.slug);

    if (!app) throw error(404); 

    const cpuRes = await fetch(`http://api:54321/api/app/${params.slug}/cpu/5m`)
    const cpuData = await cpuRes.json()

    const ramRes = await fetch(`http://api:54321/api/app/${params.slug}/ram/5m`)
    const ramData = await ramRes.json()

    console.log(cpuData)

    return { 
        app,
        cpu: {
            datasets: [{
                data: cpuData.values.map((value) => [value.time, value.val])
            }],
            labels: ['Time', 'CPU measure']
        },
        ram: {
            datasets: [{
                data: ramData.values.map((value) => [value.time, value.val])
            }],
            labels: ['Time', 'RAM Used']
        }
    };
  }