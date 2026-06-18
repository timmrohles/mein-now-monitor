"""
Kern-Logik des Sammlers: fragt mein-NOW ab und schreibt einen Snapshot
als JSON-Datei in docs/data/. Der GitHub-Actions-Workflow committed das
zurück ins Repo; das statische Dashboard liest dieselben Dateien.

Speichert pro Eintrag zusätzlich abgeleitete Metriken, die die im Doc
formulierten Ranking-Thesen verifizierbar machen:
- titel_len, inhalt_len  -> These „Kürze hilft" / Inhaltslänge ↔ Position
- q_in_titel             -> Vorkommen des Suchphrase im Titel
- q_in_inhalt            -> Vorkommen des Suchphrase im Inhalt
- q_words_in_titel       -> Wort-für-Wort Treffer im Titel (Doppelkeyword-Effekt)

Pro Begriff zusätzlich Diagnose-Metadaten der mein-NOW-Engine:
- removed_token, korrektur_vorschlag
"""
import html
import json
import re
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

# Wörter <2 Buchstaben werden ignoriert. "KI" (2 Zeichen) bleibt erlaubt.
MIN_WORD_LEN = 2


def fetch_query(query, top_n=TOP_N, retries=2):
    """Fragt einen Suchbegriff ab.

    Returns: (total_results, [angebote], meta_dict)
    meta_dict enthält: removed_token, korrektur_vorschlag
    """
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
            meta = {
                "removed_token": data.get("removedToken", "") or "",
                "korrektur_vorschlag": data.get("korrekturVorschlag", "") or "",
            }
            return total, angebote, meta
        except Exception as e:                       # noqa: BLE001
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Abfrage '{query}' fehlgeschlagen: {last_err}")


def _iso_utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0) \
        .isoformat().replace("+00:00", "Z")


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE  = re.compile(r"\s+")


def _strip_html(s):
    if not s:
        return ""
    s = _TAG_RE.sub(" ", s)
    s = html.unescape(s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def _wb_count(needle, haystack):
    """Case-insensitive Anzahl der Phrase/des Wortes im Text mit Wortgrenzen."""
    if not needle or not haystack:
        return 0
    pattern = r"\b" + re.escape(needle.lower()) + r"\b"
    return len(re.findall(pattern, haystack.lower()))


def _query_words(query):
    """Suchwörter ≥ MIN_WORD_LEN Buchstaben, lowercase, ohne Klammern."""
    cleaned = re.sub(r"[()]", " ", query)
    return [w for w in cleaned.lower().split() if len(w) >= MIN_WORD_LEN]


def _words_in_text_count(words, text):
    """Summe aller Vorkommen der Wörter im Text (mit Wortgrenzen)."""
    if not text or not words:
        return 0
    return sum(_wb_count(w, text) for w in words)


def _metrics_for_entry(query, titel, inhalt_text):
    """Berechnet die Verifikations-Metriken für einen Ergebnis-Eintrag."""
    q_words = _query_words(query)
    return {
        "titel_len":         len(titel),
        "inhalt_len":        len(inhalt_text),
        "q_in_titel":        _wb_count(query, titel),
        "q_in_inhalt":       _wb_count(query, inhalt_text),
        "q_words_in_titel":  _words_in_text_count(q_words, titel),
    }


def run_snapshot(verbose=False):
    """Kompletter Lauf: alle Begriffe abfragen, Tagesdatei + Index schreiben."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    run_at = _iso_utc_now()
    today  = run_at[:10]                     # YYYY-MM-DD

    snapshot = {"run_at": run_at, "queries": {}}
    errors   = []

    for q in ALL_QUERIES:
        try:
            total, angebote, meta = fetch_query(q)
            results = []
            for pos, a in enumerate(angebote, start=1):
                titel  = (a.get("titel") or "")[:300]
                inhalt = _strip_html(a.get("inhalt") or "")
                metrics = _metrics_for_entry(q, titel, inhalt)
                results.append({
                    "position":   pos,
                    "angebot_id": str(a.get("id", "")),
                    "titel":      titel,
                    "anbieter":   (a.get("bildungsanbieter", {}) or {})
                                   .get("name", "")[:200],
                    "termine":    a.get("anzahlTermine"),
                    **metrics,
                })
            snapshot["queries"][q] = {
                "total_results":       total,
                "removed_token":       meta["removed_token"],
                "korrektur_vorschlag": meta["korrektur_vorschlag"],
                "results":             results,
            }
            if verbose:
                print(f"  [ok] {q}: {total} Treffer, {len(results)} erfasst")
            time.sleep(0.6)
        except Exception as e:               # noqa: BLE001
            errors.append((q, str(e)))
            if verbose:
                print(f"  [!!] {q}: {e}")

    # Tagesdatei schreiben (überschreibt, falls am selben Tag erneut gelaufen)
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
