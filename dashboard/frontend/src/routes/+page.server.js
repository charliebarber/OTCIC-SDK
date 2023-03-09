import { hyphenateStr } from "../utils";

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
    const res = await fetch('http://api:54321/api/apps')
    const appsRes = await res.json()

    const apps = await Promise.all(appsRes.applications.map(async (app) => {
        const cpuRes = await fetch(`http://api:54321/api/app/${app.appName}/cpu/0m`)
        const cpuData = await cpuRes.json()

        console.log("cpuData", cpuData)
    
        const ramRes = await fetch(`http://api:54321/api/app/${app.appName}/ram/0m`)
        const ramData = await ramRes.json()
    
        const diskRes = await fetch(`http://api:54321/api/app/${app.appName}/disk/0m`)
        const diskData = await diskRes.json()
    
        const gpuRes = await fetch(`http://api:54321/api/app/${app.appName}/gpu/0m`)
        const gpuData = await gpuRes.json()
    
        const vramRes = await fetch(`http://api:54321/api/app/${app.appName}/vram/0m`)
        const vramData = await vramRes.json()

        return {
            name: app.appName,
            url: hyphenateStr(app.appName),
            languge: app.language,
            score: "n/a",
            cpu: cpuData.values[0].val,
            ram: ramData.values[0].val,
            disk: diskData.values[0].val,
            gpu: gpuData.values[0].val,
            vram: vramData.values[0].val,
        }
    }))
 

    return {
        apps
    }
}
