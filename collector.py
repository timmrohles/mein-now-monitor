"""
Kern-Logik des Sammlers: fragt mein-NOW ab und schreibt einen Snapshot
als JSON-Datei in docs/data/. Der GitHub-Actions-Workflow committed das
zurück ins Repo; das statische Dashboard liest dieselben Dateien.
"""
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

try:
    from .queries import ALL_QUERIES, TOP_N    # bei Package-Import
except ImportError:
    from queries import ALL_QUERIES, TOP_N     # bei direktem Aufruf

MEIN_NOW_URL = "https://rest.mein-now.de/now-prod/suche/pc/v1/bildungsangebot"
MEIN_NOW_KEY = "infosysbub-nowsuche"

REPO_ROOT = Path(__file__).resolve().parent
DATA_DIR  = REPO_ROOT / "docs" / "data"


def fetch_query(query, top_n=TOP_N, retries=2):
    """Fragt einen Suchbegriff ab, gibt (total_results, [angebote]) zurueck."""
    url = (f"{MEIN_NOW_URL}?sw={urllib.parse.quote(query)}"
           f"&bg=true&size={top_n}")
    req = urllib.request.Request(
        url,
        headers={"X-API-Key": MEIN_NOW_KEY, "User-Agent": "Mozilla/5.0"},
    )
    last_err = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read())
            total = data.get("page", {}).get("totalElements")
            angebote = data.get("_embedded", {}).get("bildungsangebotDTOList", [])
            return total, angebote
        except Exception as e:                       # noqa: BLE001
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Abfrage '{query}' fehlgeschlagen: {last_err}")


def _iso_utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0) \
        .isoformat().replace("+00:00", "Z")


def run_snapshot(verbose=False):
    """Kompletter Lauf: alle Begriffe abfragen, Tagesdatei + Index schreiben."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    run_at = _iso_utc_now()
    today  = run_at[:10]                     # YYYY-MM-DD

    snapshot = {"run_at": run_at, "queries": {}}
    errors   = []

    for q in ALL_QUERIES:
        try:
            total, angebote = fetch_query(q)
            results = []
            for pos, a in enumerate(angebote, start=1):
                results.append({
                    "position":   pos,
                    "angebot_id": str(a.get("id", "")),
                    "titel":      (a.get("titel") or "")[:300],
                    "anbieter":   (a.get("bildungsanbieter", {}) or {})
                                   .get("name", "")[:200],
                    "termine":    a.get("anzahlTermine"),
                })
            snapshot["queries"][q] = {
                "total_results": total,
                "results":       results,
            }
            if verbose:
                print(f"  [ok] {q}: {total} Treffer, {len(results)} erfasst")
            time.sleep(0.6)
        except Exception as e:               # noqa: BLE001
            errors.append((q, str(e)))
            if verbose:
                print(f"  [!!] {q}: {e}")

    # Tagesdatei schreiben (ueberschreibt, falls am selben Tag erneut gelaufen)
    day_file = DATA_DIR / f"{today}.json"
    day_file.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Index aktualisieren (idempotent: Datum wird nur einmal aufgenommen)
    index_file = DATA_DIR / "index.json"
    if index_file.exists():
        index = json.loads(index_file.read_text(encoding="utf-8"))
    else:
        index = {"dates": []}
    if today not in index["dates"]:
        index["dates"].append(today)
    index["dates"].sort(reverse=True)
    index_file.write_text(
        json.dumps(index, indent=2),
        encoding="utf-8",
    )

    return {
        "date":         today,
        "run_at":       run_at,
        "queries":      len(snapshot["queries"]),
        "rows_written": sum(len(qd["results"])
                            for qd in snapshot["queries"].values()),
        "errors":       errors,
    }
