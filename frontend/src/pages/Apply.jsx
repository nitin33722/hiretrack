import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { applyForJob } from '../api/applications'

export default function Apply() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [coverLetter, setCoverLetter] = useState('')
  const [resume, setResume] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const formData = new FormData()
    formData.append('job_id', id)
    formData.append('cover_letter', coverLetter)
    if (resume) formData.append('resume', resume)

    try {
      await applyForJob(formData)
      navigate('/dashboard/candidate')
    } catch (err) {
      setError(err.response?.data?.detail || 'Application failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ padding: '32px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>Apply for Job #{id}</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '6px', fontWeight: '600' }}>
              Resume (PDF or DOCX)
            </label>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(e) => setResume(e.target.files[0])}
              style={{ width: '100%' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '6px', fontWeight: '600' }}>
              Cover Letter
            </label>
            <textarea
              value={coverLetter}
              onChange={(e) => setCoverLetter(e.target.value)}
              rows={6}
              placeholder="Write your cover letter here..."
              style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #ddd', fontSize: '14px', resize: 'vertical' }}
            />
          </div>
          <button type="submit" disabled={loading} style={{
            padding: '10px',
            backgroundColor: '#1a1a2e',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '14px'
          }}>
            {loading ? 'Submitting...' : 'Submit Application'}
          </button>
        </form>
      </div>
    </div>
  )
}