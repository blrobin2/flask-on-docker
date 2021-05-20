export async function getEmails() {
  const response = await fetch('/api');
  return await response.json();
}

export async function updateEmail(id, data) {
  const response = await fetch(`/api/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      body: JSON.stringify(data)
    }
  });
  return await response.json();
}
