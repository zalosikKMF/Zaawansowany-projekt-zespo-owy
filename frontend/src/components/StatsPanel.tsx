import type { NationalStats } from "../api";
import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface Props {
  stats: NationalStats | null;
  loading: boolean;
}

export function StatsPanel({ stats, loading }: Props) {
  if (loading) return <p style={{ color: "#94a3b8" }}>Ladowanie statystyk...</p>;
  if (!stats) return null;

  const chartData = Object.entries(stats.by_quality).map(([name, value]) => ({
    name: name.length > 12 ? name.slice(0, 11) + "…" : name,
    fullName: name,
    count: value,
  }));

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="label">Aktywne czujniki PM</div>
        <div className="value">{stats.active_pm_sensors}</div>
        <div className="unit">z {stats.total_sensors} w bazie</div>
      </div>
      <div className="stat-card">
        <div className="label">Srednie PM2.5</div>
        <div className="value">{stats.avg_pm25?.toFixed(1) ?? "—"}</div>
        <div className="unit">ug/m3 (Polska)</div>
      </div>
      <div className="stat-card">
        <div className="label">Mediana PM2.5</div>
        <div className="value">{stats.median_pm25?.toFixed(1) ?? "—"}</div>
        <div className="unit">ug/m3</div>
      </div>
      <div className="stat-card">
        <div className="label">Zakres PM2.5</div>
        <div className="value" style={{ fontSize: "1rem" }}>
          {stats.min_pm25?.toFixed(0) ?? "—"} – {stats.max_pm25?.toFixed(0) ?? "—"}
        </div>
        <div className="unit">min – max ug/m3</div>
      </div>

      {chartData.length > 0 && (
        <div className="quality-list">
          <h3>Rozklad jakosci powietrza</h3>
          <div style={{ height: 200 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 4, right: 4, left: -20, bottom: 40 }}>
                <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 10 }} angle={-35} textAnchor="end" height={50} />
                <YAxis tick={{ fill: "#94a3b8", fontSize: 10 }} />
                <Tooltip
                  contentStyle={{ background: "#1e293b", border: "1px solid #334155" }}
                  labelFormatter={(_, payload) =>
                    payload?.[0]?.payload?.fullName ?? ""
                  }
                />
                <Bar dataKey="count" fill="#38bdf8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}
