import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import { useEffect } from "react";
import type { MapPoint } from "../api";

const POLAND_CENTER: [number, number] = [52.0, 19.2];
const POLAND_ZOOM = 6;

const LEGEND = [
  { label: "Bardzo dobry (≤10)", color: "#22c55e" },
  { label: "Dobry (≤20)", color: "#84cc16" },
  { label: "Umiarkowany (≤25)", color: "#eab308" },
  { label: "Dostateczny (≤50)", color: "#f97316" },
  { label: "Zly (≤75)", color: "#ef4444" },
  { label: "Bardzo zly (>75)", color: "#7f1d1d" },
];

function FitPoland() {
  const map = useMap();
  useEffect(() => {
    map.setView(POLAND_CENTER, POLAND_ZOOM);
  }, [map]);
  return null;
}

interface Props {
  points: MapPoint[];
  onSelect: (sensorId: number) => void;
}

export function AirMap({ points, onSelect }: Props) {
  return (
    <>
      <MapContainer center={POLAND_CENTER} zoom={POLAND_ZOOM} scrollWheelZoom>
        <FitPoland />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        {points.map((p) => (
          <CircleMarker
            key={p.sensor_id}
            center={[p.latitude, p.longitude]}
            radius={7}
            pathOptions={{
              color: p.aqi_color,
              fillColor: p.aqi_color,
              fillOpacity: 0.85,
              weight: 1,
            }}
            eventHandlers={{
              click: () => onSelect(p.sensor_id),
            }}
          >
            <Popup>
              <strong>Czujnik #{p.sensor_id}</strong>
              <br />
              {p.sensor_type}
              <br />
              PM2.5: {p.pm25?.toFixed(1) ?? "—"} ug/m3
              <br />
              PM10: {p.pm10?.toFixed(1) ?? "—"} ug/m3
              <br />
              <span style={{ color: p.aqi_color }}>{p.aqi_level}</span>
              <br />
              <small>{new Date(p.measured_at).toLocaleString("pl-PL")}</small>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
      <div className="legend">
        <strong>PM2.5 (ug/m3)</strong>
        {LEGEND.map((item) => (
          <div key={item.label} className="legend-item">
            <span className="legend-dot" style={{ background: item.color }} />
            {item.label}
          </div>
        ))}
      </div>
    </>
  );
}
