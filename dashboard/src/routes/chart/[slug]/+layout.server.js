import { apps } from "../../../data";

export async function load() {
    return {
        appNames: apps.map((app) => app.name)
    }
}