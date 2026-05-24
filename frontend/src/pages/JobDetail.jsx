import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getJob } from '../api/jobs'
import { useAuth } from '../context/AuthContext'

export default function JobDetail() {
  const { id } = useParams()
  const [job, setJob] = useState(null)
  const { user } = useAuth()

  useEffect(() => {
    getJob(id).then(res => setJob(res.data)).catch(console.error)
  }, [id])

  if (!job) return <p style={{ padding: '40px', textAlign: 'center' }}>Loading...</p>

  return (
    <div style={{ maxWidth: '700px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ padding: '32px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>{job.title}</h2>
        <p>📍 {job.location}</p>
        {job.salary_range && <p>💰 {job.salary_range}</p>}
        <hr />
        <p style={{ lineHeight: '1.6' }}>{job.description}</p>
        <hr />
        {user?.role === 'candidate' && (
          <Link to={`/jobs/${id}/apply`} style={{
            display: 'inline-block',
            marginTop: '16px',
            padding: '10px 24px',
            backgroundColor: '#1a1a2e',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '6px'
          }}>
            Apply Now
          </Link>
        )}
        {!user && (
          <p><Link to="/login">Login</Link> to apply for this job.</p>
        )}
      </div>
    </div>
  )
}