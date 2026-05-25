"use client"
import React, { useState, useRef, useEffect } from 'react'
import { Send, Smile, Paperclip, Mic } from 'lucide-react'
import { useChatStore } from '../../lib/store/chatStore'
import { sendMessage, sendTyping, sendStopTyping } from '../../lib/websocket'
import { format } from 'date-fns'

export default function ChatWindow({ chatId }: { chatId: string }) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const typingTimeout = useRef<ReturnType<typeof setTimeout> | null>(null)
  const { messages, typingUsers } = useChatStore()

  const chatMessages = messages[chatId] || []
  const typing = typingUsers[chatId] || []

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const handleSend = () => {
    if (!input.trim()) return
    sendMessage(chatId, {
      content: input,
      message_type: 'text'
    })
    setInput('')
    sendStopTyping(chatId)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value)
    sendTyping(chatId)
    if (typingTimeout.current) clearTimeout(typingTimeout.current)
    typingTimeout.current = setTimeout(() => sendStopTyping(chatId), 2000)
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {chatMessages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender_id === 'me' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg px-3 py-2 ${
                msg.sender_id === 'me'
                  ? 'bg-[#005c4b] text-white'
                  : 'bg-[#202c33] text-white'
              }`}
            >
              <p>{msg.content}</p>
              <p className="text-xs opacity-60 text-right mt-1">
                {format(new Date(msg.created_at), 'HH:mm')}
                {msg.sender_id === 'me' && (
                  <span className="ml-1">
                    {msg.status === 'read' ? '✓✓' : msg.status === 'delivered' ? '✓✓' : '✓'}
                  </span>
                )}
              </p>
            </div>
          </div>
        ))}
        {typing.length > 0 && (
          <div className="text-sm text-gray-400 italic">typing...</div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-3 bg-[#202c33]">
        <div className="flex items-center gap-2">
          <button className="text-gray-400 hover:text-white">
            <Smile size={24} />
          </button>
          <button className="text-gray-400 hover:text-white">
            <Paperclip size={24} />
          </button>
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type a message"
            className="flex-1 bg-[#2a3942] text-white rounded-lg px-3 py-2 outline-none"
          />
          {input.trim() ? (
            <button onClick={handleSend} className="text-[#00a884]">
              <Send size={24} />
            </button>
          ) : (
            <button className="text-[#00a884]">
              <Mic size={24} />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
