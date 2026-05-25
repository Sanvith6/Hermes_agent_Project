import { useEffect, useCallback } from 'react'
import api from '../lib/api'
import { useChatStore } from '../lib/store/chatStore'
import type { Message, Chat } from '../types'

export function useChat(chatId?: string) {
  const { setChats, setMessages, setActiveChat, setMessages: setStoreMessages } = useChatStore()

  const loadChats = useCallback(async () => {
    try {
      const { data } = await api.get('/chats')
      setChats(data)
    } catch (error) {
      console.error('Failed to load chats:', error)
    }
  }, [setChats])

  const loadMessages = useCallback(async (id: string) => {
    try {
      const { data } = await api.get(`/chats/${id}/messages`)
      setStoreMessages(id, data)
      return data
    } catch (error) {
      console.error('Failed to load messages:', error)
    }
  }, [setStoreMessages])

  const sendMessage = useCallback(async (chatId: string, content: string, messageType: string = 'text') => {
    try {
      const { data } = await api.post(`/chats/${chatId}/messages`, {
        content,
        message_type: messageType
      })
      setStoreMessages(chatId, [...(useChatStore.getState().messages[chatId] || []), data])
      return data
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }, [setStoreMessages])

  const createChat = useCallback(async (name: string, memberIds: string[]) => {
    try {
      const { data } = await api.post('/chats', { name, member_ids: memberIds })
      return data
    } catch (error) {
      console.error('Failed to create chat:', error)
    }
  }, [])

  useEffect(() => {
    loadChats()
  }, [loadChats])

  useEffect(() => {
    if (chatId) {
      loadMessages(chatId)
    }
  }, [chatId, loadMessages])

  return { loadChats, loadMessages, sendMessage, createChat }
}
