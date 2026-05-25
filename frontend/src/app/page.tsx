"use client"
import { useChatStore } from '../lib/store/chatStore'
import Sidebar from '../components/Sidebar/Sidebar'
import ChatWindow from '../components/Chat/ChatWindow'

export default function Home() {
  const { activeChat } = useChatStore()

  return (
    <div className="h-screen flex bg-[#111b21]">
      <Sidebar />
      {activeChat ? (
        <div className="flex-1 flex flex-col">
          <div className="h-14 bg-[#1f2c33] flex items-center px-4 border-b border-[#2a3942]">
            <h2 className="text-white font-medium">{activeChat.name || 'Chat'}</h2>
          </div>
          <div className="flex-1">
            <ChatWindow chatId={activeChat.id} />
          </div>
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center bg-[#222e35]">
          <div className="text-center">
            <h1 className="text-3xl font-light text-[#00a884] mb-2">WhatsApp Web</h1>
            <p className="text-gray-400">Select a chat to start messaging</p>
          </div>
        </div>
      )}
    </div>
  )
}
