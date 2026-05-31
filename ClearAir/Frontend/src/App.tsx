import { useCallback, useEffect, useState } from "react";
import { api, MapPoint, NationalStats, SensorDetail } from "./api";
import { AirMap } from "./components/AirMap";
import { StatsPanel } from "./components/StatsPanel";
import { SensorChart } from "./components/SensorChart";

export default function App() {
  const [points, setPoints] = useState<MapPoint[]>([]);
  const [stats, setStats] = useState<NationalStats | null>(null);
  const [selected, setSelected] = useState<SensorDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastSync, setLastSync] = useState<string | null>(null);

  const load = useCallback(async () => {
    setError(null);
    try {
      const [mapData, statsData, health] = await Promise.all([
        api.map(),
        api.stats(),
        api.health(),
      ]);
      setPoints(mapData);
      setStats(statsData);
      setLastSync(health.last_sync);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Blad polaczenia z API");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
    const t = setInterval(load, 5 * 60 * 1000);
    return () => clearInterval(t);
  }, [load]);

  const handleSync = async () => {
    setSyncing(true);
    try {
      await api.sync();
      await load();
      if (selected) {
        const detail = await api.sensor(selected.sensor_id);
        setSelected(detail);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Synchronizacja nieudana");
    } finally {
      setSyncing(false);
    }
  };

  const handleSelect = async (sensorId: number) => {
    try {
      const detail = await api.sensor(sensorId);
      setSelected(detail);
    } catch {
      setSelected(null);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>ClearAir</h1>
          <p>System monitorowania jakosci powietrza w Polsce | Sensor.Community</p>
        </div>
        <div className="header-actions">
          {lastSync && (
            <span className="badge">
              Ostatnia sync: {new Date(lastSync).toLocaleString("pl-PL")}
            </span>
          )}
          <button className="btn" onClick={handleSync} disabled={syncing}>
            {syncing ? "Synchronizacja..." : "Synchronizuj dane"}
          </button>
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      <div className="main">
        <aside className="sidebar">
          <StatsPanel stats={stats} loading={loading} />
          {selected && (
            <div className="detail-panel">
              <h4>Czujnik #{selected.sensor_id}</h4>
              <p>Typ: {selected.sensor_type}</p>
              {selected.manufacturer && <p>Producent: {selected.manufacturer}</p>}
              {selected.latest && (
                <>
                  <p>PM2.5: {selected.latest.pm25?.toFixed(1)} ug/m3</p>
                  <p>PM10: {selected.latest.pm10?.toFixed(1) ?? "—"} ug/m3</p>
                  <p>Jakosc: {selected.latest.aqi_level}</p>
                </>
              )}
              {selected.history.length > 1 && (
                <div className="chart-wrap">
                  <SensorChart history={selected.history} />
                </div>
              )}
            </div>
          )}
        </aside>
        <section className="map-wrap">
          <AirMap points={points} onSelect={handleSelect} />
        </section>
      </div>

      <footer className="footer">
        Dane z projektu open-source{" "}
        <a href="https://sensor.community" target="_blank" rel="noreferrer" style={{ color: "#38bdf8" }}>
          Sensor.Community
        </a>
        . ClearAir – projekt edukacyjny.
      </footer>
    </div>
  );
}
