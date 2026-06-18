"""
Die Suchbegriffe, die täglich überwacht werden.

Aufgeteilt in:
- OUR_TARGETS: Begriffe, auf die unsere künftigen Modul-Titel zielen.
  Hier wollen wir wissen, wer aktuell rankt (Baseline vor Einreichung)
  und später, wo wir selbst landen.
- MARKET_WATCH: breitere Marktbegriffe, um Index-/Algo-Bewegungen
  früh zu erkennen (große Trefferzahlen reagieren empfindlich auf Änderungen).

Beim Hinzufügen: Begriff einfach in die Liste schreiben. Kurz halten
(1-4 Wörter), so wie ein Nutzer wirklich suchen würde.
"""

OUR_TARGETS = [
    # Modul 2 — Owned
    "Content Marketing",
    "KI Content Marketing",
    # Modul 3 — Shared
    "Social Media Marketing",
    "KI Social Media",
    # Modul 4 — Paid
    "Performance Marketing",
    "KI Performance Marketing",
    # Modul 5 — Tools
    "KI Automation",
    "Marketing Automation",
    # Modul 6 — E-Commerce
    "E-Commerce Marketing",
    "KI E-Commerce",
    # Modul 7 — B2B
    "B2B Vertrieb",
    "KI B2B Vertrieb",
    # Modul 1 / Dach
    "KI Marketing Manager",
    "KI Manager",
]

MARKET_WATCH = [
    # Große, empfindliche Begriffe — Frühwarnung für Index-/Algo-Bewegungen
    "KI",
    "Marketing",
    "KI Marketing",
    "Digital Marketing",
]

# Wie viele Plätze pro Begriff protokolliert werden
TOP_N = 20

ALL_QUERIES = OUR_TARGETS + MARKET_WATCH
