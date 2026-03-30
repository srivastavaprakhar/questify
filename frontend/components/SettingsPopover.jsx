"use client"
import { useState } from "react"
import { LogOut } from "lucide-react"
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover"

export default function SettingsPopover({ children, onLogout }) {
  const [open, setOpen] = useState(false)

  const handleLogout = () => {
    onLogout?.()
    setOpen(false)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>{children}</PopoverTrigger>
      <PopoverContent className="w-64 p-0" align="start" side="top">
        <div className="p-2">
          <button 
            onClick={handleLogout}
            className="flex items-center gap-3 w-full p-2 text-sm text-left hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg"
          >
            <LogOut className="h-4 w-4" />
            <span>Log out</span>
          </button>
        </div>
      </PopoverContent>
    </Popover>
  )
}
