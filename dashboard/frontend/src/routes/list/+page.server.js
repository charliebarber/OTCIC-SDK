import { apps } from "../../data";
import { hyphenateStr } from "../../utils";

export async function load({ params }) {
    const res = await fetch('http://api:54321/api/apps')
    const apps = await res.json()

    return {
        apps: apps.applications.map((app) => ({
            name: app.appName,
            url: hyphenateStr(app.appName),
            language: app.language,
            score: "n/a",
            cpu: "n/a",
            ram: "n/a",
            disk: "n/a",
            gpu: "n/a"
        }))
    }
}