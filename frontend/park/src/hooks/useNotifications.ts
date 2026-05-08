 import { useState, useCallback } from "react";

export function useNotifications() {
  const [enabled, setEnabled] = useState(false);

  const toggle = useCallback(async () => {
    if (!("Notification" in window)) return;

    if (!enabled) {
      const permission = await Notification.requestPermission();
      if (permission === "granted") {
        setEnabled(true);
        new Notification("StockAI 대시보드", {
          body: "알림이 활성화되었습니다. 중요 시그널을 알려드릴게요.",
        });
      }
    } else {
      setEnabled(false);
    }
  }, [enabled]);

  const push = useCallback(
    (title: string, body: string) => {
      if (enabled && Notification.permission === "granted") {
        new Notification(title, { body });
      }
    },
    [enabled]
  );

  return { enabled, toggle, push };
}