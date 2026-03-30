"use client"

import { useState } from "react"
import { X } from "lucide-react"
import { apiService } from "../lib/api"

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true)
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setSuccess("")
    setLoading(true)

    try {
      if (isLogin) {
        await apiService.login(username, password)
        localStorage.setItem("username", username)
        onAuthSuccess(username)
        onClose()
      } else {
        await apiService.signup(username, password)
        setSuccess("Signup successful! Please login with your credentials.")
        setIsLogin(true)
        setPassword("")
        // Keep username so user only needs to enter password
      }
    } catch (err) {
      // Provide more helpful error messages
      let errorMessage = err.message || "Authentication failed. Please try again."
      
      // Check if it's a connection error
      if (errorMessage.includes('Cannot connect to backend') || errorMessage.includes('Failed to fetch')) {
        errorMessage = "Cannot connect to backend server. Please make sure the backend is running (python api_wrapper.py) and accessible at http://127.0.0.1:8000"
      }
      
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="relative w-full max-w-md rounded-2xl border border-zinc-200 bg-white p-6 shadow-xl dark:border-zinc-800 dark:bg-zinc-900">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 rounded-lg p-2 hover:bg-zinc-100 dark:hover:bg-zinc-800"
        >
          <X className="h-4 w-4" />
        </button>

        <div className="mb-6">
          <h2 className="text-2xl font-semibold">{isLogin ? "Login" : "Sign Up"}</h2>
          <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
            {isLogin ? "Welcome back! Please login to continue." : "Create a new account to get started."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium mb-1">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 dark:border-zinc-800 dark:bg-zinc-950"
              placeholder="Enter your username"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 dark:border-zinc-800 dark:bg-zinc-950"
              placeholder="Enter your password"
            />
          </div>

          {error && (
            <div className="rounded-lg bg-red-50 border border-red-200 px-3 py-2 text-sm text-red-600 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400">
              {error}
            </div>
          )}

          {success && (
            <div className="rounded-lg bg-green-50 border border-green-200 px-3 py-2 text-sm text-green-600 dark:bg-green-900/20 dark:border-green-800 dark:text-green-400">
              {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-zinc-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50 dark:bg-white dark:text-zinc-900"
          >
            {loading ? "Please wait..." : isLogin ? "Login" : "Sign Up"}
          </button>
        </form>

        <div className="mt-4 text-center text-sm">
          <button
            onClick={() => {
              setIsLogin(!isLogin)
              setError("")
              setSuccess("")
              setPassword("")
            }}
            className="text-blue-600 hover:underline dark:text-blue-400"
          >
            {isLogin ? "Don't have an account? Sign up" : "Already have an account? Login"}
          </button>
        </div>
      </div>
    </div>
  )
}

