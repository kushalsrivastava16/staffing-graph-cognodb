import { useAppStatus } from "../../context/AppStatusContext";

export function DbStatusBanner() {
  const { dbAvailable, checking } = useAppStatus();

  if (checking || dbAvailable) return null;

  return (
    <div className="db-banner" role="alert">
      The graph database is unreachable right now. Data won't load until the connection is restored — this
      usually means the CognoDB instance is asleep, misconfigured, or the backend can't reach it.
    </div>
  );
}
