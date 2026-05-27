import type { ReactNode } from "react";
import { useMetrics } from "../features/admin/useMetrics";

function StatCard({ label, value }: { label: string; value: string | number }) {
  /** Single metric label + value block. */
  return (
    <div className="bg-neutral-800 rounded-xl p-4 flex flex-col gap-1">
      <span className="text-xs uppercase tracking-wide text-neutral-400">{label}</span>
      <span className="text-2xl font-semibold text-stone-50">{value}</span>
    </div>
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  /** Labelled group of stat cards. */
  return (
    <div>
      <h2 className="text-sm font-semibold uppercase tracking-widest text-neutral-400 mb-3">
        {title}
      </h2>
      {children}
    </div>
  );
}

function RankedList({ items }: { items: { label: string; count: number }[] }) {
  /** Ordered list of label + count rows. */
  return (
    <ol className="space-y-1">
      {items.map((item, i) => (
        <li key={item.label} className="flex justify-between text-sm text-stone-200">
          <span className="text-neutral-400 mr-2">{i + 1}.</span>
          <span className="flex-1 truncate">{item.label}</span>
          <span className="text-neutral-400 ml-2">{item.count}</span>
        </li>
      ))}
    </ol>
  );
}

/**
 * AdminDashboardPage
 * ------------------
 * Displays a live system metrics snapshot. Data fetching and polling
 * are handled by the useMetrics hook.
 */
export default function AdminDashboardPage() {
  const { metrics, error } = useMetrics();

  if (error) {
    return (
      <div className="max-w-6xl mx-auto px-6 py-10 text-red-400">
        Failed to load metrics.
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="max-w-6xl mx-auto px-6 py-10 text-neutral-400">
        Loading…
      </div>
    );
  }

  const { cache, jobs, recommendations: rec, performance, users } = metrics;

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 space-y-10">
      <h1 className="text-2xl font-semibold text-stone-50">Admin Dashboard</h1>

      <Section title="Users">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <StatCard label="Total" value={users.total} />
          <StatCard label="Active (30d)" value={users.active} />
          <StatCard label="New Today" value={users.new_today} />
          <StatCard label="Reading History Entries" value={users.reading_history_count} />
        </div>
      </Section>

      <Section title="Jobs">
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <StatCard label="Created Today" value={jobs.total_today} />
          <StatCard label="Completed" value={jobs.completed} />
          <StatCard label="Failed" value={jobs.failed} />
        </div>
      </Section>

      <Section title="Cache">
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <StatCard label="Hits" value={cache.hits} />
          <StatCard label="Misses" value={cache.misses} />
          <StatCard label="Hit Rate" value={`${(cache.hit_rate * 100).toFixed(1)}%`} />
        </div>
      </Section>

      <Section title="Performance">
        <div className="grid grid-cols-2 gap-4">
          <StatCard
            label="Avg Cache Lookup"
            value={`${performance.avg_cache_lookup_latency_ms} ms`}
          />
          <StatCard
            label="Avg Job Duration"
            value={`${performance.avg_job_processing_duration_s} s`}
          />
        </div>
      </Section>

      <Section title="Recommendations">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
          <StatCard label="Total" value={rec.total} />
          <StatCard label="Today" value={rec.today} />
          <StatCard label="This Week" value={rec.this_week} />
          <StatCard label="Avg Confidence" value={rec.avg_confidence.toFixed(2)} />
        </div>
        <div className="grid grid-cols-3 gap-4">
          <StatCard label="Strong Match" value={`${rec.strong_match_pct}%`} />
          <StatCard label="Consider" value={`${rec.consider_pct}%`} />
          <StatCard label="Avoid" value={`${rec.avoid_pct}%`} />
        </div>
      </Section>

      <Section title="Top Lists">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="bg-neutral-800 rounded-xl p-4">
            <h3 className="text-xs uppercase tracking-wide text-neutral-400 mb-3">Books</h3>
            <RankedList items={rec.top_books.map((b) => ({ label: b.title, count: b.count }))} />
          </div>
          <div className="bg-neutral-800 rounded-xl p-4">
            <h3 className="text-xs uppercase tracking-wide text-neutral-400 mb-3">Authors</h3>
            <RankedList items={rec.top_authors.map((a) => ({ label: a.author, count: a.count }))} />
          </div>
          <div className="bg-neutral-800 rounded-xl p-4">
            <h3 className="text-xs uppercase tracking-wide text-neutral-400 mb-3">Genres</h3>
            <RankedList items={rec.top_genres.map((g) => ({ label: g.genre, count: g.count }))} />
          </div>
        </div>
      </Section>
    </div>
  );
}
