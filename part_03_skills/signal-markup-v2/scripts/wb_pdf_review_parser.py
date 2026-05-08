#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


NOISE_SUBSTRINGS = [
    "Выбор покупателей",
    "Важное из отзывов",
    "Текст составила нейросеть Wildberries",
    "Хотите что",
    "Задать вопрос продавцу",
    "Фото и видео",
    "Сортировать по",
    "Купить",
    "В корз",
    "© Wildberries",
    "Применяются",
    "Реклама",
    "Покупателям",
    "Продавцам и партнёрам",
    "Наши проекты",
    "Компания",
    "Смотреть все",
]

REPLY_MARKERS = [
    "Ответ продавца",
    "Ответ представителя",
    "Ответ бренда",
    "Представитель бренда",
]

FIELD_MARKERS = [
    "Достоинства:",
    "Недостатки:",
    "Комментарий:",
    "Плюсы товара",
    "Минусы товара",
    "Первоначальный отзыв",
]

STATUS_RE = re.compile(r"\b(Выкупили|Отказались)\b")
RUS_DATE_RE = re.compile(
    r"\b\d{1,2}\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+\d{4}\b",
    re.I,
)


def clean_space(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ")).strip()


def is_noise(line: str) -> bool:
    s = clean_space(line)
    if not s:
        return True
    if any(marker in s for marker in NOISE_SUBSTRINGS):
        return True
    if re.fullmatch(r"\d+[\d\s]*₽", s):
        return True
    if re.fullmatch(r"[0-9· ]+", s):
        return True
    if re.fullmatch(r"\d+\s*мл", s, re.I):
        return True
    if re.fullmatch(r"[👍❤️💔🔥😍😘☺️🙏💕🌷✨🤍🧡👌🏻🫠😉😁🎄💛🤤🥰👌💖 ]+", s):
        return True
    return False


def is_inline_card_noise(line: str) -> bool:
    s = clean_space(line)
    if not s:
        return False
    if "₽" in s and "оцен" in s:
        return True
    if re.search(r"/\s*Крем", s):
        return True
    if any(token in s for token in ["Off.Scrub", "REPOSE FLAVOUR", "TOUCHY", "LABORATORIUM", "Vellore"]):
        if "₽" in s or "оцен" in s:
            return True
    return False


def normalize_field_value(value: str) -> str:
    s = clean_space(value)
    if not s:
        return "—"
    if is_inline_card_noise(s):
        return "—"
    s = re.sub(r"\d+[\d\s]*₽", " ", s)
    s = re.sub(r"\d+,\d+\s*·\s*\d+\s*оценки", " ", s, flags=re.I)
    s = re.sub(r"\b255\b", " ", s)
    s = re.sub(r"\bПлюсы товара\b", " ", s)
    s = re.sub(r"\bМинусы товара\b", " ", s)
    s = clean_space(s)
    return s or "—"


def is_bad_author_candidate(line: str) -> bool:
    s = clean_space(line)
    if not s:
        return True
    if any(marker in s for marker in REPLY_MARKERS + FIELD_MARKERS):
        return True
    if is_noise(s):
        return True
    if any(token in s for token in ["₽", "Off.Scrub", "оценки", "Купить", "В корз"]):
        return True
    return False


def extract_text(pdf_path: Path) -> str:
    try:
        return subprocess.check_output(
            ["pdftotext", "-layout", "-nopgbrk", str(pdf_path), "-"],
            text=True,
        )
    except FileNotFoundError:
        raise SystemExit("pdftotext is not installed")


def detect_review_starts(lines: list[str]) -> list[tuple[int, int]]:
    starts: list[tuple[int, int]] = []
    seen_author_lines: set[int] = set()
    for idx, line in enumerate(lines):
        if not STATUS_RE.search(line):
            continue
        author_idx = None
        for j in range(idx - 1, max(-1, idx - 7), -1):
            candidate = clean_space(lines[j])
            if is_bad_author_candidate(candidate):
                continue
            author_idx = j
            break
        if author_idx is None or author_idx in seen_author_lines:
            continue
        starts.append((author_idx, idx))
        seen_author_lines.add(author_idx)
    return starts


def parse_block(block_lines: list[str], status_line: str, source_order: int) -> dict:
    author = clean_space(block_lines[0])
    status = "Отказались" if "Отказались" in status_line else "Выкупили"
    current = None
    in_reply = False
    fields = {
        "general": [],
        "pros_text": [],
        "cons_text": [],
        "comment": [],
        "pros_tags": [],
        "cons_tags": [],
        "seller_reply": [],
    }
    detected_date = None

    for raw in block_lines[1:]:
        line = clean_space(raw)
        if not line:
            continue
        if detected_date is None:
            date_match = RUS_DATE_RE.search(line)
            if date_match:
                detected_date = date_match.group(0)
                continue
        if STATUS_RE.search(line):
            continue
        if any(marker in line for marker in REPLY_MARKERS):
            in_reply = True
            current = "seller_reply"
            continue
        if in_reply:
            if not is_noise(line):
                fields["seller_reply"].append(line)
            continue
        if line == "Плюсы товара":
            current = "pros_tags"
            continue
        if line == "Минусы товара":
            current = "cons_tags"
            continue
        if line == "Первоначальный отзыв":
            continue
        if is_noise(line):
            continue
        if is_inline_card_noise(line):
            continue

        matched = False
        for prefix, key in [
            ("Достоинства:", "pros_text"),
            ("Недостатки:", "cons_text"),
            ("Комментарий:", "comment"),
        ]:
            if line.startswith(prefix):
                current = key
                value = clean_space(line[len(prefix):])
                if value:
                    fields[key].append(value)
                matched = True
                break
        if matched:
            continue

        if current in ("pros_text", "cons_text", "comment"):
            fields[current].append(line)
        elif current in ("pros_tags", "cons_tags"):
            fields[current].append(line)
        else:
            fields["general"].append(line)

    return {
        "id": source_order,
        "author": author or "—",
        "date": detected_date or "—",
        "purchase_status": status,
        "general": normalize_field_value(" ".join(fields["general"])),
        "pros_text": normalize_field_value(" ".join(fields["pros_text"])),
        "cons_text": normalize_field_value(" ".join(fields["cons_text"])),
        "comment": normalize_field_value(" ".join(fields["comment"])),
        "pros_tags": normalize_field_value(" ".join(fields["pros_tags"])),
        "cons_tags": normalize_field_value(" ".join(fields["cons_tags"])),
        "seller_reply_present": bool(fields["seller_reply"]),
        "seller_reply_text": normalize_field_value(" ".join(fields["seller_reply"])),
    }


def parse_reviews(pdf_path: Path) -> dict:
    text = extract_text(pdf_path)
    lines = [line.rstrip() for line in text.splitlines()]
    starts = detect_review_starts(lines)
    rows = []
    for idx, (author_idx, status_idx) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        block = lines[author_idx:end]
        row = parse_block(block, lines[status_idx], idx + 1)
        rows.append(row)
    return {
        "parser": "wb_pdf_review_parser",
        "parser_version": "1",
        "source_file": str(pdf_path),
        "row_count": len(rows),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Wildberries review PDF into normalized rows")
    parser.add_argument("pdf", help="Path to Wildberries review PDF")
    parser.add_argument("-o", "--output", help="Write JSON output to file instead of stdout")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    result = parse_reviews(pdf_path)
    payload = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        out_path = Path(args.output).expanduser()
        out_path.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
        if not payload.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
