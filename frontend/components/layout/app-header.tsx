"use client"

import { useRouter } from "next/navigation"
import Link from "next/link"
import { ChevronDown, LogOut, Settings, User } from "lucide-react"

import { useAuth } from "@/contexts/auth-context"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

function getInitials(name: string | null | undefined, email: string | null | undefined) {
  if (name) {
    const parts = name.trim().split(/\s+/)
    return parts
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("")
  }
  return email?.[0]?.toUpperCase() ?? "?"
}

export function AppHeader({
  title,
  description,
}: {
  title: string
  description?: string
}) {
  const router = useRouter()
  const { user, signOut } = useAuth()

  async function handleSignOut() {
    await signOut()
    router.push("/")
    router.refresh()
  }

  return (
    <header className="flex h-16 shrink-0 items-center gap-3 border-b border-border bg-background px-4 sm:px-6">
      <SidebarTrigger />
      <Separator orientation="vertical" className="h-5" />

      <div className="flex min-w-0 flex-1 flex-col justify-center">
        <h1 className="truncate text-base font-semibold text-foreground">
          {title}
        </h1>
        {description ? (
          <p className="hidden truncate text-xs text-muted-foreground sm:block">
            {description}
          </p>
        ) : null}
      </div>

      {/* <Button variant="ghost" size="icon-sm" aria-label="Notifications">
        <Bell />
      </Button> */}

      <DropdownMenu>
        <DropdownMenuTrigger
          render={
            <Button variant="ghost" className="gap-2 pl-1.5 pr-2">
              <Avatar size="sm">
                <AvatarFallback>
                  {getInitials(user?.displayName, user?.email)}
                </AvatarFallback>
              </Avatar>
              <span className="hidden text-sm font-medium sm:inline">
                {user?.displayName || user?.email || "Account"}
              </span>
              <ChevronDown className="size-3.5 text-muted-foreground" />
            </Button>
          }
        />
        <DropdownMenuContent align="end" className="w-48">
          <DropdownMenuItem render={<Link href="/settings" />}>
            <User />
            Profile
          </DropdownMenuItem>
          <DropdownMenuItem render={<Link href="/settings" />}>
            <Settings />
            Settings
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem variant="destructive" onClick={handleSignOut}>
            <LogOut />
            Sign out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </header>
  )
}
