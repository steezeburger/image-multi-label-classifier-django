// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * Makes POST request to url w/ data as json body.
 * @param url
 * @param data
 * @returns {Promise<Response>}
 */
async function post(url, data) {
  const csrfToken = getCookie('csrftoken')
  return await fetch(
    url, {
      method: 'POST',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': csrfToken,
      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
      body: JSON.stringify(data)
    })
}

/**
 * Makes PUT request to url w/ data as json body.
 * @param url
 * @param data
 * @returns {Promise<Response>}
 */
async function put(url, data) {
  const csrfToken = getCookie('csrftoken')
  return await fetch(
    url, {
      method: 'PUT',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': csrfToken,
      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer',
      body: JSON.stringify(data)
    })
}