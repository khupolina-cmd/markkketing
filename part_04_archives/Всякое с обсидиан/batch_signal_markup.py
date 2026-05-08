#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}

MARKER_RE = re.compile(r"(Достоинства|Недостатки|Комментарий):")
DATE_RE = re.compile(
    r"^(?P<day>\d{1,2}) (?P<month>[а-я]+)(?: (?P<year>\d{4}))?, "
    r"(?P<hour>\d{2}):(?P<minute>\d{2})(?:\s*·\s*Дополнен)?$"
)

KNOWN_NOUNS = (
    "запах",
    "аромат",
    "упаковка",
    "тюбик",
    "текстура",
    "дизайн",
    "вид",
    "объем",
    "объём",
    "крем",
    "эффект",
    "цвет",
    "качество",
    "липкость",
    "финиш",
)

ANCHOR_MARKERS = (
    "запах",
    "аромат",
    "увлаж",
    "впиты",
    "липк",
    "пленк",
    "текстур",
    "упаков",
    "тюбик",
    "дизайн",
    "эстет",
    "визуал",
    "цвет",
    "качеств",
    "эффект",
    "мягк",
    "бархат",
    "сух",
    "жирн",
    "крышк",
    "объем",
    "объём",
    "подар",
    "сумк",
)

TRASH_PHRASES = {
    "спасибо",
    "спасибо большое",
    "спасибо огромное",
    "ну",
    "главное",
    "конечно",
    "наверное",
    "не знаю",
    "разумеется",
    "вкусный",
    "приятный",
    "легкий",
    "заказала",
    "понравился",
    "балдеж",
}

LIST_CODE_MAP = {
    "цвет": "aesthetic.color",
    "качество": "quality.plus",
    "плохое качество": "quality.minus",
    "текстура": "texture.plus",
    "хорошо пахнет": "smell.plus",
    "плохо пахнет": "smell.minus",
    "запах": "smell.minus",
    "хороший эффект": "effect.plus",
    "нет эффекта": "effect.minus",
    "эффект от средства": "effect.minus",
    "удобно пользоваться": "usability.plus",
    "состав": "composition.minus",
    "другое": "other.minus",
    "хорошая цена": "value.plus",
    "приятный запах": "smell.plus",
    "отличное качество": "quality.plus",
    "легко использовать": "usability.plus",
}

GENERIC_TRASH = {
    "очень понравился",
    "классный",
    "классный !!!",
    "любимый крем",
    "мне понравился крем",
    "советую",
    "идеальный за такую цену",
    "очень понравился кремушек",
    "всё замечательно спасибо",
    "все нравится в нем",
    "вне конкуренции) 10 ⭐ из 5)",
    "отличный крем спасибо",
    "очень классный крем",
    "крем очень понравился",
    "прекрасный крем",
    "я очень рада",
    "веусный",
    "он прекрасен!✨",
    "он прекрасен✨",
    "все",
    "все отлично",
    "хороший сам по себе",
    "отличный крем",
    "хороший крем",
    "крем понравился",
}

POSITIVE_HINTS = [
    "приятн",
    "вкусно",
    "крутой",
    "невероятн",
    "потрясающ",
    "бархат",
    "мягк",
    "нежн",
    "шелков",
    "быстро впиты",
    "впитывается",
    "моментально",
    "не лип",
    "без липк",
    "не оставляет пленки",
    "увлажняет",
    "питает",
    "красив",
    "эстет",
    "стильн",
    "хорошо упак",
    "достойно упак",
    "идеально упак",
    "приятно открывать",
    "легко распределяется",
    "парфюмерный",
    "стойкий",
    "ненавязчив",
    "не раздражающ",
    "не бьет в голову",
    "легкий",
    "обалденный",
    "кайфушный",
    "замечательный",
    "отличнл увлажняет",
    "смягчает",
    "нормально",
]

NEGATIVE_HINTS = [
    "плохо пах",
    "запах так себе",
    "запах ужас",
    "на любителя",
    "неприятн",
    "навязчив",
    "душн",
    "сильно парфюм",
    "не пахнет",
    "без какого-либо запаха",
    "без запаха",
    "очень слабый запах",
    "слабый запах",
    "приторн",
    "бабушкин",
    "лекарств",
    "детскую присыпку",
    "не увлажняет",
    "увлажняет плохо",
    "питания не хватило",
    "не питает",
    "среднее увлажнение",
    "не сильно увлажняет",
    "суховат",
    "сухими",
    "плохо впитывается",
    "смывается пленкой",
    "пленк",
    "жиденьк",
    "жидкий",
    "выливается",
    "вытекать",
    "грязный",
    "мятый",
    "помятый",
    "вскрытый",
    "полуоткрыта",
    "жжёт",
    "жжет",
    "аллерг",
    "нет эффекта",
    "ужасном состоянии",
    "соль вместо",
    "не такой",
    "не очень",
    "едкий",
    "удушливый",
    "трещаться",
    "трескаться",
]

EXPECT_HINTS = [
    "ожидал",
    "ожидала",
    "думала",
    "не думала",
    "не ожидала",
    "не рассчитывала",
    "рассчитывала",
    "брала",
    "взяла",
    "выбирала из-за",
    "для визуала",
    "для дизайна",
    "для эстетики",
    "из-за эстетичного",
    "из-за классного дизайна",
    "ничего особенно не ждала",
    "описание хорошее",
    "отзывы тоже",
]

DOUBT_HINTS = [
    "надеюсь",
    "подойд",
    "не будет ли",
    "боюсь",
    "опасаюсь",
    "сомневаюсь",
    "не уверена",
]

SCENARIO_HINTS = [
    "на подарок",
    "в подарок",
    "подруж",
    "дочке",
    "жене",
    "сестр",
    "маме",
    "в сумке",
    "на ночь",
    "после мытья рук",
    "зимой",
    "третий раз беру",
    "2-ой раз",
    "второй раз",
    "уже 3",
    "закажу еще",
    "куплю еще",
    "беру еще",
    "отказалась",
    "не стала забирать",
    "себе беру",
    "себе и в подарок",
]

COMPARISON_HINTS = [
    "как у ",
    "как том форд",
    "том форд",
    "good girl gone bad",
    "килиан",
    "бархатные ручки",
    "я самая",
    "как дорогой",
    "как шелк",
    "похож",
    "напомнил",
    "вместо крема",
    "не то что",
]


@dataclass
class ProductContext:
    product_key: str
    product_name: str
    source_name: str
    current_year: int
    current_month: int


def clean_text(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = text.replace("Первоначальный отзыв", "")
    text = text.replace("Ещё", "")
    text = text.replace("…", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -–—\u00a0")


def normalize_match(text: str) -> str:
    return text.lower().replace("ё", "е")


def slugify(text: str) -> str:
    text = text.lower().replace("ё", "е")
    text = re.sub(r"[^a-zа-я0-9]+", "-", text)
    return text.strip("-")


def title_from_stem(stem: str) -> str:
    words = [word for word in re.split(r"[\s_-]+", stem.strip()) if word]
    if not words:
        return stem
    return " ".join(word.upper() if len(word) <= 3 else word.capitalize() for word in words)


def infer_context(source_path: Path, source_name: str, current_year: int, current_month: int) -> ProductContext:
    stem = source_path.stem
    return ProductContext(
        product_key=slugify(stem),
        product_name=title_from_stem(stem),
        source_name=source_name,
        current_year=current_year,
        current_month=current_month,
    )


def parse_date(raw: str, context: ProductContext) -> str:
    match = DATE_RE.match(raw)
    if not match:
        return raw
    day = int(match.group("day"))
    month = MONTHS[match.group("month")]
    year = match.group("year")
    inferred_year = int(year) if year else (context.current_year if month <= context.current_month else context.current_year - 1)
    return f"{inferred_year:04d}-{month:02d}-{day:02d} {match.group('hour')}:{match.group('minute')}"


def split_marker_line(line: str) -> list[tuple[str, str]]:
    matches = list(MARKER_RE.finditer(line))
    if not matches:
        return [("plain", clean_text(line))]

    parts: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(line)
        value = clean_text(line[start:end])
        if not value:
            continue
        label = {"Достоинства": "merit", "Недостатки": "flaw", "Комментарий": "comment"}[match.group(1)]
        parts.append((label, value))
    return parts


def split_fragments(text: str) -> list[str]:
    text = clean_text(text)
    if not text:
        return []

    text = text.replace(" / ", ", ")
    for separator in (";", "\n"):
        text = text.replace(separator, ". ")
    text = re.sub(r"\s+[—–-]\s+", ". ", text)

    parts: list[str] = []
    for piece in re.split(r"[.!?]+", text):
        piece = piece.strip(" ,")
        if not piece:
            continue

        subparts = [piece]
        for pattern in (
            r", но ",
            r" но ",
            r", а ",
            r" а ",
            r", тк ",
            r" тк ",
            r", хотя ",
            r" хотя ",
            r", зато ",
            r" зато ",
        ):
            next_parts: list[str] = []
            for subpart in subparts:
                next_parts.extend([item.strip(" ,") for item in re.split(pattern, subpart) if item.strip(" ,")])
            subparts = next_parts

        for subpart in subparts:
            if subpart.count(",") >= 1:
                parts.extend([item.strip(" ,") for item in subpart.split(",") if item.strip(" ,")])
            else:
                parts.append(subpart)

    seen: set[str] = set()
    unique: list[str] = []
    for part in parts:
        normalized = clean_text(part)
        lowered = normalized.lower()
        if len(normalized) < 2 or lowered in seen:
            continue
        seen.add(lowered)
        unique.append(normalized)
    return unique


def code_for_fragment(fragment: str, category: str) -> str:
    lowered = normalize_match(fragment)
    checks = [
        ("smell", "smell"),
        ("аромат", "smell"),
        ("пах", "smell"),
        ("отдуш", "smell"),
        ("увлаж", "moisture"),
        ("питан", "nutrition"),
        ("впиты", "absorption"),
        ("липк", "absorption"),
        ("пленк", "absorption"),
        ("текстур", "texture"),
        ("жидк", "texture"),
        ("масл", "texture"),
        ("геле", "texture"),
        ("упаков", "packaging"),
        ("тюбик", "packaging"),
        ("короб", "packaging"),
        ("крышк", "packaging"),
        ("оберт", "packaging"),
        ("пергамент", "packaging"),
        ("бумаг", "packaging"),
        ("эстет", "aesthetic"),
        ("дизайн", "aesthetic"),
        ("визуал", "aesthetic"),
        ("стильн", "aesthetic"),
        ("красив", "aesthetic"),
        ("фото", "aesthetic"),
        ("бархат", "effect"),
        ("мягк", "effect"),
        ("нежн", "effect"),
        ("шелков", "effect"),
        ("эффект", "effect"),
        ("гладк", "effect"),
        ("сух", "effect"),
        ("трещ", "effect"),
        ("стянут", "effect"),
        ("подар", "scenario"),
        ("подруж", "scenario"),
        ("жене", "scenario"),
        ("дочке", "scenario"),
        ("сест", "scenario"),
        ("маме", "scenario"),
        ("сумк", "scenario"),
        ("раз беру", "scenario"),
        ("закаж", "scenario"),
        ("куплю", "scenario"),
        ("цен", "value"),
        ("объем", "volume"),
        ("объём", "volume"),
        ("75", "volume"),
        ("соль вместо", "mismatch"),
        ("жж", "safety"),
        ("аллерг", "safety"),
        ("как ", "comparison"),
        ("напомнил", "comparison"),
        ("похож", "comparison"),
        ("вместо", "mismatch"),
    ]

    theme = "misc"
    for needle, candidate in checks:
        if needle in lowered:
            theme = candidate
            break

    suffix = {
        "позитив": "plus",
        "негатив": "minus",
        "ожидание": "expect",
        "сомнение": "doubt",
        "сравнение": "compare",
        "сценарий": "scenario",
    }.get(category, "misc")
    return f"{theme}.{suffix}"


def is_generic_praise(lowered: str) -> bool:
    return lowered in GENERIC_TRASH or re.fullmatch(
        r"(супер+|класс+|огонь+|вау+|идеальный|советую|очень понравился|любимый крем)( !+)?",
        lowered,
    ) is not None


def classify_fragment(fragment: str, label: str = "plain") -> tuple[str, str | None, str | None, list[str] | str | None] | None:
    fragment = fragment.strip()
    lowered = normalize_match(fragment)
    flags: list[str] = []

    if not lowered or lowered in {"нет", "нету", "-", "их нет", "не нашла", "не обнаружила", "нет комментария", "минусов не нашла"}:
        return None
    if is_generic_praise(lowered):
        return ("trash", None, None, None)
    if lowered.strip(" !👍🔥✨🤍💔😍🥰☺️🐣🌸") in TRASH_PHRASES:
        return ("trash", None, None, None)

    has_doubt = any(hint in lowered for hint in DOUBT_HINTS) or "?" in fragment
    has_expect = any(hint in lowered for hint in EXPECT_HINTS)
    has_comparison = any(hint in lowered for hint in COMPARISON_HINTS)
    has_scenario = any(hint in lowered for hint in SCENARIO_HINTS)
    has_negative = any(hint in lowered for hint in NEGATIVE_HINTS) or label == "flaw"
    has_positive = any(hint in lowered for hint in POSITIVE_HINTS) or label == "merit"
    has_anchor = any(marker in lowered for marker in ANCHOR_MARKERS) or any(noun in lowered for noun in KNOWN_NOUNS)

    if has_comparison:
        return ("сравнение", code_for_fragment(fragment, "сравнение"), fragment, flags)
    if has_doubt and not (has_positive or has_negative):
        return ("сомнение", code_for_fragment(fragment, "сомнение"), fragment, flags)
    if has_expect and any(token in lowered for token in ("для визуала", "для дизайна", "для эстетики", "из-за")) and not has_negative:
        return ("ожидание", code_for_fragment(fragment, "ожидание"), fragment, flags)
    if has_scenario and not has_negative:
        return ("сценарий", code_for_fragment(fragment, "сценарий"), fragment, flags)
    if has_expect and not (has_positive or has_negative):
        return ("ожидание", code_for_fragment(fragment, "ожидание"), fragment, flags)
    if has_expect and (has_positive or has_negative):
        flags.append("has_expectation")
    if has_doubt and (has_positive or has_negative):
        flags.append("has_doubt")
    if has_negative:
        return ("негатив", code_for_fragment(fragment, "негатив"), fragment, flags)
    if has_positive:
        if label == "plain" and not has_anchor:
            word_count = len(re.findall(r"[a-zа-я0-9]+", lowered))
            if word_count <= 3:
                return ("trash", None, None, None)
        return ("позитив", code_for_fragment(fragment, "позитив"), fragment, flags)
    if label == "flaw" and any(noun in lowered for noun in KNOWN_NOUNS):
        return ("негатив", code_for_fragment(fragment, "негатив"), fragment, flags)
    if label == "merit" and any(noun in lowered for noun in KNOWN_NOUNS):
        return ("позитив", code_for_fragment(fragment, "позитив"), fragment, flags)
    if lowered in {"упаковка целая", "упаковка", "объем", "объём"}:
        return ("trash", None, None, None)
    if re.search(r"\b(запах|аромат|упаковка|текстура|дизайн|вид|эффект|крем)\b", lowered):
        return ("manual", None, None, "сигнал есть, категория неочевидна")
    return ("trash", None, None, None)


def build_package(source_path: Path, context: ProductContext) -> dict:
    text = source_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.startswith("- ![Аватар пользователя]")]

    units_registry: list[dict] = []
    signals_registry: list[dict] = []
    manual_queue: list[dict] = []
    trash: list[dict] = []

    for unit_number, start in enumerate(starts, 1):
        end = starts[unit_number] if unit_number < len(starts) else len(lines)
        block = lines[start:end]
        cleaned_lines = [line.strip() for line in block[1:] if line.strip()]

        name = cleaned_lines[0] if cleaned_lines else "Неизвестно"
        order_status = next(
            (line[2:] for line in cleaned_lines if line.startswith("- ") and any(token in line for token in ("Выкупили", "Отказались"))),
            "unknown",
        )
        volume = next((line[2:] for line in cleaned_lines if line.startswith("- ") and "мл" in line), "")
        date_raw = next((line for line in cleaned_lines if DATE_RE.match(line)), "")
        date_iso = parse_date(date_raw, context) if date_raw else ""

        content: list[str] = []
        in_reply = False
        for line in cleaned_lines:
            if line == name or line == date_raw or (line.startswith("- ") and line[2:] in {order_status, volume}):
                continue
            if line == "Ответ продавца":
                in_reply = True
                continue
            if in_reply:
                continue
            if line.startswith("- ![") or re.match(r"^!?\[[^\]]*\]\([^)]*\)$", line):
                continue
            content.append(line)

        full_quote = clean_text(" ".join(content))
        units_registry.append(
            {
                "product_key": context.product_key,
                "unit_index": f"#{unit_number}",
                "name": name,
                "date": date_iso or date_raw or "n/a",
                "order_status": order_status,
                "volume": volume or "n/a",
                "source": context.source_name,
                "full_quote": full_quote,
            }
        )

        unit_signals: list[tuple[str, str, str, list[str]]] = []
        manual_reason: str | None = None
        field_items: list[tuple[str, str]] = []
        had_structured_blocks = False

        index = 0
        while index < len(content):
            line = content[index]
            if line == "Плюсы товара":
                had_structured_blocks = True
                index += 1
                while index < len(content) and content[index].startswith("- "):
                    item = clean_text(content[index][2:])
                    if item:
                        unit_signals.append(("позитив", LIST_CODE_MAP.get(item.lower(), code_for_fragment(item, "позитив")), item, []))
                    index += 1
                continue
            if line == "Минусы товара":
                had_structured_blocks = True
                index += 1
                while index < len(content) and content[index].startswith("- "):
                    item = clean_text(content[index][2:])
                    if item:
                        if item.lower() == "другое":
                            if not manual_reason:
                                manual_reason = "указано минусом без конкретики"
                        else:
                            unit_signals.append(("негатив", LIST_CODE_MAP.get(item.lower(), code_for_fragment(item, "негатив")), item, []))
                    index += 1
                continue

            parsed = split_marker_line(line)
            if parsed and parsed[0][0] != "plain":
                had_structured_blocks = True
            field_items.extend(parsed)
            index += 1

        if not field_items and full_quote:
            field_items = [("plain", full_quote)]

        for label, text_part in field_items:
            if had_structured_blocks and label == "plain" and text_part.startswith(("Плюсы товара", "Минусы товара")):
                continue
            for fragment in split_fragments(text_part):
                result = classify_fragment(fragment, label)
                if not result:
                    continue
                category, signal_code, signal_fragment, extra = result
                if category == "trash":
                    continue
                if category == "manual":
                    if not manual_reason:
                        manual_reason = str(extra)
                    continue
                unit_signals.append((category, str(signal_code), str(signal_fragment), list(extra or [])))

        deduped: list[tuple[str, str, str, list[str]]] = []
        seen: set[tuple[str, str]] = set()
        for category, signal_code, signal_fragment, flags in unit_signals:
            key = (category, signal_fragment.lower())
            if key in seen:
                continue
            seen.add(key)
            deduped.append((category, signal_code, signal_fragment, flags))

        if deduped:
            for signal_number, (category, signal_code, signal_fragment, flags) in enumerate(deduped, 1):
                signals_registry.append(
                    {
                        "signal_id": f"{context.product_key}:#{unit_number}:s{signal_number}",
                        "product_key": context.product_key,
                        "unit_index": f"#{unit_number}",
                        "name": name,
                        "category": category,
                        "signal_code": signal_code,
                        "signal_fragment": signal_fragment,
                        "secondary_flags": flags,
                    }
                )
        else:
            if full_quote and not manual_reason:
                trash.append({"unit_index": f"#{unit_number}", "name": name, "full_quote": full_quote})
            elif manual_reason:
                manual_queue.append(
                    {"unit_index": f"#{unit_number}", "name": name, "full_quote": full_quote, "reason": manual_reason}
                )

        if deduped and manual_reason:
            manual_queue.append({"unit_index": f"#{unit_number}", "name": name, "full_quote": full_quote, "reason": manual_reason})

    stats = {
        "B_total": len(units_registry),
        "N_trash": len(trash),
        "B_clean": len(units_registry) - len(trash),
        "N_manual": len(manual_queue),
        "N_units_with_signals": len({signal["unit_index"] for signal in signals_registry}),
        "N_signals_total": len(signals_registry),
    }
    if stats["B_total"] != stats["N_trash"] + stats["B_clean"]:
        raise ValueError(f"Stats integrity check failed for {source_path}")

    return {
        "product_key": context.product_key,
        "product_name": context.product_name,
        "source": context.source_name,
        "source_file": str(source_path),
        "units_registry": units_registry,
        "signals_registry": signals_registry,
        "manual_queue": manual_queue,
        "trash": trash,
        "stats": stats,
        "category_counts": dict(Counter(signal["category"] for signal in signals_registry)),
    }


def render_markdown(package: dict) -> str:
    lines: list[str] = []
    lines.append("# FINAL REGISTRY PACKAGE")
    lines.append("")
    lines.append(f"- product_key: `{package['product_key']}`")
    lines.append(f"- product_name: `{package['product_name']}`")
    lines.append(f"- source: `{package['source']}`")
    lines.append(f"- source_file: [{Path(package['source_file']).name}]({package['source_file']})")
    lines.append("")
    lines.append("## STATS")
    for key, value in package["stats"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## UNITS_REGISTRY")
    for unit in package["units_registry"]:
        lines.append(f"### {package['product_key']}:{unit['unit_index']}")
        lines.append(f"- product_key: `{package['product_key']}`")
        lines.append(f"- unit_index: `{unit['unit_index']}`")
        lines.append(f"- name: {unit['name']}")
        lines.append(f"- date: `{unit['date']}`")
        lines.append(f"- order_status: `{unit['order_status']}`")
        lines.append(f"- volume: `{unit['volume']}`")
        lines.append(f"- full_quote: «{unit['full_quote']}»")
        lines.append("")
    lines.append("## SIGNALS_REGISTRY")
    for signal in package["signals_registry"]:
        lines.append(f"### {signal['signal_id']}")
        lines.append(f"- product_key: `{signal['product_key']}`")
        lines.append(f"- unit_index: `{signal['unit_index']}`")
        lines.append(f"- name: {signal['name']}")
        lines.append(f"- category: `{signal['category']}`")
        lines.append(f"- signal_code: `{signal['signal_code']}`")
        lines.append(f"- signal_fragment: «{signal['signal_fragment']}»")
        flags = ", ".join(signal["secondary_flags"]) if signal["secondary_flags"] else "none"
        lines.append(f"- secondary_flags: `{flags}`")
        lines.append("")
    lines.append("## MANUAL_QUEUE")
    if package["manual_queue"]:
        for item in package["manual_queue"]:
            lines.append(
                f"- {item['unit_index']} | {item['name']} | ручной разбор | «{item['full_quote']}» | причина: {item['reason']}"
            )
    else:
        lines.append("- empty")
    lines.append("")
    lines.append("## TRASH")
    if package["trash"]:
        for item in package["trash"]:
            lines.append(f"- {item['unit_index']} | {item['name']} | мусор | «{item['full_quote']}»")
    else:
        lines.append("- empty")
    lines.append("")
    lines.append("## CATEGORY COUNTS")
    for category, count in Counter(package["category_counts"]).most_common():
        lines.append(f"- {category}: {count}")
    lines.append("")
    return "\n".join(lines)


def resolve_inputs(paths: list[str]) -> list[Path]:
    inputs: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        if path.is_dir():
            inputs.extend(sorted(path.glob("*.md")))
        else:
            inputs.append(path)

    candidates = [path for path in inputs if path.exists() and path.suffix.lower() == ".md"]
    filtered: list[Path] = []
    for path in candidates:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "- ![Аватар пользователя]" in text:
            filtered.append(path)
    return filtered


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch signal-markup for Wildberries markdown exports.")
    parser.add_argument("inputs", nargs="+", help="One or more markdown files or directories.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Optional directory for output files.")
    parser.add_argument("--source-name", default="Wildberries", help="Marketplace/source label.")
    parser.add_argument("--current-year", type=int, default=2026, help="Year used for dates without explicit year.")
    parser.add_argument("--current-month", type=int, default=4, help="Current month number used for year inference.")
    args = parser.parse_args()

    input_paths = resolve_inputs(args.inputs)
    if not input_paths:
        raise SystemExit("No markdown inputs found.")

    output_dir = args.output_dir.expanduser() if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    summaries: list[dict] = []
    for input_path in input_paths:
        context = infer_context(input_path, args.source_name, args.current_year, args.current_month)
        package = build_package(input_path, context)

        target_dir = output_dir or input_path.parent
        json_path = target_dir / f"{input_path.stem}.signal-registry.json"
        md_path = target_dir / f"{input_path.stem}.signal-registry.md"

        json_path.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(render_markdown(package), encoding="utf-8")

        summaries.append(
            {
                "file": input_path.name,
                "product_key": package["product_key"],
                "B_total": package["stats"]["B_total"],
                "N_trash": package["stats"]["N_trash"],
                "N_manual": package["stats"]["N_manual"],
                "N_signals_total": package["stats"]["N_signals_total"],
                "md_path": str(md_path),
            }
        )

    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
