import {
  LayoutDashboard,
  FlaskConical,
  BookOpen,
  Library,
  Bot,
  Settings,
  type LucideIcon,
} from "lucide-react"

export type NavItem = {
  title: string
  href: string
  icon: LucideIcon
}

export const primaryNav: NavItem[] = [
  { title: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { title: "Research Hub", href: "/research", icon: FlaskConical },
  { title: "AI Agents", href: "/agents", icon: Bot },
  { title: "Awareness Center", href: "/awareness", icon: BookOpen },
  { title: "Resource Library", href: "/resources", icon: Library },
]

export const secondaryNav: NavItem[] = [
  { title: "Settings", href: "/settings", icon: Settings },
]
