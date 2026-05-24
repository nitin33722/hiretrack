import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { createJob } from '../api/jobs'
import { useState } from 'react'

export default function PostJob() {
  const { register, handleSubmit } = useForm()
  const navigate = useNavigate()
  const [error, setError] = useState('')

  const onSubmit = async (data) => {
    try {
      await createJob(data)
      navigate('/dashboard/recruiter')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to post job')
    }
  }

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ padding: '32px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>Post a Job</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <input {...register('title')} placeholder="Job Title" required style={inputStyle} />
          <input {...register('location')} placeholder="Location" required style={inputStyle} />
          <input {...register('salary_range')} placeholder="Salary Range (e.g. 80000-120000)" style={inputStyle} />
          <textarea
            {...register('description')}
            placeholder="Job Description"
            rows={6}
            required
            style={{ ...inputStyle, resize: 'vertical' }}
          />
          <button type="submit" style={buttonStyle}>Post Job</button>
        </form>
      </div>
    </div>
  )
}

const inputStyle = { padding: '10px', borderRadius: '6px', border: '1px solid #ddd', fontSize: '14px' }
const buttonStyle = { padding: '10px', backgroundColor: '#1a1a2e', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '14px' }
