"""
Lokaler Lauf zum Testen.

Nutzung:
    python run_local.py --dry     # nur Abfrage, schreibt nichts
    python run_local.py           # echter Lauf, schreibt docs/data/<heute>.json
"""
import sys
from collector import run_snapshot, fetch_query
from queries import ALL_QUERIES, OUR_TARGETS


def dry_run():
    """Fragt nur ab und zeigt Ergebnisse, schreibt NICHTS."""
    print("TROCKENLAUF — nur Abfrage, kein Schreiben\n")
    for q in OUR_TARGETS:
        try:
            total, angebote = fetch_query(q, top_n=5)
            print(f"'{q}'  ({total} Treffer)")
            for i, a in enumerate(angebote, 1):
                titel = (a.get("titel") or "")[:50]
                anb = (a.get("bildungsanbieter", {}) or {}).get("name", "")[:22]
                print(f"   {i}. [{anb:22}] {titel}")
            print()
        except Exception as e:   # noqa: BLE001
            print(f"   FEHLER: {e}\n")


if __name__ == "__main__":
    if "--dry" in sys.argv:
        dry_run()
    else:
        print(f"Starte Snapshot über {len(ALL_QUERIES)} Begriffe ...\n")
        result = run_snapshot(verbose=True)
        print("\nErgebnis:")
        print(f"  Datum:    {result['date']}")
        print(f"  Zeilen:   {result['rows_written']}")
        print(f"  Begriffe: {result['queries']}")
        if result["errors"]:
            print(f"  Fehler:   {len(result['errors'])}")
            for q, e in result["errors"]:
                print(f"     - {q}: {e}")
