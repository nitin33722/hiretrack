import { useForm } from 'react-hook-form'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { login as loginApi } from '../api/auth'
import { useState } from 'react'

export default function Login() {
  const { register, handleSubmit } = useForm()
  const { login } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState('')

  const onSubmit = async (data) => {
    try {
      const res = await loginApi(data)
      login(res.data.access_token)
      const role = res.data.user.role
      navigate(role === 'recruiter' ? '/dashboard/recruiter' : '/dashboard/candidate')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div style={{ maxWidth: '400px', margin: '80px auto', padding: '32px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <input {...register('email')} placeholder="Email" type="email" required style={inputStyle} />
        <input {...register('password')} placeholder="Password" type="password" required style={inputStyle} />
        <button type="submit" style={buttonStyle}>Login</button>
      </form>
      <p style={{ marginTop: '16px' }}>Don't have an account? <Link to="/register">Register</Link></p>
    </div>
  )
}

const inputStyle = { padding: '10px', borderRadius: '6px', border: '1px solid #ddd', fontSize: '14px' }
const buttonStyle = { padding: '10px', backgroundColor: '#1a1a2e', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '14px' }