import { io, Socket } from 'socket.io-client'
import { useChatStore } from './store/chatStore'

let socket: Socket | null = null

export function connect(token: string) {
  socket = io(process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws', {
    auth: { token }
  })

  socket.on('connect', () => {
    console.log('WebSocket connected')
  })

  socket.on('new_message', (data) => {
    useChatStore.getState().addMessage(data.message)
  })

  socket.on('user_typing', (data) => {
    useChatStore.getState().setTyping(data.user_id, data.chat_id)
  })

  socket.on('user_stop_typing', (data) => {
    useChatStore.getState().removeTyping(data.user_id, data.chat_id)
  })

  socket.on('messages_read', (data) => {
    useChatStore.getState().markMessagesRead(data.chat_id, data.message_ids, data.read_by)
  })

  socket.on('user_online', (data) => {
    useChatStore.getState().setUserOnline(data.user_id, true)
  })

  socket.on('user_offline', (data) => {
    useChatStore.getState().setUserOnline(data.user_id, false)
  })

  return socket
}

export function disconnect() {
  socket?.disconnect()
  socket = null
}

export function sendMessage(chatId: string, message: object) {
  socket?.emit('send_message', { chat_id: chatId, ...message })
}

export function sendTyping(chatId: string) {
  socket?.emit('typing', { chat_id: chatId })
}

export function sendStopTyping(chatId: string) {
  socket?.emit('stop_typing', { chat_id: chatId })
}

export function sendMarkRead(chatId: string, messageIds: string[]) {
  socket?.emit('mark_read', { chat_id: chatId, message_ids: messageIds })
}
