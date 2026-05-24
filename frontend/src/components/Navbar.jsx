import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '0 32px',
      height: '60px',
      backgroundColor: '#1a1a2e',
      color: 'white'
    }}>
      <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '20px', fontWeight: 'bold' }}>
        HireTrack
      </Link>

      <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
        <Link to="/jobs" style={{ color: 'white', textDecoration: 'none' }}>Jobs</Link>

        {!user && (
          <>
            <Link to="/login" style={{ color: 'white', textDecoration: 'none' }}>Login</Link>
            <Link to="/register" style={{ color: 'white', textDecoration: 'none' }}>Register</Link>
          </>
        )}

        {user?.role === 'recruiter' && (
          <>
            <Link to="/dashboard/recruiter" style={{ color: 'white', textDecoration: 'none' }}>Dashboard</Link>
            <Link to="/jobs/post" style={{ color: 'white', textDecoration: 'none' }}>Post a Job</Link>
          </>
        )}

        {user?.role === 'candidate' && (
          <Link to="/dashboard/candidate" style={{ color: 'white', textDecoration: 'none' }}>My Applications</Link>
        )}

        {user && (
          <button onClick={handleLogout} style={{
            backgroundColor: 'transparent',
            border: '1px solid white',
            color: 'white',
            padding: '6px 14px',
            borderRadius: '6px',
            cursor: 'pointer'
          }}>
            Logout
          </button>
        )}
      </div>
    </nav>
  )
}