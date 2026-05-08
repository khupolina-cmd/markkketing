from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


SOURCE_PATH = Path("/Users/alittlepinkie/Documents/Obsidian Vault/off scrub.md")
OUTPUT_JSON = Path("/Users/alittlepinkie/Documents/New project/off_scrub_registry_package.json")
OUTPUT_MD = Path("/Users/alittlepinkie/Documents/New project/off_scrub_registry_package.md")

PRODUCT_KEY = "offscrub-hand-cream"
PRODUCT_NAME = "OFF SCRUB hand cream"
SOURCE_NAME = "Wildberries"
CURRENT_YEAR = 2026


MONTHS = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


LABEL_RE = re.compile(r"(Достоинства:|Недостатки:|Комментарий:)")
DATE_RE = re.compile(
    r"(?P<day>\d{2}) (?P<month>[а-я]+)(?: (?P<year>\d{4}))?, (?P<hour>\d{2}):(?P<minute>\d{2})"
)


GENERIC_POSITIVE_RE = re.compile(
    r"^(очень понравил[а-я]+|все нравится.*|вне конкуренции.*|классн(ый|ая)?!?|классный !!!|"
    r"любимый крем|мне понравился крем|отличный крем( для рук)?!?|"
    r"супер(ский)? крем!?|идеальный за такую цену|очень классный крем!?|"
    r"всё замечательно\.? спасибо\.?|прекрасный крем!?|обалденный крем\.?|"
    r"одна из лучших покупок.*|рекомендую к покупке|товар выкуплен|"
    r".*хороший сам по себе.*|он прекрасен.*)$",
    re.IGNORECASE,
)

MANUAL_HINT_RE = re.compile(
    r"(не такой|не то|странн|ввело в заблуждение|чисто запах|обычный бюджетный|"
    r"ощущение|непонят|не знаю даже|как будто)",
    re.IGNORECASE,
)


@dataclass
class Unit:
    unit_index: str
    name: str
    date: str | None
    stars: int | None
    source: str
    full_quote: str
    sections: dict[str, list[str]] = field(default_factory=dict)


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("Первоначальный отзыв", "")
    text = re.sub(r"Ещё$", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip(" |")


def strip_labels(text: str) -> str:
    text = re.sub(r"\b(Достоинства|Недостатки|Комментарий):\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(Плюсы товара|Минусы товара):\s*", "", text, flags=re.IGNORECASE)
    return clean_text(text)


def parse_date(raw: str) -> str | None:
    raw = clean_text(raw.replace("· Дополнен", ""))
    match = DATE_RE.search(raw)
    if not match:
        return None
    year = match.group("year") or str(CURRENT_YEAR)
    month = MONTHS.get(match.group("month"))
    if not month:
        return None
    return f"{year}-{month}-{match.group('day')}"


def split_labeled_text(text: str) -> list[tuple[str, str]]:
    text = clean_text(text)
    if not text:
        return []
    matches = list(LABEL_RE.finditer(text))
    if not matches:
        return [("plain", text)]
    parts: list[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        label = match.group(1).rstrip(":")
        body = clean_text(text[start:end])
        if body:
            parts.append((label, body))
    return parts


def parse_blocks(text: str) -> list[str]:
    parts = re.split(r"(?m)^- !\[Аватар пользователя\]\(.*\)\s*$", text)
    return [part for part in parts[1:] if part.strip()]


def parse_unit(block: str, index: int) -> Unit:
    lines = [line.rstrip("\n") for line in block.splitlines()]
    name = ""
    date = None
    date_idx = None
    for i, raw in enumerate(lines):
        stripped = clean_text(raw.strip())
        if not stripped:
            continue
        if DATE_RE.search(stripped):
            date = parse_date(stripped)
            date_idx = i
            break
        if (
            not name
            and not stripped.startswith("-")
            and not stripped.startswith("![")
            and stripped not in {"Плюсы товара", "Минусы товара", "Ответ продавца"}
        ):
            name = stripped

    content_lines = lines[(date_idx + 1 if date_idx is not None else 0) :]
    sections = {
        "plain": [],
        "advantages": [],
        "disadvantages": [],
        "comment": [],
        "pros": [],
        "cons": [],
    }
    mode: str | None = None
    for raw in content_lines:
        stripped = clean_text(raw.strip())
        if not stripped:
            continue
        if stripped == "Ответ продавца":
            break
        if stripped.startswith("![") or stripped == "Выкупили":
            continue
        if stripped.lower().rstrip(".") == "товар выкуплен":
            continue
        if stripped.startswith("[]("):
            continue
        if stripped.startswith("- !["):
            continue
        if stripped == "Плюсы товара":
            mode = "pros"
            continue
        if stripped == "Минусы товара":
            mode = "cons"
            continue
        if stripped.startswith("- "):
            item = clean_text(stripped[2:])
            if item and not item.startswith("![") and mode in {"pros", "cons"}:
                sections[mode].append(item)
            continue
        mode = None
        for label, body in split_labeled_text(stripped):
            if label == "plain":
                sections["plain"].append(body)
            elif label == "Достоинства":
                sections["advantages"].append(body)
            elif label == "Недостатки":
                sections["disadvantages"].append(body)
            elif label == "Комментарий":
                sections["comment"].append(body)

    full_quote_parts: list[str] = []
    for key, title in (
        ("plain", None),
        ("advantages", "Достоинства"),
        ("disadvantages", "Недостатки"),
        ("comment", "Комментарий"),
    ):
        for value in sections[key]:
            full_quote_parts.append(f"{title}: {value}" if title else value)
    if sections["pros"]:
        full_quote_parts.append("Плюсы товара: " + "; ".join(sections["pros"]))
    if sections["cons"]:
        full_quote_parts.append("Минусы товара: " + "; ".join(sections["cons"]))

    return Unit(
        unit_index=f"#{index}",
        name=name or "Покупатель",
        date=date,
        stars=None,
        source=SOURCE_NAME,
        full_quote=" | ".join(full_quote_parts),
        sections=sections,
    )


def default_signal_code(fragment: str, category: str) -> str:
    low = fragment.lower()
    if any(token in low for token in ("пах", "аромат", "отдуш")):
        return "запах+" if category == "позитив" else "запах-"
    if any(token in low for token in ("увлаж", "пита", "мягк", "бархат", "сух", "шелуш", "трещ", "напиты")):
        return "увлажн.+" if category == "позитив" else "увлажн.-"
    if any(token in low for token in ("впиты", "липк", "жирн", "пленк", "текстур", "жидк", "консист", "финиш")):
        return "текстура+" if category == "позитив" else "текстура-"
    if any(token in low for token in ("упак", "тюбик", "короб", "бумаг", "крышк", "вскрыт", "мят", "штрих", "накле")):
        return "упаковка+" if category == "позитив" else "упаковка-"
    if any(token in low for token in ("эстет", "стиль", "дизайн", "визуал", "внешний вид", "цвет", "красив", "минимализм")):
        return "дизайн+"
    if any(token in low for token in ("качеств", "крошк", "соль вместо", "брак", "не такой")):
        return "качество+" if category == "позитив" else "качество-"
    if any(token in low for token in ("эффект", "помог", "помогл", "вау", "убрал", "убирает")):
        return "эффект+" if category == "позитив" else "эффект-"
    if any(token in low for token in ("удоб", "надолго", "в сумк", "нужно не много")):
        return "удобство+"
    if any(token in low for token in ("цен", "стоим")):
        return "цена+"
    if any(token in low for token in ("объем", "обьем", "75 мл")):
        return "объем+"
    if category == "ожидание":
        return "ожидание.критерий"
    if category == "сомнение":
        return "сомнение.риск"
    if category == "сценарий":
        return "сценарий.контекст"
    if category == "сравнение":
        return "сравнение.x"
    words = re.findall(r"[а-яa-z0-9]+", low)
    root = ".".join(words[:2]) if words else "сигнал"
    return root


def fragment_is_generic_positive(fragment: str) -> bool:
    text = strip_labels(fragment).lower()
    return bool(GENERIC_POSITIVE_RE.match(text)) and not any(
        token in text
        for token in (
            "пах",
            "аромат",
            "увлаж",
            "впиты",
            "текстур",
            "упак",
            "эстет",
            "дизайн",
            "бархат",
            "мягк",
        )
    )


def split_fragments(text: str) -> list[str]:
    text = clean_text(text)
    if not text:
        return []
    text = re.sub(r"\s*[-–—]\s*", ". ", text)
    text = re.sub(r"\s+но\s+", ". ", text, flags=re.IGNORECASE)
    pieces = re.split(r"[.!?;]+", text)
    fragments: list[str] = []
    for piece in pieces:
        piece = clean_text(piece)
        if not piece:
            continue
        subparts = [clean_text(part) for part in re.split(r",\s*", piece) if clean_text(part)]
        for subpart in subparts:
            if " и " in subpart.lower():
                left_right = [clean_text(part) for part in re.split(r"\s+и\s+", subpart) if clean_text(part)]
                facet_hits = sum(
                    1
                    for part in left_right
                    if any(
                        token in part.lower()
                        for token in (
                            "пах",
                            "аромат",
                            "увлаж",
                            "впиты",
                            "липк",
                            "жирн",
                            "упак",
                            "дизайн",
                            "эстет",
                            "мягк",
                            "бархат",
                            "эффект",
                        )
                    )
                )
                if len(left_right) > 1 and facet_hits > 1:
                    fragments.extend(left_right)
                    continue
            fragments.append(subpart)
    return fragments


def classify_fragment(fragment: str, default_category: str | None = None) -> tuple[str, str, list[str]] | None:
    fragment = clean_text(fragment)
    low = fragment.lower()
    if not fragment:
        return None
    if fragment_is_generic_positive(fragment):
        return None

    flags: list[str] = []
    if re.search(r"(подойд[её]т ли|не будет ли|не окажется ли|боюсь|опасаюсь|сомневаюсь|не уверена|как понять|надеюсь,? что не)", low):
        return ("сомнение", default_signal_code(fragment, "сомнение"), flags)

    if re.search(r"(лучше, чем|хуже, чем|по сравнению с|вместо [а-яa-z]|не то, что|как японск|как .* кремы)", low):
        return ("сравнение", default_signal_code(fragment, "сравнение"), flags)

    if re.search(
        r"(на подарок|в подарок|подружк|сестрам|подругам|дочке|маме|"
        r"для себя|и себе|себе беру|куплю себе|в сумке|третий раз беру|уже .* раз|закажу еще|беру этот крем|"
        r"купила на подарок|заказала .* подружк|купила .* себе)",
        low,
    ):
        return ("сценарий", default_signal_code(fragment, "сценарий"), flags)

    if re.search(r"(взял[аи]? .*как|брал[аи]? .*как|для дизайна|для эстетики|из-за .*дизайн|из-за .*эстет)", low):
        return ("ожидание", default_signal_code(fragment, "ожидание"), flags)

    has_expectation = bool(
        re.search(r"(ожидал|ожидала|ожидания|думал|думала|рассчитывал|не ожидал|не ожидала|по описанию|заявлено|важно было|брала из-за|брала для|покупала для|хотела|хотел)", low)
    )
    negative_hint = bool(
        re.search(
            r"(не увлаж|не пит|увлажняет плохо|слабовато|нет эффекта|ужас|резк|навязчив|противн|душн|не пахнет|плохо пахнет|мят|вскрыт|грязн|жж[её]т|аллерг|сухов|жидк|крошк|соль вместо|испорчен)",
            low,
        )
    )
    positive_hint = bool(
        re.search(
            r"(прият|вкусн|нежн|шикарн|дорогой аромат|быстро впиты|не липк|не жирн|увлажняет|мягк|бархат|стильн|эстет|красив|хорошо упак|бережно|цена сказка|соотношение цены|большой объем|удобно)",
            low,
        )
    )
    negative_hint = negative_hint or bool(re.search(r"(слишком сладк|парфюмирован|едкий|лекарств|бабушкин)", low))
    positive_hint = positive_hint or bool(re.search(r"(запакован|обертк|фирменн.*бумаг|дошел в нормальном состоянии)", low))

    if has_expectation and (negative_hint or positive_hint):
        flags.append("has_expectation")
        category = "негатив" if negative_hint else "позитив"
        return (category, default_signal_code(fragment, category), flags)
    if has_expectation:
        return ("ожидание", default_signal_code(fragment, "ожидание"), flags)

    if negative_hint:
        return ("негатив", default_signal_code(fragment, "негатив"), flags)
    if positive_hint:
        return ("позитив", default_signal_code(fragment, "позитив"), flags)

    aspect_token = bool(
        re.search(
            r"(пах|аромат|отдуш|увлаж|пита|мягк|бархат|сух|шелуш|трещ|напиты|"
            r"впиты|липк|жирн|пленк|текстур|жидк|консист|финиш|"
            r"упак|тюбик|короб|бумаг|крышк|вскрыт|мят|штрих|накле|"
            r"эстет|стиль|дизайн|визуал|внешний вид|цвет|красив|"
            r"качеств|крошк|брак|эффект|помог|удоб|объем|обьем|цен|стоим)",
            low,
        )
    )
    if default_category in {"позитив", "негатив"} and aspect_token:
        return (default_category, default_signal_code(fragment, default_category), flags)

    return None


def dedupe_signals(signals: list[dict]) -> list[dict]:
    seen: set[tuple[str, str, str]] = set()
    unique: list[dict] = []
    for signal in signals:
        key = (signal["unit_index"], signal["category"], signal["signal_code"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(signal)
    return unique


def build_signals(unit: Unit) -> tuple[list[dict], list[str], bool]:
    signals: list[dict] = []
    manual_reasons: list[str] = []
    had_nontrash_text = False

    def add_signal(category: str, fragment: str, code: str, flags: list[str] | None = None) -> None:
        fragment = clean_text(fragment)
        if not fragment:
            return
        signals.append(
            {
                "signal_id": f"{PRODUCT_KEY}:{unit.unit_index}:s{len(signals) + 1}",
                "product_key": PRODUCT_KEY,
                "unit_index": unit.unit_index,
                "name": unit.name,
                "category": category,
                "signal_code": code,
                "signal_fragment": f"«{fragment}»",
                "secondary_flags": flags or [],
            }
        )

    for item in unit.sections["pros"]:
        had_nontrash_text = True
        add_signal("позитив", item, default_signal_code(item, "позитив"))
    for item in unit.sections["cons"]:
        had_nontrash_text = True
        add_signal("негатив", item, default_signal_code(item, "негатив"))

    for key, default_category in (
        ("advantages", "позитив"),
        ("disadvantages", "негатив"),
        ("comment", None),
        ("plain", None),
    ):
        for text in unit.sections[key]:
            if clean_text(text):
                had_nontrash_text = True
            fragments = split_fragments(text)
            matched_here = 0
            for fragment in fragments:
                result = classify_fragment(fragment, default_category=default_category)
                if result is None:
                    continue
                category, code, flags = result
                add_signal(category, fragment, code, flags)
                matched_here += 1
            if matched_here == 0 and clean_text(text):
                if MANUAL_HINT_RE.search(text.lower()):
                    manual_reasons.append(f"«{clean_text(text)}» | причина: неоднозначная формулировка")
                elif strip_labels(text).lower() != "товар выкуплен" and not fragment_is_generic_positive(text) and len(clean_text(text)) > 12:
                    manual_reasons.append(f"«{clean_text(text)}» | причина: сигнал есть, категория неочевидна")

    return dedupe_signals(signals), manual_reasons, had_nontrash_text


def render_markdown(package: dict) -> str:
    lines: list[str] = []
    lines.append(f"product_key: {package['product_key']}")
    lines.append("")
    lines.append("## units_registry")
    lines.append("")
    for unit in package["units_registry"]:
        lines.append(f"product_key: {unit['product_key']}")
        lines.append(f"unit_index: {unit['unit_index']}")
        lines.append(f"name: {unit['name']}")
        lines.append(f"date: {unit['date']}")
        lines.append(f"stars: {unit['stars']}")
        lines.append(f"source: {unit['source']}")
        lines.append(f"full_quote: {unit['full_quote']}")
        lines.append("")
    lines.append("## signals_registry")
    lines.append("")
    for signal in package["signals_registry"]:
        lines.append(f"signal_id: {signal['signal_id']}")
        lines.append(f"product_key: {signal['product_key']}")
        lines.append(f"unit_index: {signal['unit_index']}")
        lines.append(f"name: {signal['name']}")
        lines.append(f"category: {signal['category']}")
        lines.append(f"signal_code: {signal['signal_code']}")
        lines.append(f"signal_fragment: {signal['signal_fragment']}")
        lines.append(f"secondary_flags: {signal['secondary_flags']}")
        lines.append("")
    lines.append("## manual_queue")
    lines.append("")
    for item in package["manual_queue"]:
        lines.append(item)
    lines.append("")
    lines.append("## trash")
    lines.append("")
    for item in package["trash"]:
        lines.append(item)
    lines.append("")
    lines.append("## stats")
    lines.append("")
    for key, value in package["stats"].items():
        lines.append(f"{key}: {value}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    raw = SOURCE_PATH.read_text(encoding="utf-8")
    blocks = parse_blocks(raw)
    units_registry: list[dict] = []
    signals_registry: list[dict] = []
    manual_queue: list[str] = []
    trash: list[str] = []

    for idx, block in enumerate(blocks, start=1):
        unit = parse_unit(block, idx)
        units_registry.append(
            {
                "product_key": PRODUCT_KEY,
                "product_name": PRODUCT_NAME,
                "unit_index": unit.unit_index,
                "name": unit.name,
                "date": unit.date,
                "stars": unit.stars,
                "source": unit.source,
                "full_quote": f"«{unit.full_quote}»" if unit.full_quote else "«»",
            }
        )

        signals, manual_items, had_nontrash_text = build_signals(unit)
        if signals:
            signals_registry.extend(signals)
        elif not had_nontrash_text or fragment_is_generic_positive(strip_labels(unit.full_quote.replace("«", "").replace("»", ""))):
            trash.append(f"{unit.unit_index} | {unit.name} | мусор | «{unit.full_quote}»")
        elif unit.full_quote:
            if manual_items:
                for item in manual_items:
                    manual_queue.append(f"{unit.unit_index} | {unit.name} | ручной разбор | {item}")
            else:
                manual_queue.append(
                    f"{unit.unit_index} | {unit.name} | ручной разбор | «{unit.full_quote}» | причина: сигнал есть, категория неочевидна"
                )

        if signals and manual_items:
            for item in manual_items:
                manual_queue.append(f"{unit.unit_index} | {unit.name} | ручной разбор | {item}")

    stats = {
        "B_total": len(units_registry),
        "N_trash": len(trash),
        "B_clean": len(units_registry) - len(trash),
        "N_manual": len(manual_queue),
        "N_units_with_signals": len({signal["unit_index"] for signal in signals_registry}),
        "N_signals_total": len(signals_registry),
    }

    package = {
        "product_key": PRODUCT_KEY,
        "product_name": PRODUCT_NAME,
        "source": SOURCE_NAME,
        "units_registry": units_registry,
        "signals_registry": signals_registry,
        "manual_queue": manual_queue,
        "trash": trash,
        "stats": stats,
    }

    OUTPUT_JSON.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(package), encoding="utf-8")

    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
