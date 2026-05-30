import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface Props {
  history: Array<{
    measured_at: string;
    pm25: number | null;
    pm10: number | null;
  }>;
}

export function SensorChart({ history }: Props) {
  const data = [...history]
    .reverse()
    .map((h) => ({
      time: new Date(h.measured_at).toLocaleTimeString("pl-PL", {
        hour: "2-digit",
        minute: "2-digit",
      }),
      pm25: h.pm25,
      pm10: h.pm10,
    }));

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
        <XAxis dataKey="time" tick={{ fill: "#94a3b8", fontSize: 9 }} />
        <YAxis tick={{ fill: "#94a3b8", fontSize: 9 }} />
        <Tooltip contentStyle={{ background: "#1e293b", border: "1px solid #334155" }} />
        <Line type="monotone" dataKey="pm25" stroke="#38bdf8" dot={false} name="PM2.5" />
        <Line type="monotone" dataKey="pm10" stroke="#a78bfa" dot={false} name="PM10" />
      </LineChart>
    </ResponsiveContainer>
  );
}
