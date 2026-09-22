"""Tokenize Chordonomicon progressions for model training."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Iterable


SPECIAL_TOKENS = ("<pad>", "<unk>", "<bos>", "<eos>")
ROOTS = ("C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B")
QUALITIES = (
    "",
    "m",
    "min",
    "maj",
    "dim",
    "aug",
    "sus2",
    "sus4",
    "6",
    "7",
    "9",
    "11",
    "13",
    "maj7",
    "maj9",
    "m7",
    "min7",
    "m9",
    "min9",
    "dim7",
    "aug7",
    "add9",
    "add13",
)
CHORD_VOCABULARY = tuple(f"{root}{quality}" for root in ROOTS for quality in QUALITIES)
TOKEN_PATTERN = re.compile(r"<[^>\s]+>|[^\s]+")
SECTION_PATTERN = re.compile(r"^<[^>\s]+>$")


def normalize_chord(token: str) -> str:
    """Normalize dataset chord spelling without changing its musical meaning."""
    token = token.strip()
    if not token or SECTION_PATTERN.fullmatch(token):
        return token
    token = token.split("/", 1)[0]
    token = token.replace("♯", "s").replace("#", "s")
    token = token.replace("♭", "b").replace("-", "m")
    token = re.sub(r"no3d$", "", token)
    token = re.sub(r"^([A-Ga-g])([sb]?)(.*)$", lambda match: match.group(1).upper() + match.group(2) + match.group(3), token)
    flat_roots = {"Db": "Cs", "Eb": "Ds", "Gb": "Fs", "Ab": "Gs", "Bb": "As"}
    token = next((sharp + token[len(flat):] for flat, sharp in flat_roots.items() if token.startswith(flat)), token)
    token = token.replace("minor", "min").replace("major", "maj")
    return token


def build_vocabulary(section_tokens: Iterable[str]) -> dict[str, int]:
    """Build the stable token-to-ID mapping used by preprocessing and training."""
    tokens = list(SPECIAL_TOKENS) + list(CHORD_VOCABULARY)
    tokens.extend(sorted(set(section_tokens)))
    return {token: token_id for token_id, token in enumerate(dict.fromkeys(tokens))}


def genre_from_row(row: dict[str, str]) -> str:
    """Use the single-label field, with the serialized genre field as fallback."""
    genre = (row.get("main_genre") or "").strip()
    if genre:
        return genre
    genres = (row.get("genres") or "").strip().strip("'")
    return genres or "unknown"


def preprocess(input_path: Path, output_dir: Path) -> tuple[int, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    records_path = output_dir / "tokenized.jsonl"

    section_tokens: set[str] = set()
    with input_path.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            for token in TOKEN_PATTERN.findall(row.get("chords", "")):
                normalized = normalize_chord(token)
                if SECTION_PATTERN.fullmatch(normalized):
                    section_tokens.add(normalized)

    vocabulary = build_vocabulary(section_tokens)
    unknown_count = 0
    record_count = 0
    with input_path.open(newline="", encoding="utf-8") as source, records_path.open("w", encoding="utf-8") as target:
        for row in csv.DictReader(source):
            raw_chords = row.get("chords", "")
            tokens = [normalize_chord(token) for token in TOKEN_PATTERN.findall(raw_chords)]
            if not tokens:
                continue
            token_ids = []
            for token in tokens:
                token_id = vocabulary.get(token, vocabulary["<unk>"])
                unknown_count += token_id == vocabulary["<unk>"]
                token_ids.append(token_id)
            target.write(json.dumps({"id": row.get("id", ""), "tokens": token_ids, "genre": genre_from_row(row)}) + "\n")
            record_count += 1

    (output_dir / "vocabulary.json").write_text(json.dumps(vocabulary, indent=2) + "\n", encoding="utf-8")
    (output_dir / "metadata.json").write_text(
        json.dumps(
            {
                "input": str(input_path),
                "records": record_count,
                "vocabulary_size": len(vocabulary),
                "unknown_tokens": unknown_count,
                "genre_column": "main_genre (fallback: genres)",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return record_count, unknown_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("dataset/raw/chordonomicon_v2.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("dataset/processed"))
    args = parser.parse_args()
    records, unknowns = preprocess(args.input, args.output_dir)
    print(f"Processed {records} records with {unknowns} unknown tokens.")


if __name__ == "__main__":
    main()