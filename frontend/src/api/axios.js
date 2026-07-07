import axios from "axios";

// Central Axios instance. withCredentials ensures the Flask session
// cookie is sent with every request (required for auth).
const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true,
  timeout: 10000, // fail fast if the Flask backend is not running
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
