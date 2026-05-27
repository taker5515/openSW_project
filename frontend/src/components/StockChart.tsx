import { useState, useEffect, useMemo } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import type { WatchItem, ChartPoint } from "../types";
import { genChartData } from "../utils/mockData";

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ background: "#0a0c14", borderRadius: 8, padding: "10px 14px", border: "1px solid #0e1118" }}>
      <div style={{ fontSize: 11, color: "#4b5563", marginBottom: 3 }}>{label}</div>
      <div style={{ fontSize: 14, fontWeight: 700, color: "#c4cdd8", fontFamily: "monospace" }}>{value}</div>
    </div>
  );
}

// StockChart는 key={ticker}로 마운트 시 초기화됨 (DashboardPage에서 key prop 사용)
export function StockChart({ item }: { item: WatchItem }) {
  const [chartData, setChartData] = useState<ChartPoint[]>(() => genChartData(item.price));
  // 거래량 mock값은 렌더마다 바뀌지 않도록 초기화 시 1회만 계산
  const [volume] = useState(() => `${(Math.random() * 50 + 30).toFixed(1)}M`);
  const positive = item.change >= 0;
  const color = positive ? "#34d270" : "#f87171";

  useEffect(() => {
    const id = setInterval(() => {
      setChartData((prev) => {
        const last = prev[prev.length - 1].price;
        const next = +(last + (Math.random() - 0.47) * 0.8).toFixed(2);
        const now = new Date();
        return [
          ...prev.slice(-59),
          { time: `${now.getHours()}:${String(now.getMinutes()).padStart(2, "0")}`, price: next },
        ];
      });
    }, 3000);
    return () => clearInterval(id);
  }, []);

  const metrics = useMemo(() => [
    { label: "시가",  value: `$${(item.price * 0.989).toFixed(2)}` },
    { label: "고가",  value: `$${(item.price * 1.013).toFixed(2)}` },
    { label: "저가",  value: `$${(item.price * 0.984).toFixed(2)}` },
    { label: "거래량", value: volume },
  ], [item.price, volume]);

  return (
    <div>
      <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginBottom: 16 }}>
        <span style={{ fontSize: 28, fontWeight: 700, color: "#e2e8f0", fontFamily: "monospace" }}>
          ${item.price.toFixed(2)}
        </span>
        <span style={{ fontSize: 15, fontWeight: 600, color, fontFamily: "monospace" }}>
          {positive ? "+" : ""}{item.change.toFixed(2)} ({positive ? "+" : ""}{item.changePct.toFixed(2)}%)
        </span>
        <span style={{ fontSize: 12, color: "#4b5563" }}>{item.ticker} · 오늘</span>
      </div>
      <div style={{ background: "#0a0c14", borderRadius: 10, padding: "16px 16px 8px", border: "1px solid #0e1118" }}>
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={color} stopOpacity={0.15} />
                <stop offset="100%" stopColor={color} stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="time" tick={{ fill: "#374151", fontSize: 10 }} tickLine={false} axisLine={false} interval={9} />
            <YAxis tick={{ fill: "#374151", fontSize: 10 }} tickLine={false} axisLine={false} width={52}
              tickFormatter={(v) => `$${v.toFixed(0)}`} domain={["auto", "auto"]} />
            <Tooltip contentStyle={{ background: "#0f1117", border: "1px solid #1e2130", borderRadius: 8, fontSize: 12 }}
             formatter={(v: unknown) => [`$${(v as number).toFixed(2)}`, "가격"]} />
            <Area type="monotone" dataKey="price" stroke={color} strokeWidth={1.5} fill="url(#cg)" dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 10, marginTop: 14 }}>
        {metrics.map((m) => <MetricCard key={m.label} {...m} />)}
      </div>
    </div>
  );
}
