import type { Metadata } from "next"
import {
  ChartSpline,
  FlaskConical,
  GraduationCap,
  HeartPulse,
  type LucideIcon,
} from "lucide-react"

import { AppHeader } from "@/components/layout/app-header"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"

type Agent = {
  name: string
  tagline: string
  description: string
  icon: LucideIcon
  capabilities: string[]
  context: string
  suggestedActions: string[]
}

const AGENTS: Agent[] = [
  {
    name: "Research Agent",
    tagline: "Research workspace",
    description:
      "Synthesizes literature and validates study design against your dataset library.",
    icon: FlaskConical,
    capabilities: [
      "Literature synthesis",
      "Study design review",
      "Statistical validation",
    ],
    context: "Working from 342 validated reports across 18 active studies.",
    suggestedActions: [
      "Summarize recent cortisol rhythm literature",
      "Review power analysis for Study 14",
      "Flag confounds in the PCOS biomarker batch",
    ],
  },
  {
    name: "Data Scientist Agent",
    tagline: "Analytical modeling",
    description:
      "Runs quantitative analysis across uploaded datasets to surface trends and outliers.",
    icon: ChartSpline,
    capabilities: [
      "Dataset analysis",
      "Anomaly detection",
      "Correlation modeling",
    ],
    context: "Connected to all 124 datasets in the research workspace.",
    suggestedActions: [
      "Detect anomalies in Testosterone Replacement Outcomes",
      "Model correlation between TSH and BMI",
      "Generate a cohort comparison summary",
    ],
  },
  {
    name: "Hormone Education Agent",
    tagline: "Approachable & safe",
    description:
      "Explains hormone concepts in plain language, grounded in trusted sources — not a diagnosis tool.",
    icon: HeartPulse,
    capabilities: [
      "Plain-language explanations",
      "Symptom context (non-diagnostic)",
      "Trusted source citations",
    ],
    context: "Responses are educational only and always cite sources.",
    suggestedActions: [
      "Explain what cortisol does in the body",
      "What affects thyroid hormone levels?",
      "Summarize estrogen's role across the cycle",
    ],
  },
  {
    name: "Student Mentor",
    tagline: "Educational guidance",
    description:
      "Walks students through endocrinology concepts with structured explanations and practice questions.",
    icon: GraduationCap,
    capabilities: [
      "Concept walkthroughs",
      "Study guidance",
      "Practice questions",
    ],
    context: "Paced for coursework in endocrinology and physiology.",
    suggestedActions: [
      "Walk through the HPA axis feedback loop",
      "Quiz me on thyroid hormone regulation",
      "Explain negative vs. positive feedback with examples",
    ],
  },
]

const EXAMPLE_CONVERSATION = [
  {
    role: "user" as const,
    text: "Why does my cortisol feel higher in the morning?",
  },
  {
    role: "agent" as const,
    text: "Cortisol follows a daily rhythm called the diurnal curve — it naturally peaks about 30-45 minutes after waking (the cortisol awakening response) and declines through the day. This is a normal regulatory pattern, not necessarily a sign of stress.",
  },
]

export const metadata: Metadata = {
  title: "AI Agents",
}

export default function AgentsPage() {
  return (
    <div className="flex flex-1 flex-col">
      <AppHeader
        title="AI Agents"
        description="Specialized research and education agents for hormone data."
      />

      <div className="flex flex-1 flex-col gap-6 p-4 sm:p-6">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {AGENTS.map((agent) => (
            <AgentCard key={agent.name} agent={agent} />
          ))}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Example: Hormone Education Agent</CardTitle>
            <CardDescription>
              A preview of how the conversation surface is framed — grounded,
              cited, and non-diagnostic.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-3 rounded-lg border border-border bg-muted/40 p-4">
              {EXAMPLE_CONVERSATION.map((turn, i) => (
                <div key={i} className="flex flex-col gap-1">
                  <span className="text-xs font-medium text-muted-foreground">
                    {turn.role === "user" ? "You" : "Hormone Education Agent"}
                  </span>
                  <p
                    className={
                      turn.role === "agent"
                        ? "text-sm text-foreground"
                        : "text-sm font-medium text-foreground"
                    }
                  >
                    {turn.text}
                  </p>
                </div>
              ))}
              <Separator />
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">Source:</span>
                <Badge variant="outline">Endocrine Society Clinical Guidelines</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function AgentCard({ agent }: { agent: Agent }) {
  const Icon = agent.icon

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start gap-3">
          <div className="flex size-10 shrink-0 items-center justify-center rounded-lg border border-border bg-muted">
            <Icon className="size-5 text-primary" />
          </div>
          <div className="flex min-w-0 flex-col gap-0.5">
            <CardTitle>{agent.name}</CardTitle>
            <span className="text-xs text-muted-foreground">
              {agent.tagline}
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <CardDescription>{agent.description}</CardDescription>

        <div className="flex flex-col gap-1.5">
          <span className="text-xs font-medium text-foreground">
            Capabilities
          </span>
          <div className="flex flex-wrap gap-1.5">
            {agent.capabilities.map((c) => (
              <Badge key={c} variant="outline">
                {c}
              </Badge>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-1.5">
          <span className="text-xs font-medium text-foreground">Context</span>
          <p className="text-sm text-muted-foreground">{agent.context}</p>
        </div>

        <div className="flex flex-col gap-1.5">
          <span className="text-xs font-medium text-foreground">
            Suggested actions
          </span>
          <ul className="flex flex-col gap-1">
            {agent.suggestedActions.map((action) => (
              <li
                key={action}
                className="text-sm text-muted-foreground before:mr-1.5 before:text-border before:content-['—']"
              >
                {action}
              </li>
            ))}
          </ul>
        </div>

        <Button className="w-full">Open {agent.name}</Button>
      </CardContent>
    </Card>
  )
}
