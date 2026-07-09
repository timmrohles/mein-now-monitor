"""
Die Suchbegriffe, die täglich überwacht werden.

Aufgeteilt in:
- OUR_TARGETS: Begriffe, auf die unsere künftigen Modul-Titel zielen.
  Hier wollen wir wissen, wer aktuell rankt (Baseline vor Einreichung)
  und später, wo wir selbst landen.
- MARKET_WATCH: breitere Marktbegriffe, um Index-/Algo-Bewegungen
  früh zu erkennen (große Trefferzahlen reagieren empfindlich auf Änderungen).
- CONTROL_QUERIES: Kontroll-Suchen für die Thesen T6/T7.
- OUR_TITLES: die 7 finalen Modul-Titel als Suchqueries — sobald wir
  eingereicht sind, sehen wir hier direkt, wo unser Eintrag landet.
- TRIPLE_PATTERN_QUERIES: HECKER-Stil-Aufklärung (wer nutzt das Muster?).

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
    # Modul 5 — Tools (Vibe Coding + KI-Governance)
    "KI Governance",
    "Vibe Coding",
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
    # Die 7 finalen Modul-Titel — Baseline gegen die heutigen Treffer.
    # Sobald eingereicht, sehen wir hier direkt unsere Position.
    # M1 (Fundament) — Variante mit KI 3× für stärkeres Ranking bei "KI Marketing Manager".
    "KI-Marketing-Manager: KI-Agenten und KI-Automatisierung",
    # M2 (Owned) — Original, "Content" 2× (Doppelkeyword wirkt).
    "Content Marketing und Content Automatisierung mit KI",
    # M3 (Shared) — Original, "Social Media" 2×.
    "Social Media Marketing und Social Media Automatisierung mit KI",
    # M4 (Paid) — Neu mit SEO + SEA + Ads statt reinem Performance-Fokus.
    "Performance Marketing mit KI: SEO, SEA und Ads-Automatisierung",
    # M5 (Tools) — Vibe Coding + KI-Governance als neuer Modul-Fokus.
    "Vibe Coding und KI-Governance",
    # M6 (E-Commerce) — Original, "E-Commerce" 2×.
    "E-Commerce Marketing und E-Commerce Automatisierung mit KI",
    # M7 (B2B) — Original (Style-Kohärenz mit den anderen Modulen wichtiger als
    # HECKER-Struktur-Vorteil).
    "B2B Vertrieb und Sales-Automatisierung mit KI",
]

TRIPLE_PATTERN_QUERIES = [
    # HECKER-Stil: Topic + (Topic-Fachfrau / Topic-Fachmann) — bringt das
    # distinktive Kernwort 3× im Titel unter. Diese Queries dienen zwei Zwecken:
    # 1) Aufklärung — welche Anbieter nutzen das Tripple-Muster schon?
    # 2) Vorher-Nachher-Baseline, falls wir später eine Variante einreichen.
    "KI-Marketing-Manager (KI-Marketing-Fachfrau / KI-Marketing-Fachmann)",
    "Content Marketing (Content Marketing Fachfrau / Content Marketing Fachmann)",
    "Social Media Marketing (Social Media Fachfrau / Social Media Fachmann)",
    "Performance Marketing (Performance Marketing Fachfrau / Performance Marketing Fachmann)",
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
