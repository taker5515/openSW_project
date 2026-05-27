import { useState } from "react";
import { X, Plus } from "lucide-react";
import { LineChart, Line, ResponsiveContainer } from "recharts";
import type { WatchItem } from "../types";

function Sparkline({ data, positive }: { data: number[]; positive: boolean }) {
  const points = data.map((v, t) => ({ t, v }));
  return (
    <ResponsiveContainer width={72} height={32}>
      <LineChart data={points}>
        <Line type="monotone" dataKey="v" dot={false} strokeWidth={1.5}
          stroke={positive ? "#34d270" : "#f87171"} />
      </LineChart>
    </ResponsiveContainer>
  );
}

function WatchRow({ item, selected, onSelect, onRemove }: {
  item: WatchItem; selected: boolean;
  onSelect: () => void; onRemove: () => void;
}) {
  const positive = item.change >= 0;
  return (
    <div onClick={onSelect}
      style={{ display: "flex", alignItems: "center", gap: 8, padding: "10px 14px",
        borderBottom: "1px solid #080a10", cursor: "pointer",
        background: selected ? "#0a1020" : "transparent" }}>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0", fontFamily: "monospace" }}>{item.ticker}</div>
        <div style={{ fontSize: 10, color: "#4b5563" }}>{item.name}</div>
      </div>
      <Sparkline data={item.history} positive={positive} />
      <div style={{ textAlign: "right" }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0", fontFamily: "monospace" }}>
          ${item.price.toFixed(2)}
        </div>
        <div style={{ fontSize: 11, fontWeight: 600, color: positive ? "#34d270" : "#f87171" }}>
          {positive ? "+" : ""}{item.change.toFixed(2)} ({positive ? "+" : ""}{item.changePct.toFixed(2)}%)
        </div>
      </div>
      <button onClick={(e) => { e.stopPropagation(); onRemove(); }}
        style={{ background: "transparent", border: "none", color: "#374151", cursor: "pointer", padding: 4 }}>
        <X size={13} />
      </button>
    </div>
  );
}

export function Watchlist({ items, selectedTicker, onSelect, onAdd, onRemove }: {
  items: WatchItem[]; selectedTicker: string;
  onSelect: (t: string) => void;
  onAdd: (t: string) => void;
  onRemove: (t: string) => void;
}) {
  const [input, setInput] = useState("");

  const submit = () => {
    const t = input.toUpperCase().trim();
    if (t) { onAdd(t); setInput(""); }
  };

  return (
    <div style={{ background: "#0a0c14", borderRadius: 10, border: "1px solid #0e1118", overflow: "hidden" }}>
      <div style={{ padding: "12px 14px", borderBottom: "1px solid #0e1118",
        display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 12, fontWeight: 600, color: "#94a3b8" }}>관심종목</span>
        <span style={{ fontSize: 10, color: "#374151" }}>실시간</span>
      </div>
      {items.map((item) => (
        <WatchRow key={item.ticker} item={item}
          selected={item.ticker === selectedTicker}
          onSelect={() => onSelect(item.ticker)}
          onRemove={() => onRemove(item.ticker)} />
      ))}
      <div style={{ padding: "10px 14px", borderTop: "1px solid #0e1118", display: "flex", gap: 6 }}>
        <input value={input} onChange={(e) => setInput(e.target.value.toUpperCase())}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="티커 추가 (예: AMZN)"
          style={{ flex: 1, background: "#06080e", border: "1px solid #1e2130", borderRadius: 6,
            padding: "6px 10px", color: "#e2e8f0", fontSize: 12, outline: "none",
            fontFamily: "monospace" }} />
        <button onClick={submit}
          style={{ background: "#1d4ed8", border: "none", borderRadius: 6,
            color: "#fff", padding: "6px 10px", cursor: "pointer" }}>
          <Plus size={14} />
        </button>
      </div>
    </div>
  );
}
