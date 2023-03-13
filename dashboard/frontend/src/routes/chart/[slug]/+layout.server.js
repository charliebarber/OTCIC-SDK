import { apps } from "../../../data";
import { hyphenateStr } from "../../../utils";

export async function load() {
    const res = await fetch('http://api:54321/api/apps')
    const appsRes = await res.json()

    return {
        apps: appsRes.applications.map((app) => ({
            name: app.appName,
            url: hyphenateStr(app.appName),
        }))
    }
}
