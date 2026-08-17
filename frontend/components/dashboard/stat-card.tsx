import type { LucideIcon } from "lucide-react"
import { ArrowDown, ArrowUp } from "lucide-react"

import { cn } from "@/lib/utils"
import { Card, CardContent } from "@/components/ui/card"

export function StatCard({
  label,
  value,
  icon: Icon,
  trend,
}: {
  label: string
  value: string
  icon: LucideIcon
  trend?: {
    direction: "up" | "down"
    value: string
    label: string
  }
}) {
  return (
    <Card>
      <CardContent className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-1.5">
          <span className="text-sm text-muted-foreground">{label}</span>
          <span className="text-2xl font-semibold tracking-tight text-foreground">
            {value}
          </span>
          {trend ? (
            <span className="flex items-center gap-1 text-xs">
              <span
                className={cn(
                  "flex items-center gap-0.5 font-medium",
                  trend.direction === "up" ? "text-success" : "text-destructive"
                )}
              >
                {trend.direction === "up" ? (
                  <ArrowUp className="size-3" />
                ) : (
                  <ArrowDown className="size-3" />
                )}
                {trend.value}
              </span>
              <span className="text-muted-foreground">{trend.label}</span>
            </span>
          ) : null}
        </div>
        <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted text-primary">
          <Icon className="size-4.5" />
        </span>
      </CardContent>
    </Card>
  )
}
