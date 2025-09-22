import { BASE_URL } from '@/config'

export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function resolveUrl(url) {
  const isAbsolute = /^https?:\/\//i.test(url);
  if (isAbsolute) return url;
  return url.startsWith('/') ? `${BASE_URL}${url}` : `${BASE_URL}/${url}`;
}

export async function apiFetch(url, method = 'GET', data = null) {
  const finalUrl = resolveUrl(url);

  const options = {
    method,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: method !== 'GET' && method !== 'DELETE' ? JSON.stringify(data) : undefined,
  };

  const res = await fetch(finalUrl, options);

  
  const parse = async () => {
    const text = await res.text();
    try { return JSON.parse(text); } catch { return { message: text || null }; }
  };

  if (!res.ok) {
    const errBody = await parse();
    console.error('[apiFetch]', res.status, errBody);
   
    const msg = errBody?.message || errBody?.detail || `HTTP error! status: ${res.status}`;
    throw new Error(msg);
  }

  if (method === 'DELETE' || res.status === 204) return null;
  return await parse();
}

