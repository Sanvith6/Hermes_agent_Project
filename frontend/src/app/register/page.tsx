"use client"
import { useState } from 'react'
import { useAuth } from '../../hooks/useAuth'

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { register, loading } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await register(username, email, password)
  }

  return (
    <div className="min-h-screen bg-[#111b21] flex items-center justify-center">
      <div className="bg-[#202c33] rounded-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-[#00a884] text-center mb-6">
          Create Account
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            className="w-full bg-[#2a3942] text-white rounded-lg px-4 py-3 outline-none"
            required
          />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="w-full bg-[#2a3942] text-white rounded-lg px-4 py-3 outline-none"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full bg-[#2a3942] text-white rounded-lg px-4 py-3 outline-none"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#00a884] text-white rounded-lg py-3 font-medium hover:bg-[#008f72] disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Register'}
          </button>
        </form>
        <p className="text-center text-gray-400 text-sm mt-4">
          Already have an account?{' '}
          <a href="/login" className="text-[#00a884]">
            Login
          </a>
        </p>
      </div>
    </div>
  )
}
