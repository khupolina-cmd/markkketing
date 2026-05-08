#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from batch_signal_markup import build_package, infer_context, resolve_inputs


EMOJI = {
    "позитив": "🟢",
    "негатив": "🔴",
    "ожидание": "🟡",
    "сомнение": "🟠",
    "сравнение": "🔵",
    "сценарий": "🟣",
}

THEME_LABELS = {
    "smell": "запах",
    "moisture": "увлажнение",
    "nutrition": "питание",
    "absorption": "впитывание",
    "texture": "текстура",
    "packaging": "упаковка",
    "aesthetic": "эстетика",
    "effect": "эффект",
    "scenario": "сценарий",
    "comparison": "сравнение",
    "value": "цена",
    "volume": "объем",
    "composition": "состав",
    "quality": "качество",
    "usability": "удобство",
    "mismatch": "несоответствие",
    "safety": "переносимость",
    "misc": "разное",
    "other": "другое",
}


def escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def shorten(text: str, limit: int = 135) -> str:
    text = text.strip().replace("\n", " ")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def derive_theme_label(signal_code: str, category: str, fragment: str) -> str:
    prefix = signal_code.split(".", 1)[0]
    base = THEME_LABELS.get(prefix, prefix)
    if base == "разное":
        return shorten(fragment.lower(), 44)

    if category == "позитив":
        suffix = {
            "запах": "приятный",
            "увлажнение": "хорошее",
            "питание": "есть",
            "впитывание": "хорошее",
            "текстура": "приятная",
            "упаковка": "аккуратная",
            "эстетика": "сильная",
            "эффект": "есть",
            "цена": "нравится",
            "объем": "нравится",
            "качество": "нравится",
            "удобство": "есть",
            "сравнение": "в пользу товара",
            "сценарий": "контекст",
        }.get(base)
    elif category == "негатив":
        suffix = {
            "запах": "неприятный",
            "увлажнение": "слабое",
            "питание": "слабое",
            "впитывание": "плохое",
            "текстура": "не нравится",
            "упаковка": "проблемная",
            "эффект": "слабый",
            "качество": "плохое",
            "удобство": "плохое",
            "несоответствие": "есть",
            "переносимость": "плохая",
            "сравнение": "не в пользу товара",
        }.get(base)
    else:
        suffix = None

    return f"{base} {suffix}".strip() if suffix else base


def build_row_signals(package: dict) -> tuple[dict[str, list[str]], dict[tuple[str, str], dict]]:
    signals_by_unit: dict[str, list[str]] = defaultdict(list)
    theme_rollup: dict[tuple[str, str], dict] = {}

    for signal in package["signals_registry"]:
        category = signal["category"]
        emoji = EMOJI[category]
        theme = derive_theme_label(signal["signal_code"], category, signal["signal_fragment"])
        line = f"{emoji} {theme} — «{signal['signal_fragment']}»"
        if signal["secondary_flags"]:
            line += f" [{', '.join(signal['secondary_flags'])}]"
        signals_by_unit[signal["unit_index"]].append(line)

        key = (category, theme)
        bucket = theme_rollup.setdefault(
            key,
            {"category": category, "theme": theme, "review_ids": set(), "example": signal["signal_fragment"]},
        )
        bucket["review_ids"].add(signal["unit_index"])

    for item in package["manual_queue"]:
        signals_by_unit[item["unit_index"]].append(f"⚫ «{item['full_quote']}» — причина: {item['reason']}")
    for item in package["trash"]:
        signals_by_unit[item["unit_index"]].append(f"⚪ «{item['full_quote']}»")

    return signals_by_unit, theme_rollup


def render_overlay(package: dict) -> str:
    signals_by_unit, theme_rollup = build_row_signals(package)
    lines: list[str] = []
    add = lines.append

    add("# SIGNAL OVERLAY TABLE")
    add("")
    add(f"- product_key: `{package['product_key']}`")
    add(f"- product_name: `{package['product_name']}`")
    add(f"- source: `{package['source']}`")
    add(f"- source_file: [{Path(package['source_file']).name}]({package['source_file']})")
    add("")
    add("## Legend")
    add("- 🟢 позитив")
    add("- 🔴 негатив")
    add("- 🟡 ожидание")
    add("- 🟠 сомнение")
    add("- 🔵 сравнение")
    add("- 🟣 сценарий")
    add("- ⚫ ручной разбор")
    add("- ⚪ мусор")
    add("")
    add("## Overlay Table")
    add("| id | author | date | review | signals |")
    add("|---|---|---|---|---|")
    for unit in package["units_registry"]:
        unit_id = unit["unit_index"]
        signals_cell = "<br>".join(escape_cell(entry) for entry in signals_by_unit.get(unit_id, ["—"]))
        add(
            f"| {unit_id} | {escape_cell(unit['name'])} | {escape_cell(unit['date'])} | "
            f"{escape_cell(shorten(unit['full_quote'], 180))} | {signals_cell} |"
        )
    add("")
    add("## Manual Queue")
    if package["manual_queue"]:
        add("| id | author | fragment | reason |")
        add("|---|---|---|---|")
        for item in package["manual_queue"]:
            add(
                f"| {item['unit_index']} | {escape_cell(item['name'])} | "
                f"{escape_cell(shorten(item['full_quote'], 120))} | {escape_cell(item['reason'])} |"
            )
    else:
        add("- empty")
    add("")
    add("## Trash")
    if package["trash"]:
        add("| id | author | fragment |")
        add("|---|---|---|")
        for item in package["trash"]:
            add(f"| {item['unit_index']} | {escape_cell(item['name'])} | {escape_cell(shorten(item['full_quote'], 120))} |")
    else:
        add("- empty")
    add("")
    add("## Signal Stats")
    for key, value in package["stats"].items():
        add(f"- {key}: {value}")
    add("")
    add("### Theme Stats")
    clean_base = max(package["stats"]["B_clean"], 1)
    for item in sorted(theme_rollup.values(), key=lambda x: (x["category"], -len(x["review_ids"]), x["theme"])):
        emoji = EMOJI[item["category"]]
        people = len(item["review_ids"])
        percent = round((people / clean_base) * 100, 1)
        add(f"- {emoji} {item['theme']} — {people} человек ({percent}%) | пример: «{item['example']}»")
    add("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a one-pass signal overlay table for marketplace review exports.")
    parser.add_argument("inputs", nargs="+", help="Markdown review exports or directories.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional output directory.")
    parser.add_argument("--source-name", default="Wildberries", help="Source label.")
    parser.add_argument("--current-year", type=int, default=2026, help="Year used for missing year inference.")
    parser.add_argument("--current-month", type=int, default=4, help="Month used for missing year inference.")
    args = parser.parse_args()

    input_paths = resolve_inputs(args.inputs)
    if not input_paths:
        raise SystemExit("No valid markdown review exports found.")

    output_dir = args.output_dir.expanduser() if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    for input_path in input_paths:
        context = infer_context(input_path, args.source_name, args.current_year, args.current_month)
        package = build_package(input_path, context)
        overlay = render_overlay(package)
        target_dir = output_dir or input_path.parent
        out_path = target_dir / f"{input_path.stem}.signal-overlay-v1.md"
        out_path.write_text(overlay, encoding="utf-8")
        print(out_path)


if __name__ == "__main__":
    main()
