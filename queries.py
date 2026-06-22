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

CONTROL_QUERIES = [
    # These „Wortreihenfolge ist egal" — Vergleich mit "KI Marketing" (in MARKET_WATCH).
    # Wenn total_results und Top-10 identisch sind, ist die Reihenfolge tatsächlich egal.
    "Marketing KI",
    # These „Klammern werden ignoriert" — gleiche Vergleichsbasis "KI Marketing".
    # Wenn identisch zu "KI Marketing", werden Klammern wie nicht vorhanden behandelt.
    "(KI) Marketing",
]

OUR_TITLES = [
    # Geplante eigene Modul-Titel (noch nicht im Index). Baseline jetzt
    # gegen die heutigen Treffer — sobald eingereicht, sehen wir hier
    # direkt, wo unser eigener Eintrag für die exakte Titel-Suche landet.
    "Marketing Manager mit KI: Agenten und Automatisierung",
    "Content Marketing und Content Automatisierung mit KI",
    "Social Media Marketing und Social Media Automatisierung mit KI",
    "Performance Marketing und Ads-Automatisierung mit KI",
    "Marketing-Automation Manager: Pipelines, MCP und Workflows mit KI",
    "E-Commerce Marketing und E-Commerce Automatisierung mit KI",
    "B2B Vertrieb und Sales-Automatisierung mit KI",
]

TRIPLE_PATTERN_QUERIES = [
    # HECKER-Stil: Topic + (Topic-Fachfrau / Topic-Fachmann) — bringt das
    # distinktive Kernwort 3× im Titel unter. Diese Queries dienen zwei Zwecken:
    # 1) Aufklärung — welche Anbieter nutzen das Tripple-Muster schon?
    # 2) Wenn wir später selbst eine Variante mit diesem Muster einreichen,
    #    haben wir die Vorher-Nachher-Baseline.
    "KI-Marketing-Manager (KI-Marketing-Fachfrau / KI-Marketing-Fachmann)",
    "Content Marketing (Content Marketing Fachfrau / Content Marketing Fachmann)",
    "Social Media Marketing (Social Media Fachfrau / Social Media Fachmann)",
    "Performance Marketing (Performance Marketing Fachfrau / Performance Marketing Fachmann)",
    "Marketing Automation (Marketing Automation Fachfrau / Marketing Automation Fachmann)",
    "E-Commerce Marketing (E-Commerce Fachfrau / E-Commerce Fachmann)",
    "B2B Vertrieb (B2B Sales Fachfrau / B2B Sales Fachmann)",
]

# Wie viele Plätze pro Begriff protokolliert werden
TOP_N = 20

ALL_QUERIES = (
    OUR_TARGETS
    + MARKET_WATCH
    + CONTROL_QUERIES
    + OUR_TITLES
    + TRIPLE_PATTERN_QUERIES
)
