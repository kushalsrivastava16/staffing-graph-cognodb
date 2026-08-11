import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { getHealth } from "../api/health";

interface AppStatus {
  dbAvailable: boolean;
  checking: boolean;
}

const AppStatusContext = createContext<AppStatus>({ dbAvailable: true, checking: true });

const POLL_INTERVAL_MS = 30_000;

export function AppStatusProvider({ children }: { children: ReactNode }) {
  const [dbAvailable, setDbAvailable] = useState(true);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function check() {
      try {
        const health = await getHealth();
        if (!cancelled) setDbAvailable(health.status === "ok");
      } catch {
        if (!cancelled) setDbAvailable(false);
      } finally {
        if (!cancelled) setChecking(false);
      }
    }

    check();
    const interval = setInterval(check, POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  return <AppStatusContext.Provider value={{ dbAvailable, checking }}>{children}</AppStatusContext.Provider>;
}

export function useAppStatus() {
  return useContext(AppStatusContext);
}
