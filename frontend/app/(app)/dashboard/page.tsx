import type { Metadata } from "next"
import { Database, FlaskConical, FileCheck2, Users } from "lucide-react"

import { AppHeader } from "@/components/layout/app-header"
import { StatCard } from "@/components/dashboard/stat-card"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const MONTHLY_UPLOADS = [
  { month: "Mar", value: 42 },
  { month: "Apr", value: 58 },
  { month: "May", value: 51 },
  { month: "Jun", value: 67 },
  { month: "Jul", value: 74 },
  { month: "Aug", value: 88 },
]

const RECENT_DATASETS = [
  {
    name: "Cortisol Rhythm Cohort — Study 14",
    author: "Dr. R. Nandakumar",
    updated: "2h ago",
    status: "validated" as const,
  },
  {
    name: "Thyroid Panel, Adult Female 25-45",
    author: "S. Whitfield",
    updated: "5h ago",
    status: "processing" as const,
  },
  {
    name: "Testosterone Replacement Outcomes",
    author: "Dr. M. Osei",
    updated: "1d ago",
    status: "needs-review" as const,
  },
  {
    name: "Estradiol Longitudinal Panel",
    author: "J. Alvarez",
    updated: "2d ago",
    status: "draft" as const,
  },
  {
    name: "PCOS Biomarker Intake Batch 7",
    author: "Dr. R. Nandakumar",
    updated: "3d ago",
    status: "failed" as const,
  },
]

export const metadata: Metadata = {
  title: "Dashboard",
}

export default function DashboardPage() {
  const maxValue = Math.max(...MONTHLY_UPLOADS.map((d) => d.value))

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader
        title="Dashboard"
        description="Overview of research activity and platform health"
      />

      <div className="flex flex-1 flex-col gap-6 p-4 sm:p-6">
        <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">
              Welcome back, Ali
            </h2>
            <p className="text-sm text-muted-foreground">
              Here&apos;s what&apos;s happening across your research workspace.
            </p>
          </div>
          <Button>Upload Dataset</Button>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            label="Datasets"
            value="124"
            icon={Database}
            trend={{ direction: "up", value: "+12", label: "this month" }}
          />
          <StatCard
            label="Active Studies"
            value="18"
            icon={FlaskConical}
            trend={{ direction: "up", value: "+3", label: "this month" }}
          />
          <StatCard
            label="Validated Reports"
            value="342"
            icon={FileCheck2}
            trend={{ direction: "up", value: "+27", label: "this month" }}
          />
          <StatCard
            label="Research Members"
            value="56"
            icon={Users}
            trend={{ direction: "down", value: "-2", label: "this month" }}
          />
        </div>

        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Dataset Uploads</CardTitle>
              <CardDescription>Monthly volume, last 6 months</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex h-48 items-end gap-3 sm:gap-4">
                {MONTHLY_UPLOADS.map((d) => (
                  <div
                    key={d.month}
                    className="flex flex-1 flex-col items-center gap-2"
                  >
                    <div className="flex h-40 w-full items-end">
                      <div
                        className="w-full rounded-t-sm bg-primary transition-colors"
                        style={{
                          height: `${(d.value / maxValue) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {d.month}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Validation Status</CardTitle>
              <CardDescription>Across all active datasets</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              {[
                { label: "Validated", value: 68, color: "bg-success" },
                { label: "Processing", value: 14, color: "bg-secondary" },
                { label: "Needs Review", value: 12, color: "bg-warning" },
                { label: "Failed", value: 6, color: "bg-destructive" },
              ].map((row) => (
                <div key={row.label} className="flex flex-col gap-1.5">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-foreground">{row.label}</span>
                    <span className="font-medium text-muted-foreground">
                      {row.value}%
                    </span>
                  </div>
                  <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
                    <div
                      className={`h-full rounded-full ${row.color}`}
                      style={{ width: `${row.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Recent Datasets</CardTitle>
            <CardDescription>
              Latest uploads across your research teams
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Dataset</TableHead>
                  <TableHead>Author</TableHead>
                  <TableHead>Updated</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {RECENT_DATASETS.map((row) => (
                  <TableRow key={row.name}>
                    <TableCell className="font-medium text-foreground">
                      {row.name}
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {row.author}
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {row.updated}
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={row.status} />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
