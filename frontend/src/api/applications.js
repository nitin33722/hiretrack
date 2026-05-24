import client from './client'

export const applyForJob = (formData) =>
  client.post('/applications', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })

export const getMyApplications = () => client.get('/applications/me')

export const getJobApplications = (jobId) =>
  client.get(`/applications/job/${jobId}`)

export const updateStatus = (applicationId, status) =>
  client.patch(`/applications/${applicationId}/status`, { status })
