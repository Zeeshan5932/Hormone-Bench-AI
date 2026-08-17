import { redirect } from "next/navigation"

import { verifySession } from "@/lib/auth/session"

export async function AuthGate({ children }: { children: React.ReactNode }) {
  const session = await verifySession()

  if (!session) {
    redirect("/login")
  }

  return children
}
