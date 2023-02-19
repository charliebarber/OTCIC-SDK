import { apps } from "../../../data";
import { error } from '@sveltejs/kit';

export async function load({ params }) {
    const app = apps.find((app) => app.name === params.slug);

    if (!app) throw error(404);

    return {
        app
    }
}