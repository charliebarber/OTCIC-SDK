import { error } from '@sveltejs/kit';
import { hyphenateStr, getFormattedDate, fetchMetrics } from "../../../utils";

/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    const res = await fetch('http://api:54321/api/apps')
    const apps = await res.json()
    const app = await apps.applications.find((app) => hyphenateStr(app.appName) === params.slug);

    if (!app) throw error(404); 

    const tdpRes = await fetch(`http://api:54321/api/tdp?cpuModel=${app.cpuModel}`)
    const tdp = await tdpRes.json()

    return { 
        app,
        tdp: tdp.tdp,
        slug: params.slug,
    };
  }
