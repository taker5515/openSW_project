import { useState } from "react";
import { Activity, Bell, BellOff } from "lucide-react";
import { StockChart }        from "./components/StockChart";
import { Watchlist }         from "./components/Watchlist";
import { NewsSummary }       from "./components/NewsSummary";
import { useWatchlist }      from "./hooks/useWatchlist";
import { useNewsFeed }       from "./hooks/useNewsFeed";
import { useNotifications }  from "./hooks/useNotifications";

type Tab = "overview" | "news";

export default function App() {
  const [tab, setTab] = useState<Tab>(
    (new URLSearchParams(window.location.search).get("tab") as Tab) ?? "overview"
  );
  const [selectedTicker, setSelected] = useState("AAPL");
  const { watchlist, add, remove }    = useWatchlist();
  const { news, reanalyze }           = useNewsFeed();
  const { enabled, toggle }           = useNotifications();

  const selectedItem = watchlist.find((w) => w.ticker === selectedTicker) ?? watchlist[0];

  return (
        <div style={{ minHeight: "100vh", background: "#f8fafc", color: "#0f172a",
          fontFamily: "'Inter', 'Segoe UI', sans-serif" }}>
          <header style={{ height: 52, background: "#ffffff", borderBottom: "1px solid #e2e8f0",
            display: "flex", alignItems: "center", padding: "0 24px", gap: 16,
            position: "sticky", top: 0, zIndex: 100 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, fontWeight: 700, fontSize: 15 }}>
          <Activity size={18} color="#3b82f6" /> Stock Newsletter
        </div>

        <button onClick={toggle}
          style={{ background: "transparent", border: "1px solid #1e2130",
            borderRadius: 6, padding: "5px 9px", cursor: "pointer",
            color: enabled ? "#f59e0b" : "#94a3b8" }}>
          {enabled ? <Bell size={15} /> : <BellOff size={15} />}
        </button>
      </header>
      <main style={{ maxWidth: 1280, margin: "0 auto", padding: 24 }}>
        {tab === "overview" && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: 20 }}>
            <StockChart item={selectedItem} />
            <Watchlist
              items={watchlist}
              selectedTicker={selectedTicker}
              onSelect={setSelected}
              onAdd={add}
              onRemove={remove}
            />
          </div>
        )}
        {tab === "news" && (
          <div style={{ maxWidth: 720 }}>
            <NewsSummary news={news} onReanalyze={reanalyze} />
          </div>
        )}
      </main>
    </div>
  );
}