"""
Anomalie-Erkennung: vergleicht die zwei neuesten JSON-Snapshots in
docs/data/ und meldet Auffälligkeiten. Schwellen oben anpassbar.

Nutzung:
    python detect_changes.py
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
DATA_DIR  = REPO_ROOT / "docs" / "data"

# --- Schwellen ---
POSITION_JUMP = 5        # Positionssprung ab X Plätzen = auffällig
TOTAL_PCT     = 0.15     # Trefferzahl-Änderung ab 15 % = auffällig


def load_index():
    idx_file = DATA_DIR / "index.json"
    if not idx_file.exists():
        return []
    return json.loads(idx_file.read_text(encoding="utf-8")).get("dates", [])


def load_snapshot(date):
    return json.loads((DATA_DIR / f"{date}.json").read_text(encoding="utf-8"))


def detect():
    dates = load_index()
    if len(dates) < 2:
        print("Noch nicht genug Snapshots (mindestens 2 nötig).")
        return

    new_date, old_date = dates[0], dates[1]
    new = load_snapshot(new_date)
    old = load_snapshot(old_date)
    print(f"Vergleich: {old['run_at'][:16]}  →  {new['run_at'][:16]}\n")

    alerts = []

    # 1. Trefferzahl-Sprünge
    for q, d in new["queries"].items():
        old_q = old["queries"].get(q)
        if not old_q:
            continue
        old_total = old_q.get("total_results")
        new_total = d.get("total_results")
        if old_total and new_total:
            change = (new_total - old_total) / old_total
            if abs(change) >= TOTAL_PCT:
                alerts.append(
                    f"[TREFFERZAHL] '{q}': {old_total} → {new_total} "
                    f"({change*100:+.0f} %)  — möglicher Index-/Algo-Wechsel"
                )

    # 2. Positionssprünge je Angebot + neue Top-5 + verschwundene
    for q, d in new["queries"].items():
        old_q = old["queries"].get(q, {"results": []})
        old_pos = {r["angebot_id"]: r["position"] for r in old_q.get("results", [])}
        new_pos = {r["angebot_id"]: r["position"] for r in d["results"]}
        new_titel = {r["angebot_id"]: (r["titel"] or "")[:45] for r in d["results"]}
        old_titel = {r["angebot_id"]: (r["titel"] or "")[:45] for r in old_q.get("results", [])}

        for aid, np in new_pos.items():
            op = old_pos.get(aid)
            if op is None:
                if np <= 5:
                    alerts.append(
                        f"[NEU TOP5] '{q}': {new_titel.get(aid,'?')} "
                        f"neu auf Platz {np}"
                    )
            else:
                jump = op - np
                if abs(jump) >= POSITION_JUMP:
                    pfeil = "▲" if jump > 0 else "▼"
                    alerts.append(
                        f"[SPRUNG {pfeil}] '{q}': {new_titel.get(aid,'?')} "
                        f"Platz {op} → {np}"
                    )

        for aid, op in old_pos.items():
            if aid not in new_pos and op <= 10:
                alerts.append(
                    f"[WEG] '{q}': {old_titel.get(aid,'?')} war Platz {op}, "
                    f"heute nicht mehr in Top-{len(new_pos)}"
                )

    if not alerts:
        print("Keine Auffälligkeiten über den Schwellen. Markt stabil.")
    else:
        print(f"{len(alerts)} Auffälligkeit(en):\n")
        for a in alerts:
            print("  " + a)


if __name__ == "__main__":
    detect()
