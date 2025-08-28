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

  try {
    const response = await fetch(finalUrl, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    if (method === 'DELETE' || response.status === 204) {
      return null;
    }
    return await response.json();
  } catch (error) {
    console.error('API fetch error:', error);
    throw error;
  }
}
