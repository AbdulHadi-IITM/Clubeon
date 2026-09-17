import badmintonPng from '@/assets/badminton_court.png'
import tennisPng from '@/assets/tennis_court.png'

import badmintonWebp from '@/assets/courts/badminton.webp'
import tennisWebp from '@/assets/courts/tennis.webp'
import squashWebp from '@/assets/courts/squash.webp'
import basketballWebp from '@/assets/courts/basketball.webp'
import footballWebp from '@/assets/courts/football.webp'
import golfWebp from '@/assets/courts/golf.webp'
import padelWebp from '@/assets/courts/padel.webp'
import pickleballWebp from '@/assets/courts/pickleball.webp'
import volleyballWebp from '@/assets/courts/volleyball.webp'
import multipurposeWebp from '@/assets/courts/multi-purpose.webp'

export const sportImages = {
  tennis: tennisPng,
  tennisWebp,
  badminton: badmintonPng,
  badmintonWebp,
  squash: squashWebp,
  basketball: basketballWebp,
  football: footballWebp,
  soccer: footballWebp,
  golf: golfWebp,
  padel: padelWebp,
  pickleball: pickleballWebp,
  volleyball: volleyballWebp,
  'multi-purpose': multipurposeWebp,
  default: tennisPng
}

/**
 * Returns the exact local image asset matching the sport, court name, or event title description.
 * @param {string} text - Sport name, court name, or event title (e.g. "Harshita Tennis Tourny", "Badminton Court 1")
 * @param {string} [fallback] - Optional custom fallback image
 * @returns {string} Image URL / Asset path
 */
export function getSportImage(text, fallback = null) {
  if (!text) return fallback || tennisPng
  const str = String(text).toLowerCase()

  if (str.includes('badminton') || str.includes('shuttle')) {
    return badmintonPng
  }
  if (str.includes('tennis')) {
    return tennisPng
  }
  if (str.includes('squash')) {
    return squashWebp
  }
  if (str.includes('basketball') || str.includes('hoop')) {
    return basketballWebp
  }
  if (str.includes('football') || str.includes('soccer')) {
    return footballWebp
  }
  if (str.includes('golf')) {
    return golfWebp
  }
  if (str.includes('padel')) {
    return padelWebp
  }
  if (str.includes('pickleball')) {
    return pickleballWebp
  }
  if (str.includes('volleyball')) {
    return volleyballWebp
  }
  if (str.includes('arena') || str.includes('multi') || str.includes('stadium')) {
    return multipurposeWebp
  }

  return fallback || tennisPng
}

export default {
  sportImages,
  getSportImage
}
