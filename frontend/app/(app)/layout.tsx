import { Suspense } from "react"

import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/layout/app-sidebar"
import { AuthGate } from "@/components/layout/auth-gate"
import { PageSkeleton } from "@/components/layout/page-skeleton"
import { AuthProvider } from "@/contexts/auth-context"

export default function AppShellLayout({ children }: LayoutProps<"/">) {
  return (
    <AuthProvider>
      <SidebarProvider>
        <AppSidebar />
        <SidebarInset>
          <Suspense fallback={<PageSkeleton />}>
            <AuthGate>{children}</AuthGate>
          </Suspense>
        </SidebarInset>
      </SidebarProvider>
    </AuthProvider>
  )
}
