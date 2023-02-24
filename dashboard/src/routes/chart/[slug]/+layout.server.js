import { apps } from "../../../data";
import { hyphenateStr } from "../../../utils";

export async function load() {
    return {
        app: apps.map((app) => ({
                name: app.name,
                url: hyphenateStr(app.name)
        }))
    }
}