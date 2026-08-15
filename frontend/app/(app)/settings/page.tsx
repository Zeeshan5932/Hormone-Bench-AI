import type { Metadata } from "next"
import {
  Camera,
  KeyRound,
  ShieldCheck,
  UserPlus,
} from "lucide-react"

import { AppHeader } from "@/components/layout/app-header"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Switch } from "@/components/ui/switch"

const NOTIFICATION_PREFERENCES = [
  {
    id: "dataset-validation",
    label: "Dataset validation complete",
    description:
      "Get notified when an uploaded dataset finishes validation.",
    defaultChecked: true,
  },
  {
    id: "study-shared",
    label: "New research study shared with you",
    description: "Alerts when a collaborator shares a study with your team.",
    defaultChecked: true,
  },
  {
    id: "weekly-digest",
    label: "Weekly research digest",
    description: "A summary of activity across your research workspace.",
    defaultChecked: false,
  },
  {
    id: "security-alerts",
    label: "Security alerts",
    description: "Sign-in attempts and other important account activity.",
    defaultChecked: true,
  },
]

const TEAM_MEMBERS = [
  {
    name: "Dr. R. Nandakumar",
    email: "r.nandakumar@hormonebench.ai",
    initials: "RN",
    role: "Admin" as const,
  },
  {
    name: "S. Whitfield",
    email: "s.whitfield@hormonebench.ai",
    initials: "SW",
    role: "Researcher" as const,
  },
  {
    name: "Dr. M. Osei",
    email: "m.osei@hormonebench.ai",
    initials: "MO",
    role: "Researcher" as const,
  },
  {
    name: "J. Alvarez",
    email: "j.alvarez@hormonebench.ai",
    initials: "JA",
    role: "Viewer" as const,
  },
]

const ROLE_BADGE_VARIANT: Record<
  (typeof TEAM_MEMBERS)[number]["role"],
  "default" | "secondary" | "outline"
> = {
  Admin: "default",
  Researcher: "secondary",
  Viewer: "outline",
}

export const metadata: Metadata = {
  title: "Settings",
}

export default function SettingsPage() {
  return (
    <div className="flex flex-1 flex-col">
      <AppHeader
        title="Settings"
        description="Manage your account, notifications, and workspace preferences."
      />

      <div className="flex flex-1 flex-col gap-6 p-4 sm:p-6">
        {/* Profile */}
        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
            <CardDescription>
              Update your personal information and how it appears to your
              team.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-6">
            <div className="flex items-center gap-4">
              <Avatar size="lg">
                <AvatarFallback>AH</AvatarFallback>
              </Avatar>
              <Button variant="outline" size="sm">
                <Camera />
                Change photo
              </Button>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="full-name">Full name</Label>
                <Input id="full-name" defaultValue="Ali Hangar" />
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  defaultValue="ali@hangardirect.com"
                />
              </div>
              <div className="flex flex-col gap-1.5 sm:col-span-2">
                <Label htmlFor="role-title">Role / title</Label>
                <Input
                  id="role-title"
                  defaultValue="Principal Investigator, Endocrinology"
                />
              </div>
            </div>
          </CardContent>
          <CardFooter className="justify-end">
            <Button>Save changes</Button>
          </CardFooter>
        </Card>

        {/* Notifications */}
        <Card>
          <CardHeader>
            <CardTitle>Notifications</CardTitle>
            <CardDescription>
              Choose which updates you&apos;d like to receive.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col">
            {NOTIFICATION_PREFERENCES.map((pref, index) => (
              <div key={pref.id}>
                {index > 0 ? <Separator className="my-4" /> : null}
                <div className="flex items-start justify-between gap-4">
                  <div className="flex flex-col gap-0.5">
                    <Label htmlFor={pref.id} className="text-sm">
                      {pref.label}
                    </Label>
                    <p className="text-sm text-muted-foreground">
                      {pref.description}
                    </p>
                  </div>
                  <Switch
                    id={pref.id}
                    defaultChecked={pref.defaultChecked}
                    className="mt-0.5 shrink-0"
                  />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Security */}
        <Card>
          <CardHeader>
            <CardTitle>Security</CardTitle>
            <CardDescription>
              Manage your password and account protection.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-6">
            <div className="flex flex-col gap-4">
              <div className="flex items-center gap-2 text-sm font-medium text-foreground">
                <KeyRound className="size-4 text-muted-foreground" />
                Change password
              </div>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div className="flex flex-col gap-1.5 sm:col-span-2">
                  <Label htmlFor="current-password">Current password</Label>
                  <Input id="current-password" type="password" />
                </div>
                <div className="flex flex-col gap-1.5">
                  <Label htmlFor="new-password">New password</Label>
                  <Input id="new-password" type="password" />
                </div>
                <div className="flex flex-col gap-1.5">
                  <Label htmlFor="confirm-password">Confirm password</Label>
                  <Input id="confirm-password" type="password" />
                </div>
              </div>
            </div>

            <Separator />

            <div className="flex items-start justify-between gap-4">
              <div className="flex flex-col gap-0.5">
                <div className="flex items-center gap-2 text-sm font-medium text-foreground">
                  <ShieldCheck className="size-4 text-muted-foreground" />
                  Two-factor authentication
                </div>
                <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                  <Badge variant="success">Enabled</Badge>
                  <span>Your account is protected with an authenticator app.</span>
                </div>
              </div>
              <Switch defaultChecked className="mt-0.5 shrink-0" />
            </div>
          </CardContent>
          <CardFooter className="justify-end">
            <Button>Update password</Button>
          </CardFooter>
        </Card>

        {/* Workspace / Team */}
        <Card>
          <CardHeader>
            <CardTitle>Workspace members</CardTitle>
            <CardDescription>
              People with access to this research workspace.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col">
            {TEAM_MEMBERS.map((member, index) => (
              <div key={member.email}>
                {index > 0 ? <Separator className="my-4" /> : null}
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <Avatar>
                      <AvatarFallback>{member.initials}</AvatarFallback>
                    </Avatar>
                    <div className="flex flex-col">
                      <span className="text-sm font-medium text-foreground">
                        {member.name}
                      </span>
                      <span className="text-sm text-muted-foreground">
                        {member.email}
                      </span>
                    </div>
                  </div>
                  <Badge variant={ROLE_BADGE_VARIANT[member.role]}>
                    {member.role}
                  </Badge>
                </div>
              </div>
            ))}
          </CardContent>
          <CardFooter className="justify-end">
            <Button variant="outline">
              <UserPlus />
              Invite member
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  )
}
