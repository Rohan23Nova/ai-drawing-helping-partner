const API_BASE_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

function buildUrl(path) {
  return `${API_BASE_URL}${path}`;
}

async function parseJson(response) {
  if (response.ok) {
    return response.json();
  }

  let message = "Something went wrong.";

  try {
    const data = await response.json();
    message = data.detail || data.message || message;
  } catch {
    message = response.statusText || message;
  }

  throw new Error(message);
}

export async function uploadReference(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(buildUrl("/upload"), {
    method: "POST",
    body: formData
  });

  return parseJson(response);
}

export async function sendChatMessage(imageId, message) {
  const response = await fetch(buildUrl("/chat"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      image_id: imageId,
      message
    })
  });

  return parseJson(response);
}

export async function updateProgress(imageId, step) {
  const response = await fetch(buildUrl(`/chat/${imageId}/progress/${step}`), {
    method: "POST"
  });

  return parseJson(response);
}

export function getOriginalImageUrl(imageId) {
  return buildUrl(`/images/${imageId}/original`);
}

export function getEdgeMapUrl(imageId) {
  return buildUrl(`/images/${imageId}/edges`);
}
