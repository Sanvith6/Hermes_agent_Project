import { create } from 'zustand'
import type { Chat, Message, User } from '../../types'

interface ChatState {
  chats: Chat[]
  activeChat: Chat | null
  messages: Record<string, Message[]>
  typingUsers: Record<string, string[]>
  onlineUsers: Set<string>
  setChats: (chats: Chat[]) => void
  setActiveChat: (chat: Chat | null) => void
  addMessage: (message: Message) => void
  setMessages: (chatId: string, messages: Message[]) => void
  setTyping: (userId: string, chatId: string) => void
  removeTyping: (userId: string, chatId: string) => void
  setUserOnline: (userId: string, isOnline: boolean) => void
  markMessagesRead: (chatId: string, messageIds: string[], readBy: string) => void
}

export const useChatStore = create<ChatState>((set) => ({
  chats: [],
  activeChat: null,
  messages: {},
  typingUsers: {},
  onlineUsers: new Set(),

  setChats: (chats) => set({ chats }),

  setActiveChat: (chat) => set({ activeChat: chat }),

  addMessage: (message) => set((state) => {
    const chatMessages = state.messages[message.chat_id] || []
    return {
      messages: {
        ...state.messages,
        [message.chat_id]: [...chatMessages, message]
      }
    }
  }),

  setMessages: (chatId, messages) => set((state) => ({
    messages: { ...state.messages, [chatId]: messages }
  })),

  setTyping: (userId, chatId) => set((state) => {
    const current = state.typingUsers[chatId] || []
    if (current.includes(userId)) return state
    return {
      typingUsers: { ...state.typingUsers, [chatId]: [...current, userId] }
    }
  }),

  removeTyping: (userId, chatId) => set((state) => {
    const current = state.typingUsers[chatId] || []
    return {
      typingUsers: {
        ...state.typingUsers,
        [chatId]: current.filter(id => id !== userId)
      }
    }
  }),

  setUserOnline: (userId, isOnline) => set((state) => {
    const newOnline = new Set(state.onlineUsers)
    if (isOnline) newOnline.add(userId)
    else newOnline.delete(userId)
    return { onlineUsers: newOnline }
  }),

  markMessagesRead: (chatId, messageIds, readBy) => set((state) => {
    const chatMessages = state.messages[chatId] || []
    return {
      messages: {
        ...state.messages,
        [chatId]: chatMessages.map(m =>
          messageIds.includes(m.id) ? { ...m, status: 'read' as const } : m
        )
      }
    }
  })
}))
