import Link from "next/link"
import type { Metadata } from "next"

import { AuthProvider } from "@/contexts/auth-context"
import { Logo } from "@/components/layout/logo"

export const metadata: Metadata = {
  title: "Sign in",
}

export default function AuthLayout({ children }: LayoutProps<"/">) {
  return (
    <AuthProvider>
      <div className="flex min-h-screen flex-col items-center justify-center gap-6 bg-muted/40 px-6 py-12">
        <Link href="/" aria-label="HormoneBench AI">
          <Logo height={56} />
        </Link>
        {children}
      </div>
    </AuthProvider>
  )
}
