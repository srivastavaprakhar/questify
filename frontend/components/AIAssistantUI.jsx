"use client"

import React, { useEffect, useMemo, useRef, useState } from "react"
import Sidebar from "./Sidebar"
import Header from "./Header"
import ChatPane from "./ChatPane"
import ThemeToggle from "./ThemeToggle"
import AuthModal from "./AuthModal"
import { apiService } from "../lib/api"

export default function AIAssistantUI() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [username, setUsername] = useState("")
  const [theme, setTheme] = useState(() => {
    const saved = typeof window !== "undefined" && localStorage.getItem("theme")
    if (saved) return saved
    if (typeof window !== "undefined" && window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)
      return "dark"
    return "light"
  })

  useEffect(() => {
    try {
      if (theme === "dark") document.documentElement.classList.add("dark")
      else document.documentElement.classList.remove("dark")
      document.documentElement.setAttribute("data-theme", theme)
      document.documentElement.style.colorScheme = theme
      localStorage.setItem("theme", theme)
    } catch {}
  }, [theme])

  useEffect(() => {
    try {
      const media = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)")
      if (!media) return
      const listener = (e) => {
        const saved = localStorage.getItem("theme")
        if (!saved) setTheme(e.matches ? "dark" : "light")
      }
      media.addEventListener("change", listener)
      return () => media.removeEventListener("change", listener)
    } catch {}
  }, [])

  const [backendStatus, setBackendStatus] = useState('checking') // 'checking' | 'online' | 'offline'

  // Check backend connection on mount with retry
  useEffect(() => {
    const checkBackend = async (retries = 3, delay = 2000) => {
      for (let i = 0; i < retries; i++) {
        try {
          await apiService.healthCheck()
          setBackendStatus('online')
          return
        } catch (error) {
          console.error(`Backend health check failed (attempt ${i + 1}/${retries}):`, error)
          if (i < retries - 1) {
            // Wait before retrying
            await new Promise(resolve => setTimeout(resolve, delay))
          } else {
            setBackendStatus('offline')
          }
        }
      }
    }
    checkBackend()
  }, [])

  // Check authentication on mount
  useEffect(() => {
    const savedUsername = localStorage.getItem("username")
    if (savedUsername) {
      setUsername(savedUsername)
      setIsAuthenticated(true)
    } else {
      setShowAuthModal(true)
    }
  }, [])

  const handleAuthSuccess = (user) => {
    setUsername(user)
    setIsAuthenticated(true)
    setShowAuthModal(false)
  }

  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [collapsed, setCollapsed] = useState(() => {
    try {
      const raw = localStorage.getItem("sidebar-collapsed")
      return raw ? JSON.parse(raw) : { pinned: true, recent: false }
    } catch {
      return { pinned: true, recent: false }
    }
  })
  useEffect(() => {
    try {
      localStorage.setItem("sidebar-collapsed", JSON.stringify(collapsed))
    } catch {}
  }, [collapsed])

  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => {
    try {
      const saved = localStorage.getItem("sidebar-collapsed-state")
      return saved ? JSON.parse(saved) : false
    } catch {
      return false
    }
  })

  useEffect(() => {
    try {
      localStorage.setItem("sidebar-collapsed-state", JSON.stringify(sidebarCollapsed))
    } catch {}
  }, [sidebarCollapsed])

  const [conversations, setConversations] = useState(() => {
    try {
      const saved = localStorage.getItem("conversations")
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })
  const [selectedId, setSelectedId] = useState(null)

  const [query, setQuery] = useState("")
  const searchRef = useRef(null)

  const [isThinking, setIsThinking] = useState(false)
  const [thinkingConvId, setThinkingConvId] = useState(null)

  useEffect(() => {
    const onKey = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "n") {
        e.preventDefault()
        createNewChat()
      }
      if (!e.metaKey && !e.ctrlKey && e.key === "/") {
        const tag = document.activeElement?.tagName?.toLowerCase()
        if (tag !== "input" && tag !== "textarea") {
          e.preventDefault()
          searchRef.current?.focus()
        }
      }
      if (e.key === "Escape" && sidebarOpen) setSidebarOpen(false)
    }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [sidebarOpen, conversations])

  // Save conversations to localStorage
  useEffect(() => {
    if (conversations.length > 0) {
      localStorage.setItem("conversations", JSON.stringify(conversations))
    }
  }, [conversations])

  useEffect(() => {
    if (!selectedId && conversations.length === 0) {
      createNewChat()
    }
  }, [])

  const filtered = useMemo(() => {
    if (!query.trim()) return conversations
    const q = query.toLowerCase()
    return conversations.filter((c) => c.title.toLowerCase().includes(q) || c.preview.toLowerCase().includes(q))
  }, [conversations, query])

  const pinned = filtered.filter((c) => c.pinned).sort((a, b) => (a.updatedAt < b.updatedAt ? 1 : -1))

  const recent = filtered
    .filter((c) => !c.pinned)
    .sort((a, b) => (a.updatedAt < b.updatedAt ? 1 : -1))
    .slice(0, 10)


  function togglePin(id) {
    setConversations((prev) => prev.map((c) => (c.id === id ? { ...c, pinned: !c.pinned } : c)))
  }

  function createNewChat() {
    const id = Math.random().toString(36).slice(2)
    const item = {
      id,
      title: "New Chat",
      updatedAt: new Date().toISOString(),
      messageCount: 0,
      preview: "Say hello to start...",
      pinned: false,
      messages: [],
    }
    setConversations((prev) => [item, ...prev])
    setSelectedId(id)
    setSidebarOpen(false)
  }

  async function sendMessage(convId, content) {
    if (!content.trim()) return
    const now = new Date().toISOString()
    const userMsg = { id: Math.random().toString(36).slice(2), role: "user", content, createdAt: now }

    // Update conversation with user message
    setConversations((prev) =>
      prev.map((c) => {
        if (c.id !== convId) return c
        const msgs = [...(c.messages || []), userMsg]
        const newTitle = c.title === "New Chat" ? content.slice(0, 50) : c.title
        return {
          ...c,
          title: newTitle,
          messages: msgs,
          updatedAt: now,
          messageCount: msgs.length,
          preview: content.slice(0, 80),
        }
      }),
    )

    setIsThinking(true)
    setThinkingConvId(convId)

    const currentConvId = convId
    try {
      // Call the backend API
      const response = await apiService.askQuestion(content)
      const answer = response.answer || "Sorry, I couldn't generate a response."

      setIsThinking(false)
      setThinkingConvId(null)

      setConversations((prev) =>
        prev.map((c) => {
          if (c.id !== currentConvId) return c
          const asstMsg = {
            id: Math.random().toString(36).slice(2),
            role: "assistant",
            content: answer,
            createdAt: new Date().toISOString(),
          }
          const msgs = [...(c.messages || []), asstMsg]
          return {
            ...c,
            messages: msgs,
            updatedAt: new Date().toISOString(),
            messageCount: msgs.length,
            preview: answer.slice(0, 80),
          }
        }),
      )
    } catch (error) {
      setIsThinking(false)
      setThinkingConvId(null)
      const errorMsg = error.message || "Sorry, I encountered an error. Please make sure the backend server is running and try again."
      setConversations((prev) =>
        prev.map((c) => {
          if (c.id !== currentConvId) return c
          const asstMsg = {
            id: Math.random().toString(36).slice(2),
            role: "assistant",
            content: `Error: ${errorMsg}`,
            createdAt: new Date().toISOString(),
          }
          const msgs = [...(c.messages || []), asstMsg]
          return {
            ...c,
            messages: msgs,
            updatedAt: new Date().toISOString(),
            messageCount: msgs.length,
            preview: errorMsg.slice(0, 80),
          }
        }),
      )
    }
  }

  function editMessage(convId, messageId, newContent) {
    const now = new Date().toISOString()
    setConversations((prev) =>
      prev.map((c) => {
        if (c.id !== convId) return c
        const msgs = (c.messages || []).map((m) =>
          m.id === messageId ? { ...m, content: newContent, editedAt: now } : m,
        )
        return {
          ...c,
          messages: msgs,
          preview: msgs[msgs.length - 1]?.content?.slice(0, 80) || c.preview,
        }
      }),
    )
  }

  function resendMessage(convId, messageId) {
    const conv = conversations.find((c) => c.id === convId)
    const msg = conv?.messages?.find((m) => m.id === messageId)
    if (!msg) return
    sendMessage(convId, msg.content)
  }

  function pauseThinking() {
    setIsThinking(false)
    setThinkingConvId(null)
  }

  const composerRef = useRef(null)

  const selected = conversations.find((c) => c.id === selectedId) || null

  if (!isAuthenticated) {
    return (
      <div className="h-screen w-full bg-zinc-50 text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100 flex items-center justify-center">
        <div className="w-full max-w-md px-4">
          {backendStatus === 'offline' && (
            <div className="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-600 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400">
              <div className="font-semibold mb-2">Backend Server Not Running</div>
              <div className="text-xs mb-2">
                Please start the backend server by running: <code className="bg-red-100 dark:bg-red-900/40 px-1 rounded">python api_wrapper.py</code>
              </div>
              <div className="text-xs mb-3">
                The backend should be running on <code className="bg-red-100 dark:bg-red-900/40 px-1 rounded">http://127.0.0.1:8000</code>
              </div>
              <button
                onClick={async () => {
                  setBackendStatus('checking')
                  try {
                    await apiService.healthCheck()
                    setBackendStatus('online')
                  } catch (error) {
                    setBackendStatus('offline')
                  }
                }}
                className="text-xs px-3 py-1.5 rounded bg-red-100 dark:bg-red-900/40 hover:bg-red-200 dark:hover:bg-red-900/60 transition-colors"
              >
                Retry Connection
              </button>
            </div>
          )}
          {backendStatus === 'checking' && (
            <div className="mb-4 rounded-lg bg-yellow-50 border border-yellow-200 px-4 py-3 text-sm text-yellow-600 dark:bg-yellow-900/20 dark:border-yellow-800 dark:text-yellow-400">
              Checking backend connection...
            </div>
          )}
          <AuthModal isOpen={showAuthModal} onClose={() => {}} onAuthSuccess={handleAuthSuccess} />
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen w-full bg-zinc-50 text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
      <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} onAuthSuccess={handleAuthSuccess} />
      <div className="md:hidden sticky top-0 z-40 flex items-center gap-2 border-b border-zinc-200/60 bg-white/80 px-3 py-2 backdrop-blur dark:border-zinc-800 dark:bg-zinc-900/70">
        <div className="ml-1 flex items-center gap-2 text-sm font-semibold tracking-tight">
          <span className="inline-flex h-4 w-4 items-center justify-center">✱</span> AI Assistant
        </div>
        <div className="ml-auto flex items-center gap-2">
          <ThemeToggle theme={theme} setTheme={setTheme} />
        </div>
      </div>

      <div className="mx-auto flex h-[calc(100vh-0px)] max-w-[1400px]">
        <Sidebar
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          theme={theme}
          setTheme={setTheme}
          collapsed={collapsed}
          setCollapsed={setCollapsed}
          sidebarCollapsed={sidebarCollapsed}
          setSidebarCollapsed={setSidebarCollapsed}
          conversations={conversations}
          pinned={pinned}
          recent={recent}
          selectedId={selectedId}
          onSelect={(id) => setSelectedId(id)}
          togglePin={togglePin}
          query={query}
          setQuery={setQuery}
          searchRef={searchRef}
          createNewChat={createNewChat}
          username={username}
          onLogout={() => {
            localStorage.removeItem("username")
            localStorage.removeItem("conversations")
            setIsAuthenticated(false)
            setConversations([])
            setSelectedId(null)
            setShowAuthModal(true)
          }}
        />

        <main className="relative flex min-w-0 flex-1 flex-col">
          <Header createNewChat={createNewChat} sidebarCollapsed={sidebarCollapsed} setSidebarOpen={setSidebarOpen} />
          <ChatPane
            ref={composerRef}
            conversation={selected}
            onSend={(content) => selected && sendMessage(selected.id, content)}
            onEditMessage={(messageId, newContent) => selected && editMessage(selected.id, messageId, newContent)}
            onResendMessage={(messageId) => selected && resendMessage(selected.id, messageId)}
            isThinking={isThinking && thinkingConvId === selected?.id}
            onPauseThinking={pauseThinking}
          />
        </main>
      </div>
    </div>
  )
}
