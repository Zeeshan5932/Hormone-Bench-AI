import type { Metadata } from "next";
import { Download, ExternalLink, Search } from "lucide-react";

import { AppHeader } from "@/components/layout/app-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

type ResourceType = "Paper" | "Dataset" | "Guideline" | "Report";

interface Resource {
  title: string;
  type: ResourceType;
  category: string;
  author: string;
  date: string;
  tags: string[];
}

const RESOURCE_TYPE_VARIANT: Record<
  ResourceType,
  "default" | "secondary" | "outline"
> = {
  Paper: "outline",
  Dataset: "secondary",
  Guideline: "default",
  Report: "outline",
};

const resources: Resource[] = [
  {
    title: "Cortisol Circadian Rhythm: A Systematic Review",
    type: "Paper",
    category: "Adrenal",
    author: "Dr. Elena Marsh",
    date: "2026-06-02",
    tags: ["Cortisol", "Circadian", "Adrenal Axis"],
  },
  {
    title: "Thyroid Panel Reference Ranges — Adult Cohort",
    type: "Dataset",
    category: "Thyroid",
    author: "N. Okafor, PhD",
    date: "2026-05-18",
    tags: ["TSH", "Free T4", "Reference Ranges", "Adult"],
  },
  {
    title: "Endocrine Society Testosterone Therapy Guidelines",
    type: "Guideline",
    category: "Reproductive",
    author: "Endocrine Society",
    date: "2026-03-11",
    tags: ["Testosterone", "TRT"],
  },
  {
    title: "PCOS Biomarker Analysis Report Q2",
    type: "Report",
    category: "Reproductive",
    author: "Dr. Priya Nair",
    date: "2026-04-29",
    tags: ["PCOS", "Androgens", "Insulin Resistance"],
  },
  {
    title: "Insulin Sensitivity Across Metabolic Phenotypes",
    type: "Paper",
    category: "Metabolic",
    author: "Dr. Marcus Lin",
    date: "2026-02-14",
    tags: ["Insulin", "HOMA-IR", "Metabolic Syndrome"],
  },
  {
    title: "Longitudinal Estradiol Levels — Perimenopause Cohort",
    type: "Dataset",
    category: "Reproductive",
    author: "K. Whitfield, MSc",
    date: "2026-01-27",
    tags: ["Estradiol", "Perimenopause", "Longitudinal"],
  },
  {
    title: "AACE Clinical Practice Guidelines: Hypothyroidism",
    type: "Guideline",
    category: "Thyroid",
    author: "AACE",
    date: "2025-12-09",
    tags: ["Hypothyroidism", "Levothyroxine"],
  },
  {
    title: "Growth Hormone Deficiency Diagnostic Criteria",
    type: "Paper",
    category: "Pituitary",
    author: "Dr. Sofia Reyes",
    date: "2025-11-22",
    tags: ["GH", "IGF-1", "Diagnosis"],
  },
  {
    title: "Adrenal Fatigue: Evidence Gaps and Misconceptions",
    type: "Report",
    category: "Adrenal",
    author: "Dr. James Okoye",
    date: "2025-10-30",
    tags: ["Adrenal", "Cortisol", "Evidence Review"],
  },
  {
    title: "Vitamin D and Parathyroid Hormone Correlation Dataset",
    type: "Dataset",
    category: "Metabolic",
    author: "R. Bergström, PhD",
    date: "2025-10-05",
    tags: ["Vitamin D", "PTH", "Bone Metabolism"],
  },
  {
    title: "Pediatric Precocious Puberty: Management Guidelines",
    type: "Guideline",
    category: "Reproductive",
    author: "Pediatric Endocrine Society",
    date: "2025-09-17",
    tags: ["Puberty", "Pediatric", "LHRH"],
  },
  {
    title: "Melatonin and Thyroid Function Interaction Study",
    type: "Paper",
    category: "Thyroid",
    author: "Dr. Anya Petrov",
    date: "2025-08-21",
    tags: ["Melatonin", "TSH", "Sleep"],
  },
];

const MAX_VISIBLE_TAGS = 2;

export const metadata: Metadata = {
  title: "Resource Library",
}

export default function ResourcesPage() {
  return (
    <div className="flex flex-1 flex-col">
      <AppHeader
        title="Resource Library"
        description="Search and reference datasets, papers, and guidelines."
      />
      <div className="flex flex-1 flex-col gap-6 p-4 sm:p-6">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div className="relative flex-1 sm:max-w-sm">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search resources..."
              className="pl-9"
              aria-label="Search resources"
            />
          </div>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Select defaultValue="all-types">
              <SelectTrigger className="w-full sm:w-44">
                <SelectValue placeholder="Resource Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all-types">All Types</SelectItem>
                <SelectItem value="paper">Paper</SelectItem>
                <SelectItem value="dataset">Dataset</SelectItem>
                <SelectItem value="guideline">Guideline</SelectItem>
                <SelectItem value="report">Report</SelectItem>
              </SelectContent>
            </Select>
            <Select defaultValue="all-categories">
              <SelectTrigger className="w-full sm:w-44">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all-categories">All Categories</SelectItem>
                <SelectItem value="thyroid">Thyroid</SelectItem>
                <SelectItem value="reproductive">Reproductive</SelectItem>
                <SelectItem value="metabolic">Metabolic</SelectItem>
                <SelectItem value="adrenal">Adrenal</SelectItem>
                <SelectItem value="pituitary">Pituitary</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="rounded-xl border border-border bg-card">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Author</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Tags</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {resources.map((resource) => {
                const visibleTags = resource.tags.slice(0, MAX_VISIBLE_TAGS);
                const remaining = resource.tags.length - visibleTags.length;

                return (
                  <TableRow key={resource.title}>
                    <TableCell className="max-w-xs font-medium text-foreground">
                      {resource.title}
                    </TableCell>
                    <TableCell>
                      <Badge variant={RESOURCE_TYPE_VARIANT[resource.type]}>
                        {resource.type}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {resource.category}
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {resource.author}
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {new Date(resource.date).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-wrap items-center gap-1.5">
                        {visibleTags.map((tag) => (
                          <Badge
                            key={tag}
                            variant="outline"
                            className="font-normal text-muted-foreground"
                          >
                            {tag}
                          </Badge>
                        ))}
                        {remaining > 0 && (
                          <span className="text-xs text-muted-foreground">
                            +{remaining}
                          </span>
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Button
                          variant="ghost"
                          size="icon"
                          aria-label={`View ${resource.title}`}
                        >
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          aria-label={`Download ${resource.title}`}
                        >
                          <Download className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
