import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Navbar from './components/Navbar'
import ProtectedRoute from './components/ProtectedRoute'

import Login from './pages/Login'
import Register from './pages/Register'
import Jobs from './pages/Jobs'
import JobDetail from './pages/JobDetail'
import Apply from './pages/Apply'
import PostJob from './pages/PostJob'
import RecruiterDashboard from './pages/RecruiterDashboard'
import CandidateDashboard from './pages/CandidateDashboard'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Jobs />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/jobs/:id" element={<JobDetail />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/jobs/:id/apply" element={
            <ProtectedRoute role="candidate">
              <Apply />
            </ProtectedRoute>
          } />
          <Route path="/dashboard/candidate" element={
            <ProtectedRoute role="candidate">
              <CandidateDashboard />
            </ProtectedRoute>
          } />

          <Route path="/jobs/post" element={
            <ProtectedRoute role="recruiter">
              <PostJob />
            </ProtectedRoute>
          } />
          <Route path="/dashboard/recruiter" element={
            <ProtectedRoute role="recruiter">
              <RecruiterDashboard />
            </ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}