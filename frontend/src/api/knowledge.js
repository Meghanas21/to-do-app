import apiClient from "./client";

export async function fetchTasks(params = {}) {
  const query = new URLSearchParams(params).toString();
  const { data } = await apiClient.get(`/api/v1/tasks${query ? `?${query}` : ""}`);
  return data;
}

export async function createTask(title, description, assignedToId) {
  const { data } = await apiClient.post("/api/v1/tasks", { title, description, assigned_to_id: assignedToId });
  return data;
}

export async function updateTask(id, status) {
  const { data } = await apiClient.patch(`/api/v1/tasks/${id}`, { status });
  return data;
}

export async function fetchDocuments() {
  const { data } = await apiClient.get("/api/v1/documents");
  return data;
}

export async function uploadDocument(title, file) {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("file", file);
  const { data } = await apiClient.post("/api/v1/documents", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function searchDocuments(query) {
  const { data } = await apiClient.post(`/api/v1/search?query=${encodeURIComponent(query)}`);
  return data;
}

export async function fetchAnalytics() {
  const { data } = await apiClient.get("/api/v1/analytics");
  return data;
}

export async function fetchUsers() {
  const { data } = await apiClient.get("/api/v1/users");
  return data;
}
