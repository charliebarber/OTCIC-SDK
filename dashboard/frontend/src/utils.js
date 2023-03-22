import { env } from '$env/dynamic/public';

export function hyphenateStr(str) {
    return str.replace(/ +/g, '-').toLowerCase();
}

export function getFormattedDate(value) {
    const date = new Date(value.time * 1000)
    return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds()
}

const url = `http://${env.PUBLIC_URL || "localhost"}:54321`

export async function fetchMetrics(appName) {
    const cpuRes = await fetch(`${url}/api/app/${appName}/cpu/5m`)
    const cpuData = await cpuRes.json()

    const ramRes = await fetch(`${url}/api/app/${appName}/ram/5m`)
    const ramData = await ramRes.json()

    const diskRes = await fetch(`${url}/api/app/${appName}/disk/5m`)
    const diskData = await diskRes.json()

    const gpuRes = await fetch(`${url}/api/app/${appName}/gpu/5m`)
    const gpuData = await gpuRes.json()

    const vramRes = await fetch(`${url}/api/app/${appName}/vram/5m`)
    const vramData = await vramRes.json()

    const loadAvgRes = await fetch(`${url}/api/loadAvg?appName=${appName}`)
    const loadAvgData = await loadAvgRes.json()

    const sciRes = await fetch(`${url}/api/sciScore?appName=${appName}`)
    const sci = await sciRes.json()

    return { 
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
        },
        loadAvg: loadAvgData.loadAvg,
        sci: sci.sciScore,
    }
}
