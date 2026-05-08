 import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import type { Signal } from "../types";

const CONFIG = {
  BUY:     { bg: "#0d2e1a", border: "#1a5c30", color: "#34d270", Icon: TrendingUp,  label: "매수" },
  SELL:    { bg: "#2e0d0d", border: "#5c1a1a", color: "#f87171", Icon: TrendingDown, label: "매도" },
  NEUTRAL: { bg: "#1e1e12", border: "#4a4a1a", color: "#facc15", Icon: Minus,        label: "중립" },
} satisfies Record<Signal, unknown>;

export function SignalBadge({ signal }: { signal: Signal }) {
  const { bg, border, color, Icon, label } = CONFIG[signal];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4,
      background: bg, border: `1px solid ${border}`, color,
      borderRadius: 6, padding: "3px 10px",
      fontSize: 12, fontWeight: 700, letterSpacing: "0.04em",
      whiteSpace: "nowrap",
    }}>
      <Icon size={11} />
      {label}
    </span>
  );
}