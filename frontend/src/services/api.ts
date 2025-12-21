import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: async (username: string, password: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await api.post('/auth/login', formData);
    return response.data;
  },
};

export const evidence = {
  upload: async (caseId: string, file: File) => {
    const formData = new FormData();
    formData.append('case_id', caseId);
    formData.append('file', file);
    const response = await api.post('/evidence/upload', formData, {
      headers: {
        'Content-Type': undefined, // Let browser set multipart/form-data with boundary
      } as any,
    });
    return response.data;
  },
  verify: async (evidenceId: string) => {
    const response = await api.get(`/evidence/${evidenceId}/verify`);
    return response.data;
  },
};

export const cases = {
  list: async () => {
    const response = await api.get('/cases');
    return response.data;
  },
  get: async (id: string) => {
    const response = await api.get(`/cases/${id}`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post('/cases/', data);
    return response.data;
  },
};

export default api;
