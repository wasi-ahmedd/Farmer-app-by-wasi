const BASE_URL = "https://farmer-app-by-wasi.onrender.com/api";

function saveToken(t) { localStorage.setItem("fa_token", t); }
function getToken() { return localStorage.getItem("fa_token"); }
function clearToken() { localStorage.removeItem("fa_token"); }

async function api(path, { method = "GET", body = null, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth && getToken()) headers["Authorization"] = "Bearer " + getToken();

  const res = await fetch(BASE_URL + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  let data = null;
  try { data = await res.json(); } catch (e) {}

  if (!res.ok) throw new Error((data && data.error) || res.statusText);
  return data;
}

// ✅ Admin API
export async function getAdminStats() {
  const r = await fetch(`${BASE_URL}/admin/stats`);
  return await r.json();
}

export async function getAllUsers(role) {
  const r = await fetch(`${BASE_URL}/admin/users/${role}`);
  return await r.json();
}

export async function getAllCrops() {
  const r = await fetch(`${BASE_URL}/admin/crops`);
  return await r.json();
}

// ✅ Auth and Crop APIs
export async function signup(payload) { return api("/auth/signup", { method: "POST", body: payload }); }
export async function login(payload) { return api("/auth/login", { method: "POST", body: payload }); }
export async function createPlan(payload) { return api("/crops", { method: "POST", body: payload, auth: true }); }
export async function myPlans() { return api("/crops/mine", { auth: true }); }
export async function searchCrops(q) {
  const qs = q ? ("?q=" + encodeURIComponent(q)) : "";
  return api("/crops" + qs);
}

export { saveToken, getToken, clearToken };
