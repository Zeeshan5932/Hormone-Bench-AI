import { FirebaseError } from "firebase/app"

const MESSAGES: Record<string, string> = {
  "auth/invalid-credential": "That email or password doesn't match our records.",
  "auth/invalid-email": "Enter a valid email address.",
  "auth/user-disabled": "This account has been disabled. Contact support for help.",
  "auth/user-not-found": "That email or password doesn't match our records.",
  "auth/wrong-password": "That email or password doesn't match our records.",
  "auth/email-already-in-use": "An account with this email already exists.",
  "auth/weak-password": "Use at least 8 characters, with a letter and a number.",
  "auth/too-many-requests": "Too many attempts. Wait a few minutes and try again.",
  "auth/network-request-failed": "Check your connection and try again.",
}

export function getAuthErrorMessage(error: unknown): string {
  if (error instanceof FirebaseError) {
    if (process.env.NODE_ENV !== "production") {
      console.error(`[auth] ${error.code}:`, error.message)
    }
    return MESSAGES[error.code] ?? `Something went wrong (${error.code}). Try again.`
  }
  if (process.env.NODE_ENV !== "production") {
    console.error("[auth] unknown error:", error)
  }
  return "Something went wrong. Try again."
}
