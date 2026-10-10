#!/usr/bin/env python3
"""Editable source for the Dutch electricity market figures (Python 3.9+).

Run from any directory to regenerate both SVGs; --check compares without writing.
Only the Python standard library is required. See docs/market-diagrams.md.
"""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "src/assets/diagrams"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

# Shared palette and typography. All styles are embedded in the exported SVGs.
INK = "#2b382e"
GREEN = "#315f48"
MUTED = "#596658"
PAPER = "#fcfbf6"
SOFT = "#f0f3e9"
BORDER = "#cbd6bd"
BLUE = "#265a80"
BLUE_SOFT = "#edf2f7"
BLUE_BORDER = "#b8cbd9"
DARK = "#234f3b"
WHITE = "#f8f8ef"
FONT = "Arial, Helvetica, sans-serif"
WIDTH = 560


class Drawing:
    """Small SVG helpers; coordinates are pixels and text y values are baselines."""

    def __init__(self, height, title, description, *, clock=False):
        self.root = ET.Element(f"{{{SVG_NS}}}svg", {
            "width": str(WIDTH), "height": str(height),
            "viewBox": f"0 0 {WIDTH} {height}",
            "role": "img", "aria-labelledby": "title desc",
        })
        self.add("title", id="title").text = title
        self.add("desc", id="desc").text = description
        self.rect(1, 1, WIDTH - 2, height - 2, PAPER, "#d2d7c9",
                  radius=16 if clock else 10, **({"stroke_width": 2} if clock else {}))

    def add(self, tag, **attributes):
        return ET.SubElement(self.root, f"{{{SVG_NS}}}{tag}", {
            key.replace("_", "-"): str(value) for key, value in attributes.items()
        })

    def text(self, x, y, label, size=20, bold=False, fill=INK, **attributes):
        self.add("text", x=x, y=y, font_family=FONT, font_size=size,
                 font_weight="700" if bold else "normal", font_style="normal",
                 fill=fill, **attributes).text = label

    def rect(self, x, y, width, height, fill=SOFT, stroke=BORDER, radius=10, **attributes):
        if stroke is not None:
            attributes["stroke"] = stroke
        self.add("rect", x=x, y=y, width=width, height=height,
                 rx=radius, fill=fill, **attributes)

    def down(self, x, y):
        self.add("path", d=f"M {x} {y} v 18", stroke=GREEN, stroke_width=2)
        self.add("path", d=f"M {x-5} {y+15} l 5 7 l 5 -7 Z", fill=GREEN)

    def right(self, x, y):
        self.add("path", d=f"M {x} {y} h 24", stroke=GREEN, stroke_width=2)
        self.add("path", d=f"M {x+20} {y-5} l 7 5 l -7 5 Z", fill=GREEN)

    def svg(self):
        ET.indent(self.root, space="  ")
        return ET.tostring(self.root, encoding="unicode") + "\n"


def reserve_row(drawing, y, name, full_name, response, color):
    """A reserve's procurement and activation, aligned on the same row."""
    drawing.rect(22, y, 516, 150)
    drawing.add("rect", x=22, y=y + 10, width=5, height=130, fill=color)
    drawing.text(42, y + 32, name, 24, True, color)
    drawing.text(132, y + 31, full_name, 18, True)
    drawing.text(42, y + 66, "BEFORE DELIVERY", 15, True, MUTED)
    drawing.text(308, y + 66, "DURING DELIVERY", 15, True, MUTED)
    for index, line in enumerate(["Procure capacity", "in advance"]):
        drawing.text(42, y + 99 + index * 27, line)
    for index, line in enumerate(response):
        drawing.text(308, y + 99 + index * 27, line)
    drawing.right(266, y + 100)


def market_sequence():
    d = Drawing(1390, "Dutch electricity markets and parallel grid services", (
        "Energy trading progresses from forward contracts through day-ahead and intraday. "
        "FCR, aFRR and mFRR each have reserve capacity procured in advance and activation "
        "as needed during delivery. GOPACS coordinates day-ahead congestion arrangements "
        "and intraday redispatch, with local adjustments during delivery. These services "
        "operate in parallel. Post-delivery trading where available and residual imbalance "
        "settlement follow delivery."
    ))
    d.text(26, 36, "ONE DELIVERY INTERVAL", 16, True, GREEN)
    d.text(26, 76, "Markets and grid services", 28, True)
    d.text(26, 109, "Time moves from before to during to after delivery.", 18, fill=MUTED)

    # Energy trading before delivery.
    d.rect(22, 132, 516, 254)
    d.text(42, 167, "BEFORE DELIVERY · ENERGY TRADING", 16, True, GREEN)
    d.text(46, 207, "Forward contracts & futures", 22, True)
    d.text(46, 234, "Agree supply or hedge prices ahead.", 19)
    d.down(58, 243)
    d.text(46, 293, "Day-ahead auction", 22, True)
    d.down(58, 303)
    d.text(46, 353, "Intraday auctions & continuous trading", 22, True)
    d.text(26, 427, "Parallel services for the same interval", 24, True)
    d.text(26, 458, "Each row below runs alongside energy trading.", 18, fill=MUTED)

    # Edit the labels, response lines, colors, or row positions here.
    reserves = [
        (480, "FCR", "Frequency containment reserve",
         ["Automatic response", "to frequency"], "#795516"),
        (646, "aFRR", "Automatic frequency restoration reserve",
         ["Automatic control", "restores balance"], BLUE),
        (812, "mFRR", "Manual frequency restoration reserve",
         ["Activation on request", "supports restoration"], "#6c4b85"),
    ]
    for row in reserves:
        reserve_row(d, *row)

    # Congestion management is parallel to the reserve services.
    d.rect(22, 978, 516, 156, BLUE_SOFT, BLUE_BORDER)
    d.text(42, 1011, "GOPACS · Congestion management", 23, True, BLUE)
    d.text(42, 1045, "BEFORE DELIVERY", 15, True, MUTED)
    d.text(308, 1045, "DURING DELIVERY", 15, True, MUTED)
    d.text(42, 1077, "Day-ahead limits")
    d.text(42, 1105, "Intraday redispatch")
    d.right(266, 1077)
    d.text(308, 1077, "Adjust local flows")
    d.text(308, 1105, "as agreed")
    d.text(26, 1167, "Activate reserves as needed; their functions can overlap.", 18, fill=MUTED)
    d.text(26, 1194, "GOPACS addresses local congestion, not system balance.", 18, fill=MUTED)

    # Commercial accounting after physical delivery.
    d.rect(22, 1220, 516, 116, DARK, DARK)
    d.text(42, 1252, "AFTER DELIVERY", 16, True, WHITE)
    d.text(42, 1285, "Post-delivery trading, where available", 21, True, WHITE)
    d.text(42, 1315, "→ Settlement of remaining imbalances", 21, True, WHITE)
    d.text(26, 1369, "Schematic timing · product-specific rules apply", 18, fill=MUTED)
    return d.svg()


def auction_event(drawing, y, time, label, coverage, *, capacity=False):
    """One deadline; square marker denotes capacity, round marker denotes energy."""
    drawing.text(36, y, time, 22, True, GREEN)
    if capacity:
        drawing.add("rect", x=118, y=y - 15, width=14, height=14,
                    fill=PAPER, stroke=GREEN, stroke_width=2)
    else:
        drawing.add("circle", cx=125, cy=y - 8, r=7, fill=GREEN)
    drawing.text(150, y, label, 21, True)
    drawing.text(150, y + 31, coverage)


def auction_clock():
    d = Drawing(1524, "Auction deadlines for delivery at 18:00–18:15 in the Netherlands", (
        "On the previous day, FCR capacity closes at 08:00, day-ahead energy at 12:00, "
        "IDA1 at 15:00, and IDA2 at 22:00. On the delivery day, IDA3 closes at 10:00 "
        "and covers noon to midnight. The example delivery is 18:00–18:15. Continuous "
        "intraday trading runs alongside auctions until the applicable gate closure. "
        "Post-delivery trading where available and imbalance settlement follow physical "
        "delivery. In parallel, aFRR and mFRR reserve capacity is procured before delivery; "
        "GOPACS coordinates day-ahead arrangements and intraday redispatch. During delivery, "
        "FCR responds to frequency, aFRR follows automatic control, mFRR responds on request, "
        "and agreed congestion adjustments change local flows."
    ), clock=True)
    d.text(26, 36, "EXAMPLE DELIVERY · 18:00–18:15 ON D", 16, True, GREEN, letter_spacing=1)
    d.text(26, 74, "The auction clock", 28, True)
    d.text(26, 108, "Dutch local market time · CET / CEST", 18, fill=MUTED)

    # D−1. These are order deadlines, not auction result publication times.
    d.rect(22, 134, 516, 50, "#e7ecdd", None, radius=8)
    d.text(40, 167, "D−1 · The previous day", 23, True)
    d.add("path", d="M 125 220 V 551", stroke="#7a8b72", stroke_width=3)
    auction_event(d, 232, "08:00", "FCR capacity auction closes",
                  "Reserve availability for D.", capacity=True)
    d.text(150, 290, "Capacity, rather than an energy sale.", 18, fill=MUTED)
    d.add("path", d="M 148 310 H 516", stroke="#7a8b72", stroke_dasharray="6 5")
    for y, time, label in [
        (348, "12:00", "Day-ahead auction closes"),
        (431, "15:00", "IDA1 closes"),
        (514, "22:00", "IDA2 closes"),
    ]:
        auction_event(d, y, time, label, "Energy for all of D.")

    # No single deadline is implied for these parallel arrangements.
    d.rect(22, 568, 516, 156, BLUE_SOFT, BLUE_BORDER)
    d.text(40, 601, "IN PARALLEL · BEFORE DELIVERY", 16, True, BLUE)
    d.text(40, 636, "aFRR & mFRR: procure reserve capacity.", 21, True)
    d.text(40, 667, "GOPACS: day-ahead arrangements", 21, True)
    d.text(40, 696, "and intraday redispatch for congestion.")

    # D: the final IDA followed by the example physical delivery interval.
    d.rect(22, 748, 516, 50, "#e7ecdd", None, radius=8)
    d.text(40, 781, "D · The delivery day", 23, True)
    d.add("path", d="M 125 834 V 888", stroke="#7a8b72", stroke_width=3)
    auction_event(d, 846, "10:00", "IDA3 closes", "Energy for 12:00–24:00 on D.")
    d.rect(22, 912, 516, 298, DARK, None)
    d.text(40, 946, "18:00–18:15 · PHYSICAL DELIVERY", 16, True, WHITE, letter_spacing=1)
    d.text(40, 982, "Produce, consume & balance", 23, True, WHITE)
    for y, label in [
        (1017, "FCR · automatic frequency response"),
        (1053, "aFRR · automatic restoration control"),
        (1089, "mFRR · restoration on request"),
        (1132, "GOPACS · agreed local adjustments"),
    ]:
        d.text(40, y, label, 20, True, WHITE)
    d.text(40, 1175, "Parallel actions; reserve functions can overlap.", 18, fill=WHITE)

    # After delivery, plus the reminder about continuous trading.
    d.text(40, 1249, "After this interval ↓", 21, True)
    d.text(40, 1281, "Post-delivery trading, where available,")
    d.text(40, 1309, "then settlement of residual imbalances.")
    d.rect(22, 1336, 516, 128, "#e7ecdd", None, radius=8)
    d.text(40, 1369, "Continuous intraday trading", 21, True)
    for y, label in [
        (1400, "Runs alongside the IDAs, until the"),
        (1428, "applicable gate closure. Deadlines"),
        (1456, "depend on the contract and trading route."),
    ]:
        d.text(40, y, label)
    d.text(26, 1502, "Order deadlines · spacing is not to scale", 18, fill=MUTED)
    return d.svg()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if an SVG is missing or out of date; do not write.")
    args = parser.parse_args()
    figures = {
        "dutch-market-sequence.svg": market_sequence(),
        "dutch-market-auction-clock.svg": auction_clock(),
    }
    stale = False
    for name, svg in figures.items():
        path = OUTPUT_DIR / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                print(f"Missing or out of date: {name}")
                stale = True
        else:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(svg, encoding="utf-8")
            print(f"Generated {name}")
    if args.check and not stale:
        print("Both market diagrams match their editable source.")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
