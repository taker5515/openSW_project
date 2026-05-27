import { useState, useEffect } from "react";
import type { WatchItem } from "../types";
import { INITIAL_WATCHLIST, genHistory } from "../utils/mockData";

export function useWatchlist() {
  const [watchlist, setWatchlist] = useState<WatchItem[]>(INITIAL_WATCHLIST);

  useEffect(() => {
    const id = setInterval(() => {
      setWatchlist((prev) =>
        prev.map((w) => {
          const delta = (Math.random() - 0.495) * w.price * 0.002;
          const price = Math.max(1, +(w.price + delta).toFixed(2));
          const change = +(w.change + delta).toFixed(2);
          const changePct = +((change / (price - change)) * 100).toFixed(2);
          const history = [...w.history.slice(-19), price];
          return { ...w, price, change, changePct, history };
        })
      );
    }, 2500);
    return () => clearInterval(id);
  }, []);

  const add = (ticker: string) => {
    if (!ticker || watchlist.find((w) => w.ticker === ticker)) return;
    const base = Math.random() * 400 + 50;
    const change = +(Math.random() * 10 - 5).toFixed(2);
    setWatchlist((prev) => [
      ...prev,
      {
        ticker,
        name: `${ticker} Corporation`,
        price: +base.toFixed(2),
        change,
        changePct: +((change / base) * 100).toFixed(2),
        history: genHistory(base),
      },
    ]);
  };

  const remove = (ticker: string) =>
    setWatchlist((prev) => prev.filter((w) => w.ticker !== ticker));

  return { watchlist, add, remove };
}
