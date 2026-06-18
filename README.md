# mein-NOW Ranking Monitor

**Live-Dashboard:** https://timmrohles.github.io/mein-now-monitor/

Täglicher Snapshot der mein-NOW-Suchergebnisse für unsere Ziel-Begriffe.
Erkennt Positionsänderungen, neue Wettbewerber und mögliche Algo-/Index-Wechsel.

**Zweck:** Baseline aufbauen, *bevor* eigene Maßnahmen eingereicht sind — damit
wir später normales Rauschen von echter Bewegung unterscheiden können.

---

## Was es tut

- GitHub Actions führt täglich 06:00 UTC den Collector aus.
- Der Collector fragt für jeden Begriff die mein-NOW-API ab (Top-20 pro Begriff).
- Ergebnis wird als JSON-Datei `docs/data/<YYYY-MM-DD>.json` ins Repo committed.
- Ein statisches Dashboard auf GitHub Pages liest dieselben JSON-Dateien.
- `detect_changes.py` vergleicht lokal die zwei neuesten Snapshots und meldet
  Auffälligkeiten — dieselbe Logik läuft auch im Browser-Dashboard.

Kein LLM im Messpfad — die Messung ist deterministisch.

---

## Dateien

| Datei | Zweck |
|---|---|
| `queries.py` | Die überwachten Suchbegriffe (hier pflegen) |
| `collector.py` | Kern: API abfragen + JSON schreiben |
| `run_local.py` | Lokaler Test-Lauf (auch Trockenlauf) |
| `detect_changes.py` | Anomalie-Erkennung zwischen den letzten zwei Tagen |
| `.github/workflows/daily.yml` | GitHub Actions Cron + Commit-Back |
| `docs/index.html` | Statisches Dashboard |
| `docs/data/*.json` | Vom Workflow geschriebene Snapshots |

---

## Lokal testen

```bash
python run_local.py --dry     # nur Abfrage, schreibt nichts
python run_local.py           # echter Lauf, schreibt docs/data/<heute>.json
python detect_changes.py      # Vergleich der zwei letzten Snapshots
```

Keine externen Dependencies — nur Python-Standardbibliothek.

---

## Begriffe pflegen

In `queries.py`:
- `OUR_TARGETS` — Begriffe, auf die unsere künftigen Modul-Titel zielen.
- `MARKET_WATCH` — große Begriffe als Frühwarnung für Algo-Bewegungen.

Beim Hinzufügen: Begriff einfach in die Liste schreiben. Kurz halten (1–4 Wörter),
so wie ein Nutzer wirklich suchen würde. Commit + Push reicht — der nächste
Cron-Lauf erfasst den neuen Begriff automatisch.

---

## Fairness / Limits

- ~18 Begriffe × 1×/Tag = ~18 Abfragen täglich. Moderate, normale Nutzung.
- Nicht hochdrehen (kein Minuten-Takt, keine hunderte Begriffe) — das wäre unfair
  gegenüber der BA-Infrastruktur.
- Der Collector pausiert 0,6 s zwischen Abfragen.

---

## Grenzen (ehrlich)

- Gut messbar: eigene Position, neue Wettbewerber, grobe Algo-/Index-Brüche.
- Nicht messbar: der unsichtbare Tie-Breaker (vermutlich Teilnehmer-Bewertungen
  und Datenfrische) — die API liefert dazu keine Felder. Wir sehen *Bewegung*,
  aber nicht immer den *Grund*.
