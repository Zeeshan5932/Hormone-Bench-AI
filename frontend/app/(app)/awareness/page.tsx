import type { Metadata } from "next"
import { Clock } from "lucide-react"

import { AppHeader } from "@/components/layout/app-header"
import { Card } from "@/components/ui/card"

const CATEGORIES = [
  "All",
  "Thyroid",
  "Reproductive Health",
  "Metabolic",
  "Stress & Cortisol",
  "Aging",
]

const FEATURED_ARTICLE = {
  category: "Stress & Cortisol",
  title: "Understanding Cortisol and the Stress Response",
  excerpt:
    "Cortisol is often reduced to a single label — 'the stress hormone' — but its role in metabolism, immune regulation, and circadian timing is far more nuanced. This overview walks through how cortisol is produced, why it follows a daily rhythm, and what sustained elevation actually does to the body.",
  author: "Dr. R. Nandakumar",
  readTime: "8 min read",
  date: "Aug 12, 2026",
}

const ARTICLES = [
  {
    category: "Thyroid",
    title: "Thyroid Function: What Your Labs Actually Mean",
    excerpt:
      "TSH, free T4, free T3 — a plain-language guide to interpreting a standard thyroid panel and why reference ranges vary between labs.",
    author: "S. Whitfield",
    readTime: "6 min read",
    date: "Aug 10, 2026",
  },
  {
    category: "Reproductive Health",
    title: "PCOS and Insulin Resistance Explained",
    excerpt:
      "How insulin resistance contributes to the hormonal pattern seen in polycystic ovary syndrome, and what the current evidence supports for management.",
    author: "Dr. M. Osei",
    readTime: "7 min read",
    date: "Aug 8, 2026",
  },
  {
    category: "Reproductive Health",
    title: "Estrogen Across the Menstrual Cycle",
    excerpt:
      "A stage-by-stage look at how estrogen levels shift through the follicular, ovulatory, and luteal phases, and why timing matters for testing.",
    author: "J. Alvarez",
    readTime: "5 min read",
    date: "Aug 5, 2026",
  },
  {
    category: "Metabolic",
    title: "Testosterone Therapy: Evidence and Considerations",
    excerpt:
      "A balanced review of what clinical trials show about testosterone replacement therapy, including benefits, risks, and open questions.",
    author: "Dr. R. Nandakumar",
    readTime: "9 min read",
    date: "Aug 3, 2026",
  },
  {
    category: "Aging",
    title: "Melatonin and Circadian Rhythm Health",
    excerpt:
      "Melatonin's role extends well beyond sleep onset. Here's how light exposure, age, and shift work interact with the body's natural rhythm.",
    author: "S. Whitfield",
    readTime: "5 min read",
    date: "Jul 30, 2026",
  },
  {
    category: "Metabolic",
    title: "Growth Hormone: Myths vs. Evidence",
    excerpt:
      "Separating popular claims about growth hormone from what peer-reviewed research actually demonstrates in adults.",
    author: "Dr. M. Osei",
    readTime: "6 min read",
    date: "Jul 27, 2026",
  },
  {
    category: "Aging",
    title: "Perimenopause: A Clinical Overview",
    excerpt:
      "The hormonal transitions that define perimenopause, common symptoms, and how clinicians approach evaluation and support.",
    author: "J. Alvarez",
    readTime: "8 min read",
    date: "Jul 24, 2026",
  },
  {
    category: "Thyroid",
    title: "Hashimoto's Thyroiditis: Recognizing Early Signs",
    excerpt:
      "An overview of the autoimmune process behind Hashimoto's thyroiditis and the early laboratory and symptom markers to watch for.",
    author: "Dr. R. Nandakumar",
    readTime: "6 min read",
    date: "Jul 20, 2026",
  },
]

export const metadata: Metadata = {
  title: "Awareness Center",
}

export default function AwarenessPage() {
  return (
    <div className="flex flex-1 flex-col">
      <AppHeader
        title="Awareness Center"
        description="Evidence-based education on hormone health, written for clarity."
      />

      <div className="flex flex-1 flex-col gap-8 p-4 sm:p-6">
        <nav aria-label="Categories" className="flex flex-wrap gap-x-5 gap-y-2">
          {CATEGORIES.map((category, index) => (
            <button
              key={category}
              type="button"
              className={
                index === 0
                  ? "text-sm font-medium text-foreground"
                  : "text-sm text-muted-foreground transition-colors hover:text-foreground"
              }
            >
              {category}
            </button>
          ))}
        </nav>

        <Card className="overflow-hidden p-0">
          <div className="grid grid-cols-1 lg:grid-cols-2">
            <div className="aspect-video w-full bg-muted lg:aspect-auto" />
            <div className="flex flex-col justify-center gap-3 p-6 sm:p-8">
              <span className="text-xs font-medium uppercase tracking-wide text-secondary">
                Featured · {FEATURED_ARTICLE.category}
              </span>
              <h2 className="text-2xl font-medium leading-snug text-foreground sm:text-3xl">
                {FEATURED_ARTICLE.title}
              </h2>
              <p className="max-w-[60ch] text-base leading-relaxed text-muted-foreground">
                {FEATURED_ARTICLE.excerpt}
              </p>
              <div className="flex items-center gap-2 pt-2 text-xs text-muted-foreground">
                <span>{FEATURED_ARTICLE.author}</span>
                <span aria-hidden="true">·</span>
                <span className="inline-flex items-center gap-1">
                  <Clock className="size-3.5" />
                  {FEATURED_ARTICLE.readTime}
                </span>
                <span aria-hidden="true">·</span>
                <span>{FEATURED_ARTICLE.date}</span>
              </div>
            </div>
          </div>
        </Card>

        <div>
          <h3 className="mb-4 text-lg font-semibold text-foreground">
            All Articles
          </h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {ARTICLES.map((article) => (
              <Card
                key={article.title}
                className="overflow-hidden p-0"
              >
                <div className="aspect-video w-full bg-muted" />
                <div className="flex flex-col gap-2 p-5">
                  <span className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                    {article.category}
                  </span>
                  <h4 className="text-base font-medium leading-snug text-foreground">
                    {article.title}
                  </h4>
                  <p className="line-clamp-2 text-sm leading-relaxed text-muted-foreground">
                    {article.excerpt}
                  </p>
                  <div className="flex items-center gap-2 pt-1 text-xs text-muted-foreground">
                    <span>{article.author}</span>
                    <span aria-hidden="true">·</span>
                    <span>{article.readTime}</span>
                    <span aria-hidden="true">·</span>
                    <span>{article.date}</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
