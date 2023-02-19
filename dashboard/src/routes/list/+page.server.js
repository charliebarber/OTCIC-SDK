import { apps } from "../../data";

export async function load({ params }) {
    return {
        apps: apps.map((app) => ({
            name: app.name,
            language: app.language,
            score: app.score,
            cpu: app.metrics.cpu,
            ram: app.metrics.ram,
            disk: app.metrics.disk,
            gpu: app.metrics.gpu
        }))
    }
}