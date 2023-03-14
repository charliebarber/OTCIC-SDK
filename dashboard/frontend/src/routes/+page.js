// import { hyphenateStr } from "../utils";

// /** @type {import('./$types').PageLoad} */
// export async function load({ params }) {
//     const res = await fetch('http://api:54321/api/apps')
//     const appsRes = await res.json()
//     console.log("APPS", appsRes)

//     return {
//         apps: appsRes.applications.map((app) => ({
//             name: app.appName,
//             url: hyphenateStr(app.appName),
//             language: app.language,
//             score: "n/a",
//             cpu: "n/a",
//             ram: "n/a",
//             disk: "n/a",
//             gpu: "n/a"
//         }))
//     }
// }