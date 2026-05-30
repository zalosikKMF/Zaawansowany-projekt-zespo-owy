const API_BASE = import.meta.env.VITE_API_URL || "";

export interface MapPoint {
  sensor_id: number;
  location_id: number;
  latitude: number;
  longitude: number;
  sensor_type: string;
  indoor: boolean;
  measured_at: string;
  pm10: number | null;
  pm25: number | null;
  aqi_level: string;
  aqi_color: string;
}

export interface NationalStats {
  total_sensors: number;
  active_pm_sensors: number;
  avg_pm25: number | null;
  avg_pm10: number | null;
  median_pm25: number | null;
  max_pm25: number | null;
  min_pm25: number | null;
  last_sync: string | null;
  measured_at_range: string | null;
  by_quality: Record<string, number>;
}

export interface SensorDetail {
  sensor_id: number;
  sensor_type: string;
  manufacturer: string | null;
  latitude: number;
  longitude: number;
  indoor: boolean;
  latest: MapPoint | null;
  history: Array<{
    measured_at: string;
    pm10: number | null;
    pm25: number | null;
    temperature: number | null;
    humidity: number | null;
  }>;
}

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json();
}

export const api = {
  map: () => fetchJson<MapPoint[]>("/api/map"),
  stats: () => fetchJson<NationalStats>("/api/stats"),
  health: () => fetchJson<{ status: string; database: string; last_sync: string | null }>("/api/health"),
  sensor: (id: number) => fetchJson<SensorDetail>(`/api/sensors/${id}`),
  sync: () =>
    fetch(`${API_BASE}/api/sync`, { method: "POST" }).then((r) => {
      if (!r.ok) throw new Error("Sync failed");
      return r.json();
    }),
};
