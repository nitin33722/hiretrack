import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getJobs } from '../api/jobs'
import { getJobApplications, updateStatus } from '../api/applications'

export default function RecruiterDashboard() {
  const [jobs, setJobs] = useState([])
  const [selectedJob, setSelectedJob] = useState(null)
  const [applications, setApplications] = useState([])

  useEffect(() => {
    getJobs().then(res => setJobs(res.data.items)).catch(console.error)
  }, [])

  const viewApplications = async (job) => {
    setSelectedJob(job)
    const res = await getJobApplications(job.id)
    setApplications(res.data)
  }

  const handleStatusChange = async (applicationId, status) => {
    await updateStatus(applicationId, status)
    viewApplications(selectedJob)
  }

  return (
    <div style={{ maxWidth: '900px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>Recruiter Dashboard</h2>
        <Link to="/jobs/post" style={{ padding: '8px 16px', backgroundColor: '#1a1a2e', color: 'white', textDecoration: 'none', borderRadius: '6px' }}>
          Post a Job
        </Link>
      </div>

      <h3>Your Jobs</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '32px' }}>
        {jobs.map(job => (
          <div key={job.id} style={{ padding: '16px', border: '1px solid #ddd', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <strong>{job.title}</strong>
              <span style={{ marginLeft: '12px', color: '#666' }}>📍 {job.location}</span>
            </div>
            <button onClick={() => viewApplications(job)} style={{ padding: '6px 14px', backgroundColor: '#1a1a2e', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
              View Applicants
            </button>
          </div>
        ))}
      </div>

      {selectedJob && (
        <div>
          <h3>Applicants for: {selectedJob.title}</h3>
          {applications.length === 0 ? <p>No applications yet.</p> : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f5f5f5' }}>
                  <th style={thStyle}>ID</th>
                  <th style={thStyle}>Applied At</th>
                  <th style={thStyle}>Status</th>
                  <th style={thStyle}>Update Status</th>
                </tr>
              </thead>
              <tbody>
                {applications.map(app => (
                  <tr key={app.id}>
                    <td style={tdStyle}>#{app.id}</td>
                    <td style={tdStyle}>{new Date(app.applied_at).toLocaleDateString()}</td>
                    <td style={tdStyle}>
                      <span style={{ textTransform: 'capitalize' }}>{app.status}</span>
                    </td>
                    <td style={tdStyle}>
                      <select
                        value={app.status}
                        onChange={(e) => handleStatusChange(app.id, e.target.value)}
                        style={{ padding: '4px 8px', borderRadius: '4px' }}
                      >
                        <option value="pending">Pending</option>
                        <option value="reviewed">Reviewed</option>
                        <option value="accepted">Accepted</option>
                        <option value="rejected">Rejected</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  )
}

const thStyle = { padding: '10px', textAlign: 'left', borderBottom: '2px solid #ddd' }
const tdStyle = { padding: '10px', borderBottom: '1px solid #ddd' }