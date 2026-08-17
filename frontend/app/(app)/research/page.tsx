"use client";

import * as React from "react";
import {
  FlaskConical,
  CheckCircle2,
  Clock,
  Users,
  Search,
  Upload,
  MoreHorizontal,
} from "lucide-react";

import { AppHeader } from "@/components/layout/app-header";
import { StatCard } from "@/components/dashboard/stat-card";
import { StatusBadge, type ResearchStatus } from "@/components/dashboard/status-badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";

interface Study {
  id: string;
  name: string;
  author: string;
  category: string;
  updated: string;
  status: ResearchStatus;
}

const studies: Study[] = [
  {
    id: "1",
    name: "Cortisol Circadian Rhythm Cohort",
    author: "Dr. Elena Vasquez",
    category: "Cortisol",
    updated: "2026-08-12",
    status: "validated",
  },
  {
    id: "2",
    name: "Testosterone Replacement Outcomes",
    author: "Dr. Marcus Chen",
    category: "Testosterone",
    updated: "2026-08-11",
    status: "processing",
  },
  {
    id: "3",
    name: "Estradiol Variability in Perimenopause",
    author: "Dr. Priya Nair",
    category: "Estradiol",
    updated: "2026-08-10",
    status: "needs-review",
  },
  {
    id: "4",
    name: "Thyroid Panel Reference Ranges",
    author: "Dr. Samuel Okafor",
    category: "Thyroid (TSH/T3/T4)",
    updated: "2026-08-09",
    status: "validated",
  },
  {
    id: "5",
    name: "PCOS Androgen Profile Study",
    author: "Dr. Laura Kim",
    category: "PCOS / Androgens",
    updated: "2026-08-08",
    status: "draft",
  },
  {
    id: "6",
    name: "Insulin Resistance & Cortisol Correlation",
    author: "Dr. Elena Vasquez",
    category: "Cortisol",
    updated: "2026-08-07",
    status: "failed",
  },
  {
    id: "7",
    name: "Progesterone Luteal Phase Tracking",
    author: "Dr. Ana Ferreira",
    category: "Progesterone",
    updated: "2026-08-06",
    status: "processing",
  },
  {
    id: "8",
    name: "Male Hypogonadism Biomarker Set",
    author: "Dr. Marcus Chen",
    category: "Testosterone",
    updated: "2026-08-05",
    status: "needs-review",
  },
  {
    id: "9",
    name: "Postpartum Thyroiditis Longitudinal Data",
    author: "Dr. Samuel Okafor",
    category: "Thyroid (TSH/T3/T4)",
    updated: "2026-08-03",
    status: "validated",
  },
  {
    id: "10",
    name: "Adrenal Fatigue Hypothesis Dataset",
    author: "Dr. Laura Kim",
    category: "Cortisol",
    updated: "2026-08-01",
    status: "draft",
  },
];

const statusFilters: { label: string; value: ResearchStatus | "all" }[] = [
  { label: "All", value: "all" },
  { label: "Validated", value: "validated" },
  { label: "Processing", value: "processing" },
  { label: "Needs Review", value: "needs-review" },
  { label: "Failed", value: "failed" },
  { label: "Draft", value: "draft" },
];

export default function ResearchHubPage() {
  const [activeFilter, setActiveFilter] = React.useState<ResearchStatus | "all">("all");
  const [query, setQuery] = React.useState("");

  const filteredStudies = studies.filter((study) => {
    const matchesStatus = activeFilter === "all" || study.status === activeFilter;
    const matchesQuery =
      query.trim() === "" ||
      study.name.toLowerCase().includes(query.toLowerCase()) ||
      study.author.toLowerCase().includes(query.toLowerCase()) ||
      study.category.toLowerCase().includes(query.toLowerCase());
    return matchesStatus && matchesQuery;
  });

  return (
    <div className="flex flex-1 flex-col">
      <AppHeader
        title="Research Hub"
        description="Validate, analyze, and review hormone research datasets."
      />
      <div className="flex flex-1 flex-col gap-6 p-4 sm:p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="grid flex-1 grid-cols-2 gap-4 lg:grid-cols-4">
            <StatCard label="Total Studies" value="128" icon={FlaskConical} />
            <StatCard label="Datasets Validated" value="94" icon={CheckCircle2} />
            <StatCard label="Pending Review" value="17" icon={Clock} />
            <StatCard label="Active Researchers" value="23" icon={Users} />
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <Tabs
              value={activeFilter}
              onValueChange={(value) => setActiveFilter(value as ResearchStatus | "all")}
            >
              <TabsList>
                {statusFilters.map((filter) => (
                  <TabsTrigger key={filter.value} value={filter.value}>
                    {filter.label}
                  </TabsTrigger>
                ))}
              </TabsList>
            </Tabs>

            <div className="flex items-center gap-2">
              <div className="relative w-full sm:w-64">
                <Search className="pointer-events-none absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  placeholder="Search studies, authors, hormones..."
                  className="pl-8"
                />
              </div>
              <Button className="shrink-0 gap-2">
                <Upload className="h-4 w-4" />
                Upload Dataset
              </Button>
            </div>
          </div>

          <div className="overflow-hidden rounded-lg border border-border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Study / Dataset</TableHead>
                  <TableHead>Author / Team</TableHead>
                  <TableHead>Hormone / Category</TableHead>
                  <TableHead>Last Updated</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="w-10 text-right">
                    <span className="sr-only">Actions</span>
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredStudies.length === 0 ? (
                  <TableRow>
                    <TableCell
                      colSpan={6}
                      className="h-24 text-center text-muted-foreground"
                    >
                      No studies match your filters.
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredStudies.map((study) => (
                    <TableRow key={study.id}>
                      <TableCell className="font-medium text-foreground">
                        {study.name}
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {study.author}
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {study.category}
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {study.updated}
                      </TableCell>
                      <TableCell>
                        <StatusBadge status={study.status} />
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger
                            render={
                              <Button
                                variant="ghost"
                                size="icon-sm"
                                aria-label="Open actions"
                              >
                                <MoreHorizontal />
                              </Button>
                            }
                          />
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>View details</DropdownMenuItem>
                            <DropdownMenuItem>Download report</DropdownMenuItem>
                            <DropdownMenuItem>Reassign reviewer</DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>
    </div>
  );
}
