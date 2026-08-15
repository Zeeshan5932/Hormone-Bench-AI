import { NextResponse } from "next/server"

import {
  createSessionCookie,
  clearSessionCookie,
  verifySession,
} from "@/lib/auth/session"

export async function POST(request: Request) {
  const { idToken } = await request.json()

  if (typeof idToken !== "string" || !idToken) {
    return NextResponse.json({ error: "Missing idToken" }, { status: 400 })
  }

  try {
    await createSessionCookie(idToken)
    return NextResponse.json({ success: true })
  } catch {
    return NextResponse.json(
      { error: "Failed to create session" },
      { status: 401 }
    )
  }
}

export async function DELETE() {
  const session = await verifySession()

  if (!session) {
    return NextResponse.json({ error: "No active session" }, { status: 401 })
  }

  await clearSessionCookie()
  return NextResponse.json({ success: true })
}
