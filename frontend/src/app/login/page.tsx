"use client"
import { useState } from 'react'
import { useAuth } from '../../hooks/useAuth'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const { login, loading } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await login(username, password)
  }

  return (
    <div className="min-h-screen bg-[#111b21] flex items-center justify-center">
      <div className="bg-[#202c33] rounded-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-[#00a884] text-center mb-6">
          WhatsApp Web Clone
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
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <p className="text-center text-gray-400 text-sm mt-4">
          Don't have an account?{' '}
          <a href="/register" className="text-[#00a884]">
            Register
          </a>
        </p>
      </div>
    </div>
  )
}
