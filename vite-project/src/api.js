import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:5000", // Địa chỉ API Flask
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  getDepartments() {
    return apiClient.get("/api/departments");
  },
};
