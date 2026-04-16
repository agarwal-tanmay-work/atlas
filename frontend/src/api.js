import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const searchFailures = (q, domain, rootCause, limit) => 
  api.get('/search', { params: { q, domain, root_cause: rootCause, limit } })

export const searchBySymptom = (symptom) =>
  api.get('/search/by-symptom', { params: { symptom } })

export const getFailure = (id) => api.get(`/failures/${id}`)

export const getFailures = (domain, severity, limit, offset) =>
  api.get('/failures', { params: { domain, severity, limit, offset } })

export const getStats = () => api.get('/failures/stats')

export const getRootCauses = () => api.get('/search/root-causes')

export const getDomains = () => api.get('/search/domains')

export const analyzeProject = (projectDescription) =>
  api.post('/analyze', { project_description: projectDescription })
