import Link from "next/link"
import {
  ArrowRight,
  FlaskConical,
  GraduationCap,
  HeartPulse,
  Stethoscope,
  Microscope,
  Bot,
  Salad,
  PenTool,
  ChartSpline,
  BookOpen,
  Users,
  Library,
  Trophy,
  Newspaper,
  Network,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { AssayStrip } from "@/components/marketing/assay-strip"
import { Logo } from "@/components/layout/logo"

const NAV_LINKS = [
  { label: "Research", href: "#audiences" },
  { label: "AI Agents", href: "#agents" },
  { label: "Learn", href: "#audiences" },
  { label: "Awareness", href: "#modules" },
  { label: "Resources", href: "#modules" },
  { label: "Community", href: "#modules" },
]

const AUDIENCES = [
  {
    icon: Microscope,
    ref: "Audience A",
    title: "Research Hub",
    subtitle: "Researchers & Universities",
    description:
      "The flagship platform for scientific research on hormonal health, from raw data to publication.",
    features: [
      "Multi-dataset upload (CSV, Excel)",
      "AI dataset validator",
      "Dataset cards & model cards",
      "Benchmark leaderboards",
      "Explainable AI",
      "Research Copilot",
      "Biomedical knowledge graph",
      "Statistical analysis",
      "Open API & collaboration workspace",
    ],
  },
  {
    icon: GraduationCap,
    ref: "Audience B",
    title: "Student Academy",
    subtitle: "Students & Learners",
    description:
      "A complete learning portal for students interested in AI, medicine, biology, and public health.",
    features: [
      "Women's Hormonal Health 101",
      "Endocrinology basics",
      "PCOS, thyroid disorders, menopause",
      "AI in healthcare & biomedical data science",
      "Research methodology & scientific writing",
      "AI Tutor for interactive explanations",
    ],
  },
  {
    icon: HeartPulse,
    ref: "Audience C",
    title: "Patient Awareness Center",
    subtitle: "The Public",
    description:
      "Education only, never diagnosis — clear, calm, and trustworthy information on hormonal health.",
    features: [
      "Understanding hormones & menstrual health",
      "PCOS, endometriosis, menopause, fertility",
      "Simple explanations & visual diagrams",
      "Myth vs. fact",
      "When to seek medical care",
      "Trusted resources",
    ],
  },
  {
    icon: Stethoscope,
    ref: "Audience D",
    title: "Healthcare Professional Portal",
    subtitle: "Clinicians, Nutritionists & Researchers",
    description:
      "Evidence-based tools designed for the pace and rigor of clinical and applied research work.",
    features: [
      "Clinical guidelines & biomarker references",
      "Research summaries & literature updates",
      "Evidence explorer",
      "Dataset repository",
      "AI validation tools",
      "Collaboration",
    ],
  },
]

const AGENTS = [
  {
    icon: FlaskConical,
    name: "Research Agent",
    audience: "For scientists",
    description:
      "Analyzes datasets, recommends preprocessing, benchmarks models, and finds literature.",
  },
  {
    icon: GraduationCap,
    name: "Student Mentor Agent",
    audience: "For students",
    description:
      "Teaches concepts, quizzes users, generates study notes and flashcards.",
  },
  {
    icon: HeartPulse,
    name: "Hormone Education Agent",
    audience: "For the public",
    description:
      "Answers everyday questions on cycles, hormones, and lifestyle — always pointing toward professional care.",
  },
  {
    icon: Salad,
    name: "Nutrition Agent",
    audience: "Dietitian-reviewed",
    description:
      "Explains balanced diets and nutrients tied to hormonal health, without personalized medical therapy.",
  },
  {
    icon: PenTool,
    name: "Research Writing Agent",
    audience: "For researchers",
    description:
      "Drafts literature reviews, abstracts, methods sections, and grant applications.",
  },
  {
    icon: ChartSpline,
    name: "Data Scientist Agent",
    audience: "For research teams",
    description:
      "Detects missing values and outliers, recommends models, evaluates fairness, generates Python.",
  },
]

const MODULES = [
  {
    icon: BookOpen,
    title: "Awareness Center",
    description: "Daily articles, myth busters, expert interviews, and research highlights.",
  },
  {
    icon: Users,
    title: "Community",
    description: "Forums, student groups, research groups, Women in STEM, university chapters.",
  },
  {
    icon: Library,
    title: "Resource Library",
    description: "Research papers, clinical guidelines, open datasets, books, and courses.",
  },
  {
    icon: Trophy,
    title: "Research Challenges",
    description: "Monthly AI competitions, dataset challenges, leaderboards, and hackathons.",
  },
  {
    icon: Newspaper,
    title: "Publications",
    description: "Research outputs, preprints, case studies, white papers, and conference papers.",
  },
  {
    icon: Network,
    title: "Expert Network",
    description: "Endocrinologists, gynecologists, nutritionists, epidemiologists, and data scientists.",
  },
]

const JOURNEYS = [
  {
    audience: "Researchers",
    steps: ["Upload datasets", "AI validation", "Benchmark", "Reports", "Publish"],
  },
  {
    audience: "Students",
    steps: ["Learn", "AI Tutor", "Quizzes", "Certificates", "Projects"],
  },
  {
    audience: "Patients",
    steps: ["Awareness", "Educational AI", "Lifestyle guidance", "Resources", "Professional care"],
  },
  {
    audience: "Healthcare Professionals",
    steps: ["Evidence", "Guidelines", "Research", "Collaboration"],
  },
]

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-border bg-background">
        <div className="mx-auto grid max-w-6xl grid-cols-[auto_1fr_auto] items-center gap-6 px-6 py-3">
          <Logo height={36} />
          <nav className="hidden items-center justify-center gap-6 lg:flex">
            {NAV_LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-sm whitespace-nowrap text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
              </a>
            ))}
          </nav>
          <div className="flex items-center justify-end gap-3">
            <Button variant="outline" size="sm" render={<Link href="/login" />}>
              Sign in
            </Button>
            <Button size="sm" render={<Link href="/signup" />}>
              Get started
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <section className="border-b border-border bg-background">
          <div className="mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 px-6 py-16 sm:py-20 lg:grid-cols-2 lg:gap-16 lg:py-24">
            <div className="order-2 flex flex-col gap-6 lg:order-1">
              <span className="font-mono text-xs uppercase tracking-[0.08em] text-secondary">
                An AI ecosystem for women&apos;s hormonal health
              </span>
              <h1 className="font-serif text-4xl leading-[1.1] tracking-tight text-foreground sm:text-5xl">
                Research, education, and care — instrumented and evidence-grade.
              </h1>
              <p className="max-w-md text-base leading-7 text-muted-foreground">
                HormoneBench AI advances women&apos;s hormonal health through
                research, education, clinical decision support, and public
                awareness — serving researchers, students, patients, and
                healthcare professionals in one trusted workspace.
              </p>
              <div className="flex flex-col gap-3 sm:flex-row">
                <Button size="lg" render={<Link href="/login" />}>
                  Enter the platform
                  <ArrowRight />
                </Button>
                <Button size="lg" variant="outline" render={<Link href="#audiences" />}>
                  Explore the ecosystem
                </Button>
              </div>
            </div>

            <div className="order-1 flex items-center rounded-xl border border-border bg-card p-6 lg:order-2">
              <AssayStrip />
            </div>
          </div>
        </section>

        <section id="audiences" className="bg-background">
          <div className="mx-auto max-w-6xl px-6 py-20 sm:py-24">
            <div className="mb-12 flex flex-col gap-3 border-b border-border pb-6">
              <span className="font-mono text-xs uppercase tracking-[0.08em] text-muted-foreground">
                The ecosystem
              </span>
              <h2 className="font-serif text-2xl text-foreground sm:text-3xl">
                Built for four audiences, not just researchers
              </h2>
              <p className="max-w-2xl text-base text-muted-foreground">
                Every audience gets tools scoped to how they actually work —
                nothing generic, nothing borrowed from an unrelated product.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
              {AUDIENCES.map((audience) => (
                <Card key={audience.title} className="gap-4">
                  <CardHeader className="gap-2">
                    <div className="flex items-center justify-between font-mono text-[11px] uppercase tracking-[0.08em] text-muted-foreground">
                      <span>{audience.ref}</span>
                      <span className="text-secondary">{audience.subtitle}</span>
                    </div>
                    <span className="flex size-9 items-center justify-center rounded-lg bg-muted text-primary">
                      <audience.icon className="size-4.5" />
                    </span>
                    <CardTitle className="text-base">{audience.title}</CardTitle>
                    <CardDescription>{audience.description}</CardDescription>
                  </CardHeader>
                  <ul className="flex flex-col gap-1.5 border-t border-border px-6 pt-4 pb-2">
                    {audience.features.map((feature) => (
                      <li
                        key={feature}
                        className="flex items-baseline gap-2 text-sm text-foreground"
                      >
                        <span className="mt-1.5 size-1 shrink-0 rounded-full bg-secondary" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section id="agents" className="border-t border-border bg-muted/50">
          <div className="mx-auto max-w-6xl px-6 py-20 sm:py-24">
            <div className="mb-12 flex flex-col gap-3 border-b border-border pb-6">
              <span className="font-mono text-xs uppercase tracking-[0.08em] text-muted-foreground">
                AI agents
              </span>
              <h2 className="font-serif text-2xl text-foreground sm:text-3xl">
                Six specialists, not one generic chatbot
              </h2>
              <p className="max-w-2xl text-base text-muted-foreground">
                Each agent is scoped to a role and a real workflow — differentiated
                by purpose and content, not by color.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {AGENTS.map((agent) => (
                <Card key={agent.name}>
                  <CardHeader className="gap-2">
                    <span className="flex size-9 items-center justify-center rounded-lg bg-background text-primary ring-1 ring-border">
                      <agent.icon className="size-4.5" />
                    </span>
                    <span className="font-mono text-[11px] uppercase tracking-[0.08em] text-secondary">
                      {agent.audience}
                    </span>
                    <CardTitle className="text-base">{agent.name}</CardTitle>
                    <CardDescription>{agent.description}</CardDescription>
                  </CardHeader>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <section id="modules" className="border-t border-border bg-background">
          <div className="mx-auto max-w-6xl px-6 py-20 sm:py-24">
            <div className="mb-12 flex flex-col gap-3 border-b border-border pb-6">
              <span className="font-mono text-xs uppercase tracking-[0.08em] text-muted-foreground">
                Platform modules
              </span>
              <h2 className="font-serif text-2xl text-foreground sm:text-3xl">
                Everything around the research, in one place
              </h2>
            </div>

            <div className="grid grid-cols-1 gap-px overflow-hidden rounded-xl border border-border bg-border sm:grid-cols-2 lg:grid-cols-3">
              {MODULES.map((module) => (
                <div key={module.title} className="flex flex-col gap-3 bg-card p-6">
                  <span className="flex size-9 items-center justify-center rounded-lg bg-muted text-primary">
                    <module.icon className="size-4.5" />
                  </span>
                  <h3 className="text-base font-semibold text-foreground">
                    {module.title}
                  </h3>
                  <p className="text-sm leading-6 text-muted-foreground">
                    {module.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="journeys" className="border-t border-border bg-muted/50">
          <div className="mx-auto max-w-6xl px-6 py-20 sm:py-24">
            <div className="mb-12 flex flex-col gap-3 border-b border-border pb-6">
              <span className="font-mono text-xs uppercase tracking-[0.08em] text-muted-foreground">
                User journeys
              </span>
              <h2 className="font-serif text-2xl text-foreground sm:text-3xl">
                A clear path for every audience
              </h2>
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              {JOURNEYS.map((journey) => (
                <div
                  key={journey.audience}
                  className="flex flex-col gap-3 rounded-xl border border-border bg-card p-6"
                >
                  <span className="text-sm font-semibold text-foreground">
                    {journey.audience}
                  </span>
                  <div className="flex flex-wrap items-center gap-2">
                    {journey.steps.map((step, i) => (
                      <div key={step} className="flex items-center gap-2">
                        <span className="rounded-md bg-muted px-2.5 py-1 text-xs font-medium text-foreground">
                          {step}
                        </span>
                        {i < journey.steps.length - 1 ? (
                          <ArrowRight className="size-3.5 text-muted-foreground" />
                        ) : null}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="border-t border-border bg-background">
          <div className="mx-auto flex max-w-3xl flex-col items-center gap-4 px-6 py-20 text-center sm:py-24">
            <span className="flex size-10 items-center justify-center rounded-lg bg-muted text-primary">
              <Bot className="size-5" />
            </span>
            <h2 className="font-serif text-2xl text-foreground sm:text-3xl">
              The world&apos;s first open AI ecosystem for women&apos;s hormonal health
            </h2>
            <p className="max-w-xl text-base leading-7 text-muted-foreground">
              Where researchers accelerate discovery, students build expertise,
              healthcare professionals access evidence-based resources, and the
              public learns through trusted, AI-assisted education.
            </p>
            <p className="max-w-lg text-xs text-muted-foreground">
              HormoneBench AI provides educational information and is not a
              substitute for professional medical advice, diagnosis, or treatment.
            </p>
          </div>
        </section>

        <section className="border-t border-border bg-background">
          <div className="mx-auto flex max-w-6xl flex-col items-center gap-6 px-6 py-20 text-center sm:py-24">
            <h2 className="font-serif text-2xl text-foreground sm:text-3xl">
              Bring structure to your hormone research today
            </h2>
            <p className="max-w-xl text-base text-muted-foreground">
              Upload your first dataset, run it through validation, and see
              the platform in action.
            </p>
            <Button size="lg" render={<Link href="/signup" />}>
              Get started
              <ArrowRight />
            </Button>
          </div>
        </section>
      </main>

      <footer className="border-t border-border bg-background">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 py-8 text-sm text-muted-foreground sm:flex-row">
          <span>© {new Date().getFullYear()} HormoneBench AI</span>
          <span className="font-mono text-xs">Research-grade hormone data platform</span>
        </div>
      </footer>
    </div>
  )
}
