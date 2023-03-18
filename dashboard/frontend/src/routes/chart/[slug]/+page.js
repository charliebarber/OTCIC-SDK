import { env } from '$env/dynamic/public';
import { browser } from '$app/environment'; 

const url = `http://${env.PUBLIC_URL || "localhost"}:54321`

export async function load({data}) {
//  const parent_data = await parent()

  if (browser) {
    const ciRes = await fetch(url + '/api/ci')
    const ci = await ciRes.json()
   return {
     ...data,
     carbonIntensity: ci
   }
  } else {
    const ciRes = await fetch('http://api:54321/api/ci')
    const ci = await ciRes.json()
    return {
      ...data,
      carbonIntensity: ci
    }
  }

}
