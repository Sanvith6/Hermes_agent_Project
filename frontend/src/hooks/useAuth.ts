import { useState, useCallback } from 'react'
import api from '../lib/api'
import { connect, disconnect } from '../lib/websocket'
import type { User } from '../types'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)

  const login = useCallback(async (username: string, password: string) => {
    setLoading(true)
    try {
      const { data } = await api.post('/auth/login', new URLSearchParams({
        username, password
      }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      
      const { data: userData } = await api.get('/users/me')
      setUser(userData)
      connect(data.access_token)
      return userData
    } finally {
      setLoading(false)
    }
  }, [])

  const register = useCallback(async (username: string, email: string, password: string) => {
    setLoading(true)
    try {
      const { data } = await api.post('/auth/register', { username, email, password })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      
      const { data: userData } = await api.get('/users/me')
      setUser(userData)
      connect(data.access_token)
      return userData
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    disconnect()
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }, [])

  const refreshUser = useCallback(async () => {
    const { data } = await api.get('/users/me')
    setUser(data)
  }, [])

  return { user, loading, login, register, logout, refreshUser }
}
