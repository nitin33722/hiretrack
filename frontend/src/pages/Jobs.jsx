import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getJobs } from '../api/jobs'
import { useAuth } from '../context/AuthContext'

export default function Jobs() {
  const [jobs, setJobs] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [title, setTitle] = useState('')
  const [location, setLocation] = useState('')
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()

  useEffect(() => {
    fetchJobs()
  }, [page, title, location])

  const fetchJobs = async () => {
    setLoading(true)
    try {
      const res = await getJobs({ page, limit: 10, title, location })
      setJobs(res.data.items)
      setTotal(res.data.total)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '900px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2>Job Listings ({total})</h2>
        {user?.role === 'recruiter' && (
          <Link to="/jobs/post" style={{ ...buttonStyle, textDecoration: 'none' }}>Post a Job</Link>
        )}
      </div>

      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
        <input
          placeholder="Search by title..."
          value={title}
          onChange={(e) => { setTitle(e.target.value); setPage(1) }}
          style={inputStyle}
        />
        <input
          placeholder="Filter by location..."
          value={location}
          onChange={(e) => { setLocation(e.target.value); setPage(1) }}
          style={inputStyle}
        />
      </div>

      {loading ? <p>Loading...</p> : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {jobs.length === 0 ? <p>No jobs found.</p> : jobs.map(job => (
            <div key={job.id} style={cardStyle}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <h3 style={{ margin: '0 0 8px' }}>{job.title}</h3>
                  <p style={{ margin: '0 0 4px', color: '#666' }}>📍 {job.location}</p>
                  {job.salary_range && <p style={{ margin: '0', color: '#666' }}>💰 {job.salary_range}</p>}
                </div>
                <Link to={`/jobs/${job.id}`} style={{ ...buttonStyle, textDecoration: 'none', alignSelf: 'center' }}>
                  View
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{ display: 'flex', gap: '8px', marginTop: '24px', justifyContent: 'center' }}>
        <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} style={buttonStyle}>Prev</button>
        <span style={{ padding: '8px 16px' }}>Page {page}</span>
        <button onClick={() => setPage(p => p + 1)} disabled={jobs.length < 10} style={buttonStyle}>Next</button>
      </div>
    </div>
  )
}

const inputStyle = { padding: '10px', borderRadius: '6px', border: '1px solid #ddd', fontSize: '14px', flex: 1 }
const buttonStyle = { padding: '8px 16px', backgroundColor: '#1a1a2e', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '14px' }
const cardStyle = { padding: '20px', border: '1px solid #ddd', borderRadius: '8px', backgroundColor: 'white' }