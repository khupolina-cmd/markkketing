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


def shorten(text: str, limit: int = 110) -> str:
    text = text.strip().replace("\n", " ")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def escape_table(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def derive_theme_label(signal_code: str, category: str, fragment: str) -> str:
    prefix = signal_code.split(".", 1)[0]
    base = THEME_LABELS.get(prefix, prefix)
    if base == "разное":
        return shorten(fragment.lower(), 42)
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
            "сценарий": "контекст",
            "сравнение": "в пользу товара",
        }.get(base)
    elif category == "негатив":
        suffix = {
            "запах": "неприятный",
            "увлажнение": "слабое",
            "питание": "слабое",
            "впитывание": "плохое",
            "текстура": "не нравится",
            "упаковка": "проблемная",
            "эстетика": "не спасает",
            "эффект": "слабый",
            "цена": "спорная",
            "объем": "не нравится",
            "качество": "плохое",
            "удобство": "плохое",
            "сценарий": "ломается",
            "сравнение": "не в пользу товара",
            "несоответствие": "есть",
            "переносимость": "плохая",
        }.get(base)
    else:
        suffix = None
    return f"{base} {suffix}".strip() if suffix else base


def render_dashboard(package: dict) -> str:
    units_by_id = {unit["unit_index"]: unit for unit in package["units_registry"]}
    signals_by_unit: dict[str, list[dict]] = defaultdict(list)
    for signal in package["signals_registry"]:
        signals_by_unit[signal["unit_index"]].append(signal)

    manual_by_unit: dict[str, list[dict]] = defaultdict(list)
    for item in package["manual_queue"]:
        manual_by_unit[item["unit_index"]].append(item)

    trash_by_unit: dict[str, list[dict]] = defaultdict(list)
    for item in package["trash"]:
        trash_by_unit[item["unit_index"]].append(item)

    theme_rollup: dict[tuple[str, str], dict] = {}
    for signal in package["signals_registry"]:
        category = signal["category"]
        theme = derive_theme_label(signal["signal_code"], category, signal["signal_fragment"])
        key = (category, theme)
        bucket = theme_rollup.setdefault(
            key,
            {"review_ids": set(), "example": signal["signal_fragment"], "category": category, "theme": theme},
        )
        bucket["review_ids"].add(signal["unit_index"])

    lines: list[str] = []
    add = lines.append

    add("# SIGNAL DASHBOARD V2")
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
    add("## Normalized Reviews Table")
    add("| id | author | date | review |")
    add("|---|---|---|---|")
    for unit in package["units_registry"]:
        add(
            f"| {unit['unit_index']} | {escape_table(unit['name'])} | {escape_table(unit['date'])} | {escape_table(shorten(unit['full_quote'], 140))} |"
        )
    add("")
    add("## Review Dashboard")
    for unit in package["units_registry"]:
        unit_id = unit["unit_index"]
        add(f"### {unit_id} | {unit['name']} | {unit['date']}")
        add(f"> {unit['full_quote']}")
        add("")
        if signals_by_unit.get(unit_id):
            add("Signals")
            for signal in signals_by_unit[unit_id]:
                category = signal["category"]
                emoji = EMOJI[category]
                theme = derive_theme_label(signal["signal_code"], category, signal["signal_fragment"])
                flags = f" | flags: {', '.join(signal['secondary_flags'])}" if signal["secondary_flags"] else ""
                add(f"- {emoji} {category} | тема: {theme} | фрагмент: «{signal['signal_fragment']}»{flags}")
        if manual_by_unit.get(unit_id):
            if not signals_by_unit.get(unit_id):
                add("Signals")
            for item in manual_by_unit[unit_id]:
                add(f"- ⚫ ручной разбор | фрагмент: «{item['full_quote']}» | причина: {item['reason']}")
        if trash_by_unit.get(unit_id):
            add("Signals")
            for item in trash_by_unit[unit_id]:
                add(f"- ⚪ мусор | фрагмент: «{item['full_quote']}»")
        add("")
    add("## Manual Queue")
    if package["manual_queue"]:
        add("| id | author | fragment | reason |")
        add("|---|---|---|---|")
        for item in package["manual_queue"]:
            add(
                f"| {item['unit_index']} | {escape_table(item['name'])} | {escape_table(shorten(item['full_quote'], 120))} | {escape_table(item['reason'])} |"
            )
    else:
        add("- empty")
    add("")
    add("## Trash")
    if package["trash"]:
        add("| id | author | fragment |")
        add("|---|---|---|")
        for item in package["trash"]:
            add(f"| {item['unit_index']} | {escape_table(item['name'])} | {escape_table(shorten(item['full_quote'], 120))} |")
    else:
        add("- empty")
    add("")
    add("## Signal Stats")
    for key, value in package["stats"].items():
        add(f"- {key}: {value}")
    add("")
    add("### Theme Stats")
    clean_base = max(package["stats"]["B_clean"], 1)
    sorted_rollup = sorted(
        theme_rollup.values(),
        key=lambda item: (item["category"], -len(item["review_ids"]), item["theme"]),
    )
    for item in sorted_rollup:
        category = item["category"]
        emoji = EMOJI[category]
        people = len(item["review_ids"])
        percent = round((people / clean_base) * 100, 1)
        add(f"- {emoji} {item['theme']} — {people} человек ({percent}%) | пример: «{item['example']}»")
    add("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render readable signal dashboards with colored emoji categories.")
    parser.add_argument("inputs", nargs="+", help="One or more markdown review exports or directories.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional output directory.")
    parser.add_argument("--source-name", default="Wildberries", help="Source label.")
    parser.add_argument("--current-year", type=int, default=2026, help="Year used for missing year inference.")
    parser.add_argument("--current-month", type=int, default=4, help="Month used for missing year inference.")
    args = parser.parse_args()

    inputs = resolve_inputs(args.inputs)
    if not inputs:
        raise SystemExit("No valid markdown review exports found.")

    output_dir = args.output_dir.expanduser() if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    for input_path in inputs:
        context = infer_context(input_path, args.source_name, args.current_year, args.current_month)
        package = build_package(input_path, context)
        dashboard = render_dashboard(package)
        target_dir = output_dir or input_path.parent
        output_path = target_dir / f"{input_path.stem}.signal-dashboard-v2.md"
        output_path.write_text(dashboard, encoding="utf-8")
        print(output_path)


if __name__ == "__main__":
    main()
