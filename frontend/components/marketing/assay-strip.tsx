const TIMEPOINTS = ["06:00", "09:00", "12:00", "18:00", "24:00"]

export function AssayStrip() {
  return (
    <figure className="w-full">
      <div className="flex items-baseline justify-between gap-4 border-b border-border pb-2">
        <figcaption className="font-mono text-[11px] uppercase tracking-[0.08em] text-muted-foreground">
          Fig. 1 — Serum cortisol, 24h profile
        </figcaption>
        <span className="font-mono text-[11px] text-muted-foreground">
          n = 1 · μg/dL
        </span>
      </div>

      <svg
        viewBox="0 0 640 220"
        role="img"
        aria-label="Chart of serum cortisol across a 24 hour cycle, staying within the normal reference band except for one elevated point flagged at 12:00"
        className="mt-4 h-auto w-full"
      >
        <rect x="0" y="92" width="640" height="64" fill="var(--secondary)" opacity="0.12" />
        <line x1="0" y1="92" x2="640" y2="92" stroke="var(--border)" strokeWidth="1" />
        <line x1="0" y1="156" x2="640" y2="156" stroke="var(--border)" strokeWidth="1" />

        <text
          x="6"
          y="88"
          fontFamily="var(--font-mono)"
          fontSize="10"
          fill="var(--muted-foreground)"
        >
          upper limit
        </text>
        <text
          x="6"
          y="170"
          fontFamily="var(--font-mono)"
          fontSize="10"
          fill="var(--muted-foreground)"
        >
          lower limit
        </text>

        <path
          d="M 0 108 C 40 40, 90 28, 130 44 S 220 96, 280 104 C 320 110, 340 40, 372 34 S 430 118, 480 132 C 540 148, 590 150, 640 150"
          fill="none"
          stroke="var(--primary)"
          strokeWidth="2.5"
          strokeLinecap="round"
          className="assay-strip-path"
        />

        <circle cx="372" cy="34" r="4.5" fill="var(--warning)" stroke="var(--background)" strokeWidth="2" />
        <text
          x="372"
          y="20"
          textAnchor="middle"
          fontFamily="var(--font-mono)"
          fontSize="10"
          fontWeight="600"
          fill="var(--warning)"
        >
          21.4 — elevated
        </text>

        {TIMEPOINTS.map((label, i) => (
          <text
            key={label}
            x={(i / (TIMEPOINTS.length - 1)) * 640}
            y="212"
            textAnchor={i === 0 ? "start" : i === TIMEPOINTS.length - 1 ? "end" : "middle"}
            fontFamily="var(--font-mono)"
            fontSize="10"
            fill="var(--muted-foreground)"
          >
            {label}
          </text>
        ))}
      </svg>
    </figure>
  )
}
