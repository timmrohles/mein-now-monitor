# Inbetriebnahme mein-NOW Ranking Monitor + Dashboard

**Datum:** 2026-06-18
**Status:** Approved (Design)
**Scope:** Minimal-Go-Live des Collectors via GitHub Actions, mit JSON-Dateien im Repo als Datenspeicher und kleinem statischen Dashboard auf GitHub Pages — komplett ohne externe Datenbank.

---

## Ziel

Den vorhandenen Collector produktiv schalten, sodass täglich automatisch ein
Snapshot der mein-NOW-Suchergebnisse für die in `queries.py` definierten
Begriffe als JSON-Datei in das Repo geschrieben wird. Zusätzlich eine
kleine statische Web-Seite, auf der die aktuellen Top-10 pro Begriff plus
die Auffälligkeiten des letzten Tages sichtbar sind.

## Architekturentscheidung 1: GitHub Actions statt Vercel-Cron

Vercel-Hobby limitiert Functions auf 10 s, unsere Läufe brauchen ~25–30 s.
GitHub Actions hat keine relevante Timeout-Grenze, kein Code-Splitting nötig.

## Architekturentscheidung 2: JSON-Dateien im Repo statt Supabase

Ursprünglich war Supabase Postgres geplant. Alternativen waren JSON-im-Repo
und Turso (SQLite + HTTP).

Entscheidung: **JSON-Dateien im Repo selbst.** Begründung:
- Null externe Infrastruktur, kein Account, kein Key zu verwalten
- Daten sind durch Git automatisch versioniert — pro Tag ein klarer Diff
- Alles lebt auf einer Plattform (GitHub)
- Dashboard kann die JSON-Dateien direkt von der selben GH-Pages-Origin
  laden — kein CORS, kein RLS, keine Auth
- Datenvolumen ist klein genug (~50 KB pro Snapshot ⇒ <20 MB nach einem
  Jahr) dass die Repo-Größe kein Problem ist

Trade-off: **`collector.py` wird umgeschrieben** (Supabase-REST-Calls
raus, Schreibe-Logik für JSON-Dateien rein). `detect_changes.py` ebenfalls
(liest JSON statt Supabase). Schema-SQL fällt komplett weg.

## Architekturentscheidung 3: Statisches Dashboard auf GitHub Pages

Statische HTML-Seite im selben Repo unter `docs/index.html`. Vanilla JS/CSS,
Pico.css per CDN. Lädt JSON-Dateien aus dem selben Pages-Pfad
(`docs/data/...`), keine externen Calls.

## Architektur

**Collector-Pfad:**
- **GitHub Actions Workflow** (täglich 06:00 UTC) → `python run_local.py`
  in einem Ubuntu-Runner.
- **`collector.py`** (umgeschrieben) — fragt mein-NOW ab, schreibt eine
  Datei `docs/data/<YYYY-MM-DD>.json` plus aktualisiert `docs/data/index.json`.
- **Workflow committed die neuen Dateien zurück ins Repo** mit
  `${{ secrets.GITHUB_TOKEN }}` und `permissions: contents: write`.
- **`queries.py`** — unverändert.
- **`run_local.py`** — leicht angepasst (`--dry` bleibt; "echter Lauf" ruft
  jetzt die neue Datei-Schreib-Logik statt Supabase auf).
- **`detect_changes.py`** — liest die zwei neuesten JSON-Dateien aus
  `docs/data/`, gleiche Vergleichslogik.
- **`schema.sql`** — gelöscht.

**Dashboard-Pfad:**
- **`docs/index.html`** — vanilla HTML. Lädt zuerst `data/index.json`
  (Liste der vorhandenen Datumsdateien), dann die zwei neuesten
  Tagesdateien. Rendert Auffälligkeiten-Box und Top-10-Listen.
- **GitHub Pages** — Source: `main` Branch, Folder `/docs`. Daten und
  Dashboard liegen unter der selben Origin, daher kein CORS.

**Vercel-Reste** (`api/cron.py`, `vercel.json`) werden gelöscht.

## Dateiformat

**`docs/data/<YYYY-MM-DD>.json`** — ein Snapshot:
```json
{
  "run_at": "2026-06-18T06:00:12Z",
  "queries": {
    "Content Marketing": {
      "total_results": 4170,
      "results": [
        {"position": 1, "angebot_id": "12345",
         "titel": "Content Marketing Manager", "anbieter": "Beispiel GmbH",
         "termine": 5}
      ]
    }
  }
}
```

**`docs/data/index.json`** — Sortier-Index, neueste zuerst:
```json
{
  "dates": ["2026-06-18", "2026-06-17", "2026-06-16"]
}
```

Pro Run kommt eine neue Datumsdatei dazu und `index.json` wird neu
geschrieben. Wenn am selben Tag mehrere Runs passieren (manueller Re-Trigger),
wird die Tagesdatei überschrieben — pro Tag bleibt also genau eine.

## Dashboard-Inhalt

1. **Auffälligkeiten-Box oben** — Zusammenfassung aus den letzten zwei
   Snapshots: "X Sprünge, Y neue Top-5, Z Trefferzahl-Wechsel", darunter
   konkrete Beispiele. Gleiche Schwellen wie `detect_changes.py`
   (POSITION_JUMP=5, TOTAL_PCT=0.15).
2. **Pro Suchbegriff: Top-10-Liste** — Position, Titel, Anbieter, daneben
   ▲/▼ mit Positionsdifferenz seit gestern oder "NEU".

**Bewusst nicht drauf:** keine Charts, keine Klick-Details, keine
Kachel-Übersicht.

## Inbetriebnahme-Reihenfolge

1. **Code anpassen** — `collector.py` und `detect_changes.py` für
   JSON-Speicherung umschreiben. `run_local.py` minimal anpassen.
2. **Vercel-Reste + `schema.sql` löschen.**
3. **`.gitignore` anlegen.**
4. **Lokaler Trockenlauf** — `python run_local.py --dry` prüft API.
5. **Lokaler echter Lauf** — schreibt `docs/data/<heute>.json`.
6. **README anpassen** (alle Supabase- und Vercel-Erwähnungen raus).
7. **Dashboard `docs/index.html`** anlegen.
8. **Git init + GitHub-Repo erstellen** (öffentlich, weil GH Pages auf
   privaten Repos Pro braucht).
9. **Workflow `.github/workflows/daily.yml`** anlegen — mit
   `permissions: contents: write` und Commit-Back-Step.
10. **Workflow manuell triggern** zur Validierung.
11. **GitHub Pages aktivieren** (Source: `main`, Folder `/docs`).
12. **Dashboard im Browser prüfen.**

## Abnahme-Kriterien (Done)

- In `docs/data/` liegen mindestens zwei Snapshot-JSONs.
- GitHub Actions: letzter Run grün, hat eigenständig committed; nächster
  Cron-Run für morgen geplant.
- Dashboard-URL erreichbar, zeigt Top-10 + Auffälligkeiten-Box.
- `detect_changes.py` läuft lokal ohne Exception gegen die JSON-Dateien.
- README spiegelt JSON-Stack (kein Supabase, kein Vercel).

## Explizit nicht im Scope

- Keine Änderungen an `queries.py`.
- Keine externe Datenbank.
- Keine E-Mail-/Slack-Alerts.
- Keine Charts oder Verlaufsdiagramme im Dashboard.
- Keine Interaktivität im Dashboard.
- Kein automatisches `is_ours = true`-Markieren (Feld wandert ins JSON-Format,
  kann später manuell gepflegt werden).

## Risiken & Annahmen

- **mein-NOW-API-Stabilität** — Retry (2×, Backoff 2s/4s) reicht. Strukturelle
  Response-Änderungen scheitern hart — akzeptiert.
- **GH-Actions-Cron-Drift** — kann mehrere Minuten verzögern, für Tages-
  granularität irrelevant.
- **Commit-Back vom Workflow** — Standard-Token + `contents: write` reicht.
  Bot-Commits mit fester Author-Email (`github-actions[bot]`), kein Loop-Risiko
  weil der Workflow nicht auf `push` triggert.
- **Repo-Wachstum** — ~50 KB/Tag × 365 = 18 MB/Jahr. Akzeptabel auf Jahre.
- **Race-Conditions bei manuellem Re-Trigger am selben Tag** — die Datums-
  Datei wird überschrieben, das ist ok. `index.json` braucht Idempotenz
  (Datum nur einmal in der Liste).
- **Fehlschläge unbeobachtet** — GitHub schickt bei default-Settings eine
  Mail bei fehlgeschlagenen Runs.

## Offene Punkte für den Implementierungsplan

- Konkreter Inhalt von `.gitignore`, `.github/workflows/daily.yml`,
  umgeschriebene `collector.py` / `detect_changes.py`, `docs/index.html`.
- Sprache des Dashboards: Deutsch.
