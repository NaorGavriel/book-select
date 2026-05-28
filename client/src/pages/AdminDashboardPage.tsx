import type { ReactNode } from "react";
import { useMetrics } from "../features/admin/useMetrics";

type Accent =
  | "blue"
  | "green"
  | "red"
  | "purple"
  | "amber"
  | "cyan";

const accentStyles: Record<
  Accent,
  {
    border: string;
    glow: string;
    value: string;
  }
> = {
  blue: {
    border: "border-blue-500/40",
    glow: "from-blue-500/10",
    value: "text-blue-300",
  },
  green: {
    border: "border-emerald-500/40",
    glow: "from-emerald-500/10",
    value: "text-emerald-300",
  },
  red: {
    border: "border-red-500/40",
    glow: "from-red-500/10",
    value: "text-red-300",
  },
  purple: {
    border: "border-purple-500/40",
    glow: "from-purple-500/10",
    value: "text-purple-300",
  },
  amber: {
    border: "border-amber-500/40",
    glow: "from-amber-500/10",
    value: "text-amber-300",
  },
  cyan: {
    border: "border-cyan-500/40",
    glow: "from-cyan-500/10",
    value: "text-cyan-300",
  },
};

function StatCard({
  label,
  value,
  accent = "blue",
}: {
  label: string;
  value: string | number;
  accent?: Accent;
}) {
  const style = accentStyles[accent];

  return (
    <div
      className={`
        relative overflow-hidden rounded-2xl border bg-neutral-900/80
        p-5 backdrop-blur-sm transition-all duration-200
        hover:-translate-y-1 hover:shadow-xl
        ${style.border}
      `}
    >
      <div
        className={`
          absolute inset-0 bg-gradient-to-br to-transparent pointer-events-none
          ${style.glow}
        `}
      />

      <div className="relative flex flex-col gap-2">
        <span className="text-[11px] font-semibold uppercase tracking-[0.2em] text-neutral-500">
          {label}
        </span>

        <span className={`text-3xl font-bold ${style.value}`}>
          {value}
        </span>
      </div>
    </div>
  );
}

function Section({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <section className="space-y-5">
      <div className="flex items-end justify-between border-b border-neutral-800 pb-3">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-stone-50">
            {title}
          </h2>

          {subtitle && (
            <p className="mt-1 text-sm text-neutral-400">{subtitle}</p>
          )}
        </div>
      </div>

      {children}
    </section>
  );
}

function RankedPanel({ title, items }: { title: string; items: { label: string; count: number }[] }) {
  /** Titled card wrapping a RankedList. */
  return (
    <div className="rounded-2xl border border-neutral-800 bg-neutral-900/80 p-5">
      <h3 className="mb-4 text-lg font-semibold text-stone-100">{title}</h3>
      <RankedList items={items} />
    </div>
  );
}

function RankedList({ items }: { items: { label: string; count: number }[] }) {
  return (
    <ol className="space-y-2">
      {items.map((item, i) => (
        <li
          key={item.label}
          className="flex items-center justify-between rounded-lg bg-neutral-900/70 px-3 py-2"
        >
          <div className="flex items-center gap-3 overflow-hidden">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-neutral-800 text-xs font-semibold text-neutral-400">
              {i + 1}
            </span>

            <span className="truncate text-sm text-stone-200">
              {item.label}
            </span>
          </div>

          <span className="text-sm font-medium text-neutral-400">
            {item.count}
          </span>
        </li>
      ))}
    </ol>
  );
}

/**
 * AdminDashboardPage
 * ------------------
 * Displays a live system metrics snapshot.
 */
export default function AdminDashboardPage() {
  const { metrics, error } = useMetrics();

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-10 text-red-400">
        Failed to load metrics.
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-10 text-neutral-400">
        Loading…
      </div>
    );
  }

  const { cache, jobs, recommendations: rec, performance, users } = metrics;

  return (
    <div className="min-h-screen bg-neutral-950">
      <div className="max-w-7xl mx-auto px-6 py-10 space-y-12">
        {/* Header */}
        <div className="space-y-3">
          <div className="inline-flex items-center rounded-full border border-neutral-800 bg-neutral-900 px-3 py-1 text-xs font-medium uppercase tracking-wider text-neutral-400">
            Admin Panel
          </div>

          <div>
            <h1 className="text-4xl font-bold tracking-tight text-stone-50">
              Admin Dashboard
            </h1>

            <p className="mt-2 max-w-2xl text-neutral-400">
              Monitor platform activity, recommendation quality, cache
              performance and overall system health in real time.
            </p>
          </div>
        </div>

        <Section
          title="Users"
          subtitle="User growth and activity overview"
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            <StatCard label="Total Users" value={users.total} accent="blue" />

            <StatCard
              label="Active (30d)"
              value={users.active}
              accent="green"
            />

            <StatCard
              label="New Today"
              value={users.new_today}
              accent="purple"
            />

            <StatCard
              label="Reading History Entries"
              value={users.reading_history_count}
              accent="cyan"
            />
          </div>
        </Section>

        <Section
          title="Jobs"
          subtitle="Background processing pipeline metrics"
        >
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <StatCard
              label="Created Today"
              value={jobs.total_today}
              accent="blue"
            />

            <StatCard
              label="Completed"
              value={jobs.completed}
              accent="green"
            />

            <StatCard
              label="Failed"
              value={jobs.failed}
              accent="red"
            />
          </div>
        </Section>

        <Section
          title="Cache"
          subtitle="Recommendation cache efficiency and lookup behavior"
        >
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <StatCard label="Hits" value={cache.hits} accent="green" />

            <StatCard label="Misses" value={cache.misses} accent="red" />

            <StatCard
              label="Hit Rate"
              value={`${(cache.hit_rate * 100).toFixed(1)}%`}
              accent="amber"
            />
          </div>
        </Section>

        <Section
          title="Performance"
          subtitle="Average latency and processing times"
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <StatCard
              label="Avg Cache Lookup"
              value={`${performance.avg_cache_lookup_latency_ms} ms`}
              accent="cyan"
            />

            <StatCard
              label="Avg Job Duration"
              value={`${performance.avg_job_processing_duration_s} s`}
              accent="purple"
            />
          </div>
        </Section>

        <Section
          title="Recommendations"
          subtitle="Recommendation volume and confidence distribution"
        >
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total" value={rec.total} accent="blue" />

            <StatCard label="Today" value={rec.today} accent="green" />

            <StatCard
              label="This Week"
              value={rec.this_week}
              accent="purple"
            />

            <StatCard
              label="Avg Confidence"
              value={rec.avg_confidence.toFixed(2)}
              accent="amber"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <StatCard
              label="Strong Match"
              value={`${rec.strong_match_pct}%`}
              accent="green"
            />

            <StatCard
              label="Consider"
              value={`${rec.consider_pct}%`}
              accent="amber"
            />

            <StatCard
              label="Avoid"
              value={`${rec.avoid_pct}%`}
              accent="red"
            />
          </div>
        </Section>

        <Section
          title="Top Lists"
          subtitle="Most recommended books, authors and genres"
        >
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            <RankedPanel
              title="Top Books"
              items={rec.top_books.map((b) => ({ label: b.title, count: b.count }))}
            />
            <RankedPanel
              title="Top Authors"
              items={rec.top_authors.map((a) => ({ label: a.author, count: a.count }))}
            />
            <RankedPanel
              title="Top Genres"
              items={rec.top_genres.map((g) => ({ label: g.genre, count: g.count }))}
            />
          </div>
        </Section>
      </div>
    </div>
  );
}