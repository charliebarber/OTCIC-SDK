import { apps } from "../../../data";
import { error } from '@sveltejs/kit';
import { hyphenateStr } from "../../../utils";

export async function load({ params }) {
    const app = apps.find((app) => hyphenateStr(app.name) === params.slug);

    if (!app) throw error(404);

    return {
        app
    }
}