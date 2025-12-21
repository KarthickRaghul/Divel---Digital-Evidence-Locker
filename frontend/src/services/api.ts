import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  let token = localStorage.getItem('token');
  console.log('DEBUG: Interceptor running for', config.url);
  
  if (token) {
    // Remove quotes if they were accidentally stored
    token = token.replace(/^"(.*)"$/, '$1');
    console.log('DEBUG: Token found:', token ? 'Yes (starts with ' + token.substring(0, 10) + '...)' : 'No');
    
    config.headers.Authorization = `Bearer ${token}`;
    console.log('DEBUG: Authorization header set:', config.headers.Authorization);
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
        'Content-Type': undefined,
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
