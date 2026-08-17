import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Research Hub",
}

export default function ResearchLayout({ children }: LayoutProps<"/research">) {
  return children
}
