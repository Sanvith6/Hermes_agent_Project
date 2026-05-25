"use client"
import React from 'react'
import { useChatStore } from '../../lib/store/chatStore'
import { Search } from 'lucide-react'

export default function Sidebar() {
  const { chats, setActiveChat, activeChat } = useChatStore()

  return (
    <div className="w-[350px] bg-[#111b21] flex flex-col h-full border-r border-[#2a3942]">
      <div className="p-3">
        <div className="flex items-center gap-2 bg-[#202c33] rounded-lg px-3 py-2">
          <Search size={18} className="text-gray-400" />
          <input
            type="text"
            placeholder="Search or start new chat"
            className="bg-transparent text-white text-sm outline-none flex-1"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {chats.map((chat) => (
          <div
            key={chat.id}
            onClick={() => setActiveChat(chat)}
            className={`flex items-center gap-3 px-3 py-3 cursor-pointer hover:bg-[#202c33] ${
              activeChat?.id === chat.id ? 'bg-[#2a3942]' : ''
            }`}
          >
            <div className="w-12 h-12 rounded-full bg-[#00a884] flex items-center justify-center text-white font-bold flex-shrink-0">
              {chat.name ? chat.name[0].toUpperCase() : '?'}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex justify-between items-baseline">
                <h3 className="text-white font-medium truncate">{chat.name || 'Chat'}</h3>
                <span className="text-xs text-gray-400">
                  {chat.last_message?.created_at
                    ? new Date(chat.last_message.created_at).toLocaleDateString()
                    : ''}
                </span>
              </div>
              <p className="text-sm text-gray-400 truncate">
                {chat.last_message?.content || 'Start a conversation'}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
