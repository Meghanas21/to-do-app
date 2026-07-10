import apiClient from "./client";

export async function registerUser(email, password) {
  const { data } = await apiClient.post("/api/v1/auth/register", { email, password });
  return data;
}

export async function loginUser(email, password) {
  const { data } = await apiClient.post("/api/v1/auth/login", { email, password });
  return data; // { access_token, token_type }
}

export async function getCurrentUser() {
  const { data } = await apiClient.get("/api/v1/auth/me");
  return data;
}
