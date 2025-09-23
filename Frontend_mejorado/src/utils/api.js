// api.js
import { BASE_URL } from '@/config'           // usa '@' si tienes alias; si no, cambia a ruta relativa

export function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

/* === NUEVO: helpers para URLs limpias y con slash final === */
function ensureTrailingSlash(path) {
  if (!path) return path
  const [base, qs] = path.split('?')
  return base.endsWith('/') ? path : `${base}/${qs ? `?${qs}` : ''}`
}
function joinUrl(base, path) {
  if (!base) return path
  if (base.endsWith('/') && path.startsWith('/')) return base + path.slice(1)
  if (!base.endsWith('/') && !path.startsWith('/')) return `${base}/${path}`
  return base + path
}

/* === REEMPLAZO: resolveUrl prioriza proxy en dev para /api === */
function resolveUrl(url) {
  const isDev = typeof import.meta !== 'undefined' && import.meta.env?.MODE === 'development'

  // En desarrollo, deja /api tal cual → Vite proxy lo maneja (mismo origen)
  if (isDev && url.startsWith('/api')) {
    return ensureTrailingSlash(url)
  }

  // URLs absolutas: respétalas y normaliza slash final
  if (/^https?:\/\//i.test(url)) {
    return ensureTrailingSlash(url)
  }

  // Con BASE_URL (tu caso en prod): compón
  const path = url.startsWith('/') ? url : `/${url}`
  return ensureTrailingSlash(joinUrl(BASE_URL, path))
}

/* === apiFetch (igual, ya con mejor parse de errores) === */
export async function apiFetch(url, method = 'GET', data = null) {
  const finalUrl = resolveUrl(url)

  const options = {
    method,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: method !== 'GET' && method !== 'DELETE' ? JSON.stringify(data) : undefined,
  }

  const res = await fetch(finalUrl, options)

  const parse = async () => {
    const text = await res.text()
    try { return JSON.parse(text) } catch { return { message: text || null } }
  }

  if (!res.ok) {
    const errBody = await parse()
    console.error('[apiFetch]', res.status, errBody)
    const msg = errBody?.message || errBody?.detail || `HTTP error! status: ${res.status}`
    throw new Error(msg)
  }

  if (method === 'DELETE' || res.status === 204) return null
  return await parse()
}
