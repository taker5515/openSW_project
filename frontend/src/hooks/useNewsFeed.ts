import { useState } from "react";
import type { NewsItem, Signal } from "../types";
import { INITIAL_NEWS } from "../utils/mockData";

const SYSTEM_PROMPT = `You are a financial analyst. Respond ONLY with valid JSON:
{"summary":"2-sentence Korean analysis","signal":"BUY"|"SELL"|"NEUTRAL"}`;

export function useNewsFeed() {
  const [news, setNews] = useState<NewsItem[]>(INITIAL_NEWS);

  const setLoading = (id: string, loading: boolean) =>
    setNews((prev) => prev.map((n) => (n.id === id ? { ...n, loading } : n)));

  const reanalyze = async (id: string) => {
    const item = news.find((n) => n.id === id);
    if (!item) return;

    setLoading(id, true);
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: SYSTEM_PROMPT,
          messages: [{ role: "user", content: `Headline: ${item.title}` }],
        }),
      });

      const data = await res.json();
      const text = data.content?.[0]?.text ?? "{}";
      const parsed = JSON.parse(text.replace(/```json|```/g, "").trim()) as {
        summary: string;
        signal: Signal;
      };

      setNews((prev) =>
        prev.map((n) =>
          n.id === id
            ? { ...n, loading: false, summary: parsed.summary ?? n.summary, signal: parsed.signal ?? n.signal }
            : n
        )
      );
    } catch {
      setLoading(id, false);
    }
  };

  return { news, reanalyze };
}
