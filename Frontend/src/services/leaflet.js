const LEAFLET_VERSION = '1.9.4'
const LEAFLET_CSS_ID = 'clubeon-leaflet-css'
const LEAFLET_SCRIPT_ID = 'clubeon-leaflet-script'

export function loadLeaflet() {
  if (window.L) return Promise.resolve(window.L)

  if (window.__clubeonLeafletPromise) {
    return window.__clubeonLeafletPromise
  }

  window.__clubeonLeafletPromise = new Promise((resolve, reject) => {
    if (!document.getElementById(LEAFLET_CSS_ID)) {
      const link = document.createElement('link')
      link.id = LEAFLET_CSS_ID
      link.rel = 'stylesheet'
      link.href = `https://unpkg.com/leaflet@${LEAFLET_VERSION}/dist/leaflet.css`
      link.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY='
      link.crossOrigin = ''
      document.head.appendChild(link)
    }

    const existing = document.getElementById(LEAFLET_SCRIPT_ID)
    if (existing) {
      existing.addEventListener('load', () => resolve(window.L), { once: true })
      existing.addEventListener('error', reject, { once: true })
      return
    }

    const script = document.createElement('script')
    script.id = LEAFLET_SCRIPT_ID
    script.src = `https://unpkg.com/leaflet@${LEAFLET_VERSION}/dist/leaflet.js`
    script.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo='
    script.crossOrigin = ''
    script.onload = () => resolve(window.L)
    script.onerror = () => reject(new Error('Unable to load the map library.'))
    document.head.appendChild(script)
  })

  return window.__clubeonLeafletPromise
}

const CACHE_KEY = 'clubeon:club-geocodes:v1'

export const BANGALORE_FALLBACK_GEOCODES = {
  '10, Field Marshal Cariappa Rd, Shanthala Nagar, Ashok Nagar, Bengaluru, Karnataka 560025': {
    lat: 12.9698,
    lng: 77.5986,
    displayName: 'Bangalore Club, Ashok Nagar, Bengaluru, Karnataka',
  },
  'St Mark\'s Rd, Shantala Nagar, Ashok Nagar, Bengaluru, Karnataka 560001': {
    lat: 12.9734,
    lng: 77.6041,
    displayName: 'Bowring Institute, St Mark\'s Rd, Bengaluru, Karnataka',
  },
  'Cubbon Road, Shivaji Nagar, Bengaluru, Karnataka 560001': {
    lat: 12.9788,
    lng: 77.5996,
    displayName: 'KSCA Club / Chinnaswamy Stadium, Shivaji Nagar, Bengaluru, Karnataka',
  },
  'Survey No 336, Bettahalasuru Jala Hobli, Yelahanka Taluk, Bengaluru, Karnataka 562157': {
    lat: 13.1783,
    lng: 77.6358,
    displayName: 'Padukone - Dravid Centre for Sports Excellence (CSE), Yelahanka, Bengaluru, Karnataka',
  },
  '6th Cross, 6th Block, Koramangala, Bengaluru, Karnataka 560095': {
    lat: 12.9345,
    lng: 77.6200,
    displayName: 'The Koramangala Club, 6th Block, Koramangala, Bengaluru, Karnataka',
  },
  '9th Main Road, 4th Cross, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka 560008': {
    lat: 12.9676,
    lng: 77.6432,
    displayName: 'Indiranagar Club, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka',
  },
  'Sarjapur Main Road, Central Jail Road, Kasavanahalli, Bengaluru, Karnataka 560035': {
    lat: 12.8988,
    lng: 77.6744,
    displayName: 'Play Arena Sports Complex, Kasavanahalli, Sarjapur Road, Bengaluru, Karnataka',
  },
  'ITPL Main Road, Whitefield, Bengaluru, Karnataka 560066': {
    lat: 12.9856,
    lng: 77.7289,
    displayName: 'Whitefield Sports Arena, ITPL Main Road, Bengaluru, Karnataka',
  },
}

function readCache() {
  try {
    return JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
  } catch {
    return {}
  }
}

function writeCache(cache) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify(cache))
  } catch {
    // Storage can be unavailable in private/restricted browser contexts.
  }
}

export async function geocodeClubAddress(address) {
  const normalized = String(address || '').trim()
  if (!normalized) return null

  // 1. Check Bangalore hardcoded real geocodes for instant high-fidelity resolution
  if (BANGALORE_FALLBACK_GEOCODES[normalized]) {
    return BANGALORE_FALLBACK_GEOCODES[normalized]
  }

  // Also check if normalized address includes known club names
  for (const [key, point] of Object.entries(BANGALORE_FALLBACK_GEOCODES)) {
    if (normalized.toLowerCase().includes('ksca') || normalized.toLowerCase().includes('chinnaswamy')) {
      if (key.includes('Cubbon Road')) return point
    }
    if (normalized.toLowerCase().includes('dravid') || normalized.toLowerCase().includes('padukone') || normalized.toLowerCase().includes('centre for sports excellence')) {
      if (key.includes('Bettahalasuru')) return point
    }
    if (normalized.toLowerCase().includes('koramangala')) {
      if (key.includes('Koramangala')) return point
    }
    if (normalized.toLowerCase().includes('indiranagar')) {
      if (key.includes('Indiranagar')) return point
    }
    if (normalized.toLowerCase().includes('play arena') || normalized.toLowerCase().includes('kasavanahalli')) {
      if (key.includes('Sarjapur')) return point
    }
    if (normalized.toLowerCase().includes('bangalore club')) {
      if (key.includes('Cariappa')) return point
    }
  }

  // 2. Check local storage cache
  const cache = readCache()
  if (cache[normalized]) return cache[normalized]

  // 3. Fallback to OpenStreetMap Nominatim
  try {
    const url = new URL('https://nominatim.openstreetmap.org/search')
    url.searchParams.set('format', 'jsonv2')
    url.searchParams.set('limit', '1')
    url.searchParams.set('q', normalized)

    const response = await fetch(url.toString(), {
      headers: {
        Accept: 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Geocoding failed with status ${response.status}.`)
    }

    const results = await response.json()
    const first = results?.[0]
    if (!first) return null

    const point = {
      lat: Number(first.lat),
      lng: Number(first.lon),
      displayName: first.display_name || normalized,
    }

    cache[normalized] = point
    writeCache(cache)
    return point
  } catch (err) {
    console.warn('Geocoding request failed:', err)
    return null
  }
}

export async function searchPlaces(query) {
  const normalized = String(query || '').trim()
  if (!normalized || normalized.length < 2) return []

  try {
    const url = new URL('https://nominatim.openstreetmap.org/search')
    url.searchParams.set('format', 'jsonv2')
    url.searchParams.set('limit', '5')
    url.searchParams.set('q', `${normalized}, Bengaluru, Karnataka, India`)

    const response = await fetch(url.toString(), {
      headers: {
        Accept: 'application/json',
      },
    })

    if (!response.ok) return []
    const results = await response.json()
    return (results || []).map((item) => ({
      lat: Number(item.lat),
      lng: Number(item.lon),
      displayName: item.display_name,
      type: item.type,
    }))
  } catch {
    return []
  }
}

export function getCurrentPosition(options = {}) {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Location services are not supported by this browser.'))
      return
    }

    navigator.geolocation.getCurrentPosition(resolve, reject, {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0,
      ...options,
    })
  })
}

export function distanceInKm(lat1, lng1, lat2, lng2) {
  const earthRadiusKm = 6371
  const toRadians = (value) => (value * Math.PI) / 180
  const dLat = toRadians(lat2 - lat1)
  const dLng = toRadians(lng2 - lng1)
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRadians(lat1)) *
      Math.cos(toRadians(lat2)) *
      Math.sin(dLng / 2) ** 2
  return earthRadiusKm * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

export async function fetchRoute(startLat, startLng, endLat, endLng, profile = 'driving') {
  const osrmProfile = profile === 'walking' ? 'foot' : 'driving'
  const url = `https://router.project-osrm.org/route/v1/${osrmProfile}/${startLng},${startLat};${endLng},${endLat}?overview=full&geometries=geojson&steps=true`

  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`Routing service returned status ${response.status}`)
    }

    const data = await response.json()
    if (!data.routes || !data.routes.length) {
      throw new Error('No road route found between these locations.')
    }

    const route = data.routes[0]
    // GeoJSON coordinates are [longitude, latitude], Leaflet polyline expects [latitude, longitude]
    const coordinates = route.geometry.coordinates.map(([lng, lat]) => [lat, lng])
    const distanceKm = route.distance / 1000
    const durationMin = Math.round(route.duration / 60)

    const steps = (route.legs?.[0]?.steps || []).map((step, idx) => {
      const maneuver = step.maneuver || {}
      const stepDistMeters = Math.round(step.distance)
      const stepDistText =
        stepDistMeters >= 1000
          ? `${(stepDistMeters / 1000).toFixed(1)} km`
          : `${stepDistMeters} m`

      let instruction
      const street = step.name ? ` onto ${step.name}` : ''

      switch (maneuver.type) {
        case 'depart':
          instruction = `Head ${maneuver.modifier || 'out'} on ${step.name || 'the road'}`.trim()
          break
        case 'arrive':
          instruction = 'Arrive at your sports venue destination'
          break
        case 'turn':
          instruction = `Turn ${maneuver.modifier || 'onto'}${street}`
          break
        case 'new name':
        case 'continue':
          instruction = `Continue on ${step.name || 'current road'}`
          break
        case 'roundabout':
          instruction = `At the roundabout, take exit ${maneuver.exit || 1}${street}`
          break
        case 'fork':
          instruction = `Keep ${maneuver.modifier || 'right'}${street}`
          break
        case 'end of road':
          instruction = `At the end of the road, turn ${maneuver.modifier || 'right'}${street}`
          break
        default:
          instruction = `${maneuver.type || 'Proceed'} ${maneuver.modifier || ''}${street}`.trim()
      }

      return {
        id: idx,
        instruction,
        distanceText: stepDistText,
        durationSeconds: Math.round(step.duration),
      }
    })

    return {
      success: true,
      coordinates,
      distanceKm: Number(distanceKm.toFixed(1)),
      durationMin: Math.max(durationMin, 1),
      summary: route.legs?.[0]?.summary || 'Fastest Road Route',
      steps,
    }
  } catch (err) {
    console.warn('OSRM routing failed, falling back to direct line:', err)
    const directDist = distanceInKm(startLat, startLng, endLat, endLng)
    return {
      success: false,
      fallback: true,
      error: err.message,
      coordinates: [
        [startLat, startLng],
        [endLat, endLng],
      ],
      distanceKm: Number(directDist.toFixed(1)),
      durationMin: Math.max(Math.round((directDist / 25) * 60), 2),
      summary: 'Direct Path (Estimate)',
      steps: [
        {
          id: 0,
          instruction: 'Head towards destination venue',
          distanceText: `${directDist.toFixed(1)} km`,
          durationSeconds: 0,
        },
        {
          id: 1,
          instruction: 'Arrive at destination venue',
          distanceText: '0 m',
          durationSeconds: 0,
        },
      ],
    }
  }
}
