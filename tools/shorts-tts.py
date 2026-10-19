#!/usr/bin/env python3
"""
shorts-tts.py – Erzeugt Sprachausgabe für Shorts mit Microsoft Neural Voices (kostenlos, kein API-Key).

Installation (einmalig):
    pip3 install --user edge-tts

Nutzung:
    python3 shorts-tts.py -t "Dein Text hier" -o ausgabe.mp3
    python3 shorts-tts.py -f skript.txt -o skript.mp3
    python3 shorts-tts.py -f skript.txt -v de-DE-ConradNeural -r "+10%"
    python3 shorts-tts.py --voices           # alle deutschen Stimmen anzeigen

Tipps:
    - Rate (Geschwindigkeit): "-r +10%" ist für Shorts oft angenehmer.
    - Danach MP3 + Text in CapCut importieren, Auto-Untertitel (deutsch) drüberlegen.
"""

import argparse
import sys

DEUTSCHE_STIMMEN = {
    "de-DE-KatjaNeural": "Weiblich, standard – gut für die meisten Shorts",
    "de-DE-ConradNeural": "Männlich, ruhig, sachlich",
    "de-DE-AmalaNeural": "Weiblich, jung, stimmlich etwas heller",
    "de-DE-KillianNeural": "Männlich, etwas tiefer",
}


def main():
    parser = argparse.ArgumentParser(description="KI-Stimme für Shorts (kostenlos via edge-tts)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", help="Direkter Text")
    group.add_argument("-f", "--file", help="Textdatei (z.B. ein Skript)")
    group.add_argument("--voices", action="store_true", help="Verfügbare deutschen Stimmen anzeigen")
    parser.add_argument("-o", "--output", default="output.mp3", help="Ausgabedatei (default: output.mp3)")
    parser.add_argument("-v", "--voice", default="de-DE-KatjaNeural", help="Stimme (default: de-DE-KatjaNeural)")
    parser.add_argument("-r", "--rate", default="+0%", help='Tempo, z.B. "+10%" oder "-5%"')
    args = parser.parse_args()

    if args.voices:
        print("Verfügbare deutsche Stimmen:")
        for name, beschreibung in DEUTSCHE_STIMMEN.items():
            print(f"  {name:26s} – {beschreibung}")
        print("\nAlle Stimmen: python3 -m edge_tts --list-voices | grep de-DE")
        return

    try:
        import edge_tts  # noqa: F401
    except ImportError:
        sys.exit("edge-tts fehlt. Installiere es mit:  pip3 install --user edge-tts")

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read().strip()
    else:
        text = args.text.strip()

    if not text:
        sys.exit("Kein Text vorhanden.")

    import asyncio

    async def synth():
        communicate = edge_tts.Communicate(text, args.voice, rate=args.rate)
        await communicate.save(args.output)

    asyncio.run(synth())
    dauer = len(text.split()) / 2.5  # grobe Schätzung: ~2.5 Wörter/Sekunde
    print(f"✓ {args.output} erstellt  (~{dauer:.0f}s Sprache, {len(text.split())} Wörter, Stimme: {args.voice})")


if __name__ == "__main__":
    main()
