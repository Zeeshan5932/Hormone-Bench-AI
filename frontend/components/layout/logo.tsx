import Image from "next/image"

import { cn } from "@/lib/utils"

const HEADER_LOGO_RATIO = 1421 / 763

export function Logo({
  className,
  height = 36,
}: {
  className?: string
  height?: number
}) {
  const width = Math.round(height * HEADER_LOGO_RATIO)

  return (
    <Image
      src="/assets/logo-header.png"
      alt="HormoneBench AI"
      width={width}
      height={height}
      style={{ width, height }}
      className={cn("shrink-0 object-contain", className)}
      priority
    />
  )
}

export function LogoMark({
  className,
  size = 28,
}: {
  className?: string
  size?: number
}) {
  return (
    <Image
      src="/assets/logo-icon.png"
      alt="HormoneBench AI"
      width={size}
      height={size}
      className={cn("shrink-0 object-contain", className)}
      priority
    />
  )
}
