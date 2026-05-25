export interface User {
  id: string
  username: string
  email: string
  avatar?: string
  bio?: string
  is_online: boolean
  last_seen?: string
}

export interface Message {
  id: string
  chat_id: string
  sender_id: string
  sender_username?: string
  content: string
  message_type: 'text' | 'image' | 'file' | 'voice_note'
  file_url?: string
  file_name?: string
  status: 'sent' | 'delivered' | 'read'
  reply_to_id?: string
  created_at: string
}

export interface Chat {
  id: string
  name?: string
  chat_type: 'private' | 'group'
  avatar?: string
  members: Array<{id: string; role: string}>
  last_message?: {id: string; content: string; created_at?: string}
  created_at: string
}

export interface TypingUser {
  user_id: string
  chat_id: string
}
