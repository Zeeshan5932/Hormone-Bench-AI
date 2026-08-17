import { Badge } from "@/components/ui/badge"

export type ResearchStatus =
  | "validated"
  | "processing"
  | "needs-review"
  | "failed"
  | "draft"

const STATUS_CONFIG: Record<
  ResearchStatus,
  { label: string; variant: "success" | "info" | "warning" | "destructive" | "outline" }
> = {
  validated: { label: "Validated", variant: "success" },
  processing: { label: "Processing", variant: "info" },
  "needs-review": { label: "Needs Review", variant: "warning" },
  failed: { label: "Failed", variant: "destructive" },
  draft: { label: "Draft", variant: "outline" },
}

export function StatusBadge({ status }: { status: ResearchStatus }) {
  const config = STATUS_CONFIG[status]
  return <Badge variant={config.variant}>{config.label}</Badge>
}
