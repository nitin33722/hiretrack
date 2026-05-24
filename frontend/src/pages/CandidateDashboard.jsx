import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getMyApplications } from '../api/applications'
import StatusBadge from '../components/StatusBadge'

export default function CandidateDashboard() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getMyApplications()
      .then(res => setApplications(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div style={{ maxWidth: '900px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>My Applications</h2>
        <Link to="/jobs" style={{ padding: '8px 16px', backgroundColor: '#1a1a2e', color: 'white', textDecoration: 'none', borderRadius: '6px' }}>
          Browse Jobs
        </Link>
      </div>

      {loading ? <p>Loading...</p> : applications.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <p>You haven't applied to any jobs yet.</p>
          <Link to="/jobs">Browse Jobs</Link>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {applications.map(app => (
            <div key={app.id} style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div>
                  <h3 style={{ margin: '0 0 8px' }}>{app.job_title || `Job #${app.job_id}`}</h3>
                  {app.job_location && <p style={{ margin: '0 0 4px', color: '#666' }}>📍 {app.job_location}</p>}
                  {app.job_salary_range && <p style={{ margin: '0 0 4px', color: '#666' }}>💰 {app.job_salary_range}</p>}
                  <p style={{ margin: '4px 0 0', color: '#999', fontSize: '13px' }}>
                    Applied: {new Date(app.applied_at).toLocaleDateString()}
                  </p>
                </div>
                <StatusBadge status={app.status} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}