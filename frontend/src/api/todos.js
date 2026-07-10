import apiClient from "./client";

export async function fetchTodos() {
  const { data } = await apiClient.get("/api/v1/todos");
  return data;
}

export async function createTodo(title, description) {
  const { data } = await apiClient.post("/api/v1/todos", { title, description });
  return data;
}

export async function updateTodo(id, updates) {
  const { data } = await apiClient.put(`/api/v1/todos/${id}`, updates);
  return data;
}

export async function deleteTodo(id) {
  await apiClient.delete(`/api/v1/todos/${id}`);
}
