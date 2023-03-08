import { error } from '@sveltejs/kit';
import { hyphenateStr } from "../../../utils";

function getFormattedDate(value) {
    const date = new Date(value.time * 1000)
    return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
}

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

    const diskRes = await fetch(`http://api:54321/api/app/${params.slug}/disk/5m`)
    const diskData = await diskRes.json()

    const gpuRes = await fetch(`http://api:54321/api/app/${params.slug}/gpu/5m`)
    const gpuData = await gpuRes.json()

    const vramRes = await fetch(`http://api:54321/api/app/${params.slug}/vram/5m`)
    const vramData = await vramRes.json()

    console.log(cpuData)

    return { 
        app,
        cpu: {
            data: cpuData.values.map((value) => (value.val * 100)),
            labels: cpuData.values.map((value) => getFormattedDate(value))
        },
        ram: {
            data: ramData.values.map((value) => value.val),
            labels: ramData.values.map((value) => getFormattedDate(value))
        },
        disk: {
            data: diskData.values.map((value) => value.val),
            labels: diskData.values.map((value) => getFormattedDate(value))
        },
        gpu: {
            data: gpuData.values.map((value) => (value.val * 100)),
            labels: gpuData.values.map((value) => getFormattedDate(value))
        },
        vram: {
            data: vramData.values.map((value) => value.val),
            labels: vramData.values.map((value) => getFormattedDate(value))
        }
    };
  }