"use client"

import { useState, type FormEvent } from "react"
import Link from "next/link"
import { AlertCircle, ArrowLeft, MailCheck } from "lucide-react"

import { useAuth } from "@/contexts/auth-context"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { getAuthErrorMessage } from "@/lib/auth/error-messages"

export default function ForgotPasswordPage() {
  const { sendPasswordReset } = useAuth()

  const [email, setEmail] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSent, setIsSent] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(null)
    setIsSubmitting(true)
    try {
      await sendPasswordReset(email)
      setIsSent(true)
    } catch (err) {
      setError(getAuthErrorMessage(err))
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isSent) {
    return (
      <Card className="w-full max-w-sm">
        <CardHeader>
          <span className="mb-2 flex size-9 items-center justify-center rounded-lg bg-muted text-secondary">
            <MailCheck className="size-4.5" />
          </span>
          <CardTitle className="text-xl">Check your email</CardTitle>
          <CardDescription>
            If an account exists for {email}, we&apos;ve sent a link to reset
            your password.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" className="w-full" render={<Link href="/login" />}>
            <ArrowLeft />
            Back to sign in
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle className="text-xl">Reset your password</CardTitle>
        <CardDescription>
          Enter your email and we&apos;ll send you a reset link.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        {error ? (
          <div className="flex items-start gap-2 rounded-lg border border-destructive/20 bg-destructive/10 px-3 py-2 text-sm text-destructive">
            <AlertCircle className="mt-0.5 size-4 shrink-0" />
            <span>{error}</span>
          </div>
        ) : null}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <Button type="submit" disabled={isSubmitting} className="mt-1">
            {isSubmitting ? "Sending…" : "Send reset link"}
          </Button>
        </form>

        <p className="text-center text-sm text-muted-foreground">
          Remembered your password?{" "}
          <Link href="/login" className="font-medium text-primary transition-colors hover:text-primary-hover">
            Sign in
          </Link>
        </p>
      </CardContent>
    </Card>
  )
}
