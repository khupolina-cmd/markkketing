#!/usr/bin/env python3
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


INPUT_PATH = Path("/Users/alittlepinkie/Documents/Obsidian Vault/off scrub.md")
OUTPUT_PATH = Path("/Users/alittlepinkie/Documents/New project/off_scrub_signal_registry.json")
PRODUCT_KEY = "offscrub-hand-cream"
SOURCE = "Wildberries"

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

GENERIC_TRASH = {
    "очень понравился",
    "любимый крем",
    "классный",
    "классный !!!",
    "классный крем",
    "отличный крем",
    "отличный крем для рук",
    "отличный крем для рук!",
    "это космос",
    "советую",
    "мне понравился крем",
    "крем понравился",
    "все нравится в нем",
    "все",
    "все супер",
    "просто лучший крем который у меня был",
    "рекомендую 100%",
}

PLUS_MAP = {
    "хорошо пахнет": "аромат.приятный",
    "приятный запах": "аромат.приятный",
    "запах": "аромат.приятный",
    "текстура": "текстура.приятная",
    "качество": "качество.хорошее",
    "хороший эффект": "эффект.положительный",
    "эффект от средства": "эффект.положительный",
    "удобно пользоваться": "использование.удобно",
    "легко использовать": "использование.удобно",
    "цвет": "визуал.эстетика",
    "хорошая цена": "цена.выгодная",
    "отличное качество": "качество.хорошее",
    "состав": "состав.плюс",
}

MINUS_MAP = {
    "плохо пахнет": "аромат.неприятный",
    "нет эффекта": "эффект.нет",
    "плохое качество": "качество.плохое",
    "другое": "прочее.негатив",
}

POSITIVE_PATTERNS = [
    (r"аромат невероятн|аромат просто шикарн|аромат шикарн|аромат приятн|аромат интересн|очень приятный аромат|приятный аромат|вкусно пахнет|пахнет очень вкусно|пахнет приятно|аромат потрясающий|запах шикарный|запах просто бомба|запах приятн|запах очень вкусно|запах очень приятно|запах мне понравился|аромат и текстура очень приятные", "аромат.приятный"),
    (r"не липк", "финиш.без_липкости"),
    (r"не жирн", "финиш.без_жирности"),
    (r"быстро впитыва", "впитывание.быстрое"),
    (r"моментально", "впитывание.быстрое"),
    (r"легко распредел", "нанесение.легкое"),
    (r"нераздражающ\w* запах|едва уловим\w*|ненавязчив\w*|нейтральн\w* запах", "аромат.мягкий"),
    (r"хорошо увлажня|увлажняет\\.?$|супер увлажнение|очень хорошо увлажняет|ручки становятся мягкими|кожа .* мягк|стянутость .* убирает|смягчает кожу", "увлажнение.хорошее"),
    (r"руки после него нежные|руки после становятся нежными|нежные бархатистые", "эффект.смягчение"),
    (r"бархатн\w* финиш|ощущени\w* бархата", "финиш.бархатный"),
    (r"легк\w* текстур|мягк\w* текстур|приятн\w* текстур|текстура .*кремов", "текстура.приятная"),
    (r"кремовая", "текстура.кремовая"),
    (r"эстетичн\w*|красив\w* упаковк|стильн\w* тюбик|визуальн\w* вид|дизайн", "визуал.эстетика"),
    (r"хорошо упак|достойно упак|красиво упак|упаковка целая|ничего не повреждено|хорошо запакованной коробке|дополнительной оберткой|коробочка\\+|в тишью|в пергамент", "упаковка.хорошая"),
    (r"мягк\w* руки|шелушинк\w* ушли", "эффект.смягчение"),
    (r"большой объем|неплохой объем", "объем.достаточный"),
    (r"цена .*сказка|цена отличная|за такую цену", "цена.выгодная"),
    (r"очень довольн|очень нравится|сам крем тоже хороший|неплохой крем|хороший крем|нормально|окей", "эффект.общая_удовлетворенность"),
    (r"экономия расхода", "расход.экономичный"),
    (r"аромат супер|оказался очень классный|понравился и запах и текстура|пользуюсь с удовольствием", "эффект.общая_удовлетворенность"),
]

NEGATIVE_PATTERNS = [
    (r"увлажняет плохо|слабовато увлажняет|среднее увлажнение|не сильно увлажняет|не спасет|5/10", "увлажнение.слабое"),
    (r"нет эффекта|никакого эффекта", "эффект.нет"),
    (r"плохо пахнет|запах ужасн|запах .*неприятн|пахнет .*лекарств|запах на любителя|ничего особенного|слишком сладк|очень приторн\w* запах|запах духов|запах не давал спать|душн\w*|противн\w*|едк\w*|бабушкин\w*|очень ароматизирован", "аромат.неприятный"),
    (r"не пахнет|без какого-либо запаха|запах менее чувствуется|еле уловимый", "аромат.слабый"),
    (r"мят\w*|помят\w*|распечатанн\w*|не упакован|не дали|не нашли|следы .*крови|следы .*джема|весь грязн", "упаковка.дефект"),
    (r"жж[её]т руки|аллерги|сыпь", "реакция.негативная"),
    (r"жидк\w*", "текстура.жидкая"),
    (r"не совсем кремовая", "текстура.не_кремовая"),
    (r"плохо впитыва|не сразу впитывается|оставляет пл[её]нк", "финиш.тяжелый"),
    (r"неудобн\w* упаковк|вытекать|весь грязный", "упаковка.неудобная"),
    (r"покрытие .*треск|краска .*оставаться на руках", "упаковка.износ"),
    (r"черные крошки", "качество.инородные_частицы"),
    (r"не подойдет|не хватает жирности|питания не хватило", "увлажнение.недостаточное"),
    (r"не такой", "сравнение.не_как_раньше"),
]

SCENARIO_PATTERNS = [
    (r"купила на подарок|заказала .* на подарок|для подарка|подарила(?: .*?)? на новый год|взяла еще сестре|заказала подружкам", "сценарий.подарок"),
    (r"себе беру|заказала себе|маме отдала|увидела у мамы", "сценарий.для_себя_или_семьи"),
    (r"для визуала|для дизайна и эстетики|как эстетичный крем", "сценарий.для_эстетики"),
    (r"в сумке", "сценарий.в_сумку"),
    (r"на работу", "сценарий.на_работу"),
    (r"третий раз беру|2-ой раз|это мой третий тюбик|буду заказывать еще|перезакажу|заказывать еще|буду пользоваться иногда", "сценарий.повторная_покупка"),
    (r"молодому человеку понравился|дочке|подружкам|сестр", "сценарий.для_другого"),
    (r"попробовала сама", "сценарий.для_себя_или_семьи"),
]

EXPECTATION_PATTERNS = [
    (r"не ожидала", "ожидание.ниже_планки"),
    (r"ожидала другой запах|хотелось пожирнее|большего ожидать", "ожидание.сенсорика_или_эффект"),
    (r"по описанию|на карточку товара|создается ощущение", "ожидание.по_карточке"),
    (r"не рассчитывая на хорошее увлажнение", "ожидание.скепсис"),
    (r"очень большие ожидания были", "ожидание.завышенное"),
    (r"ничего особенно не ждала", "ожидание.низкие_ожидания"),
]

COMPARISON_PATTERNS = [
    (r"оригинал", "сравнение.с_оригиналом"),
    (r"как на картинке", "сравнение.с_карточкой"),
    (r"из дорогого ухода|пахнет париж|good girl gone bad|том форд|бархатные ручки|я самая", "сравнение.с_люксом_или_аналогом"),
]

MANUAL_PATTERNS = [
    (r"качество .*не понятно|не знаю .*аромате|может быть именно мне такой пришел", "постфактумная неопределенность"),
    (r"не пойдет", "нужен контекст цели"),
    (r"рекомендую\?$", "сарказм или рекомендация"),
]


@dataclass
class Unit:
    unit_index: str
    name: str
    date: str
    stars: None
    source: str
    full_quote: str


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip(" |")


def slug(text: str) -> str:
    text = text.lower()
    text = text.replace("ё", "е")
    text = re.sub(r"[^a-zа-я0-9]+", ".", text)
    return text.strip(".")[:48] or "signal"


def parse_date(line: str) -> str:
    cleaned = line.replace("\xa0", " ").replace("· Дополнен", "").strip()
    month_pattern = "|".join(MONTHS)
    match = re.search(rf"(\d{{1,2}}) ({month_pattern})(?: (\d{{4}}))?", cleaned)
    if not match:
        return cleaned
    day, month, year = match.groups()
    year = year or "2026"
    return f"{year}-{MONTHS[month]}-{int(day):02d}"


def split_inline_sections(text: str) -> List[tuple[str, str]]:
    matches = list(re.finditer(r"(Достоинства:|Недостатки:|Комментарий:)", text))
    if not matches:
        return [("text", normalize_whitespace(text))] if normalize_whitespace(text) else []
    parts = []
    for i, match in enumerate(matches):
        label = match.group(1).rstrip(":")
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = normalize_whitespace(text[start:end])
        if content:
            parts.append((label, content))
    return parts


def parse_block(block: str, index: int) -> dict:
    raw_lines = [line.rstrip() for line in block.splitlines()]
    lines = [line.strip() for line in raw_lines if line.strip()]
    lines = [line for line in lines if not line.startswith("![") and not line.startswith("[](")]
    if "Ответ продавца" in lines:
        lines = lines[: lines.index("Ответ продавца")]
    if not lines:
        return {}

    name = ""
    date = ""
    parts: List[tuple[str, str]] = []
    plus_items: List[str] = []
    minus_items: List[str] = []
    mode = None

    for line in lines:
        if line.startswith("(https://"):
            continue
        if not name and not line.startswith("- ") and not re.search(r"\d{1,2} [а-я]+", line):
            name = line
            continue
        month_pattern = "|".join(MONTHS)
        if re.search(rf"\d{{1,2}} ({month_pattern})(?: \d{{4}})?", line):
            date = parse_date(line)
            mode = None
            continue
        if line in {"Плюсы товара", "Минусы товара"}:
            mode = line
            continue
        if line.startswith("- "):
            value = normalize_whitespace(line[2:])
            if not value or value == "Выкупили" or value.endswith("мл") or value == "Отказались":
                continue
            if mode == "Плюсы товара":
                plus_items.append(value)
            elif mode == "Минусы товара":
                minus_items.append(value)
            continue

        mode = None
        if any(marker in line for marker in ("Достоинства:", "Недостатки:", "Комментарий:")):
            parts.extend(split_inline_sections(line))
        else:
            text = normalize_whitespace(line)
            if text and text not in {"Первоначальный отзыв"}:
                parts.append(("text", text))

    full_parts = []
    for label, content in parts:
        if content:
            full_parts.append(f"{label}: {content}" if label != "text" else content)
    if plus_items:
        full_parts.append("Плюсы товара: " + "; ".join(plus_items))
    if minus_items:
        full_parts.append("Минусы товара: " + "; ".join(minus_items))

    return {
        "unit": Unit(
            unit_index=f"#{index}",
            name=name or "Покупатель",
            date=date or "",
            stars=None,
            source=SOURCE,
            full_quote=" | ".join(full_parts),
        ),
        "parts": parts,
        "plus_items": plus_items,
        "minus_items": minus_items,
    }


def sentence_chunks(text: str) -> List[str]:
    text = normalize_whitespace(text)
    text = re.sub(r"([.!?])([А-ЯA-Z])", r"\1 \2", text)
    chunks = []
    for piece in re.split(r"[.!?]+", text):
        piece = normalize_whitespace(piece)
        if not piece:
            continue
        subparts = re.split(r",\s*(?:но|а)\s+|;\s*", piece)
        for sub in subparts:
            sub = normalize_whitespace(sub)
            if sub:
                chunks.append(sub)
    return chunks


def map_list_item(item: str, negative: bool) -> str:
    item_norm = item.lower()
    if negative:
        return MINUS_MAP.get(item_norm, f"негатив.{slug(item_norm)}")
    return PLUS_MAP.get(item_norm, f"позитив.{slug(item_norm)}")


def classify_clause(clause: str, default_category: str | None) -> List[tuple[str, str, str, List[str]]]:
    results: List[tuple[str, str, str, List[str]]] = []
    lowered = clause.lower()

    for pattern, reason in MANUAL_PATTERNS:
        if re.search(pattern, lowered):
            results.append(("manual", reason, clause, []))
            return results

    for pattern, code in SCENARIO_PATTERNS:
        if re.search(pattern, lowered):
            results.append(("сценарий", code, clause, []))
            break

    for pattern, code in COMPARISON_PATTERNS:
        if re.search(pattern, lowered):
            results.append(("сравнение", code, clause, []))
            break

    expectation_hit = None
    for pattern, code in EXPECTATION_PATTERNS:
        if re.search(pattern, lowered):
            expectation_hit = code
            break

    if expectation_hit and not any(r[0] in {"сценарий", "сравнение"} for r in results):
        if re.search(r"но .*оказал|но .*достойн|увы|не пахнет|жидк|не понрав|не проходит|держится", lowered):
            results.append(("негатив", expectation_hit.replace("ожидание", "ожидание"), clause, ["has_expectation"]))
        elif re.search(r"оказал|пахнет очень вкусно|достойн", lowered):
            results.append(("позитив", expectation_hit.replace("ожидание", "ожидание"), clause, ["has_expectation"]))
        else:
            results.append(("ожидание", expectation_hit, clause, []))

    matched = False
    for pattern, code in NEGATIVE_PATTERNS:
        if re.search(pattern, lowered):
            flags = ["has_expectation"] if expectation_hit and not results else []
            results.append(("негатив", code, clause, flags))
            matched = True
            break

    for pattern, code in POSITIVE_PATTERNS:
        if re.search(pattern, lowered):
            flags = ["has_expectation"] if expectation_hit and not results else []
            results.append(("позитив", code, clause, flags))
            matched = True
            break

    if not results and default_category in {"позитив", "негатив"}:
        code = f"{default_category}.{slug(clause)}"
        results.append((default_category, code, clause, []))
        matched = True

    if not results and len(lowered) > 4:
        results.append(("manual", "категория неочевидна", clause, []))

    return results


def is_generic_trash(text: str) -> bool:
    cleaned = normalize_whitespace(text.lower().strip("!?. "))
    return cleaned in GENERIC_TRASH or (
        len(cleaned.split()) <= 3
        and not any(ch.isdigit() for ch in cleaned)
        and not any(
            keyword in cleaned
            for keyword in (
                "запах",
                "аромат",
                "пах",
                "увлаж",
                "текстур",
                "упаков",
                "впит",
                "кожа",
                "эффект",
                "аллер",
                "реакц",
            )
        )
    )


def build_registry() -> dict:
    text = INPUT_PATH.read_text()
    blocks = text.split("- ![Аватар пользователя]")[1:]

    units_registry = []
    signals_registry = []
    manual_queue = []
    trash = []
    used_signal_fragments = set()

    for index, block in enumerate(blocks, 1):
        parsed = parse_block(block, index)
        if not parsed:
            continue

        unit: Unit = parsed["unit"]
        parts = parsed["parts"]
        plus_items = parsed["plus_items"]
        minus_items = parsed["minus_items"]
        unit_has_signal = False

        for item in plus_items:
            signal_fragment = item
            dedupe_key = (unit.unit_index, "позитив", signal_fragment.lower())
            if dedupe_key in used_signal_fragments:
                continue
            used_signal_fragments.add(dedupe_key)
            signals_registry.append(
                {
                    "signal_id": f"{PRODUCT_KEY}:{unit.unit_index}:s{len(signals_registry) + 1}",
                    "product_key": PRODUCT_KEY,
                    "unit_index": unit.unit_index,
                    "name": unit.name,
                    "category": "позитив",
                    "signal_code": map_list_item(item, negative=False),
                    "signal_fragment": f"«{signal_fragment}»",
                    "secondary_flags": [],
                }
            )
            unit_has_signal = True

        for item in minus_items:
            signal_fragment = item
            dedupe_key = (unit.unit_index, "негатив", signal_fragment.lower())
            if dedupe_key in used_signal_fragments:
                continue
            used_signal_fragments.add(dedupe_key)
            signals_registry.append(
                {
                    "signal_id": f"{PRODUCT_KEY}:{unit.unit_index}:s{len(signals_registry) + 1}",
                    "product_key": PRODUCT_KEY,
                    "unit_index": unit.unit_index,
                    "name": unit.name,
                    "category": "негатив",
                    "signal_code": map_list_item(item, negative=True),
                    "signal_fragment": f"«{signal_fragment}»",
                    "secondary_flags": [],
                }
            )
            unit_has_signal = True

        for label, content in parts:
            if not content:
                continue
            default_category = None
            if label == "Достоинства":
                default_category = "позитив"
            elif label == "Недостатки":
                default_category = "негатив"

            if is_generic_trash(content) and not (plus_items or minus_items):
                continue

            for clause in sentence_chunks(content):
                if is_generic_trash(clause):
                    continue
                for category, code, fragment, flags in classify_clause(clause, default_category):
                    if category == "manual":
                        manual_queue.append(
                            f"{unit.unit_index} | {unit.name} | ручной разбор | «{fragment}» | причина: {code}"
                        )
                        continue
                    dedupe_key = (unit.unit_index, category, fragment.lower())
                    if dedupe_key in used_signal_fragments:
                        continue
                    used_signal_fragments.add(dedupe_key)
                    signals_registry.append(
                        {
                            "signal_id": f"{PRODUCT_KEY}:{unit.unit_index}:s{len(signals_registry) + 1}",
                            "product_key": PRODUCT_KEY,
                            "unit_index": unit.unit_index,
                            "name": unit.name,
                            "category": category,
                            "signal_code": code,
                            "signal_fragment": f"«{fragment}»",
                            "secondary_flags": flags,
                        }
                    )
                    unit_has_signal = True

        if not unit_has_signal and not manual_queue:
            trash.append(f"{unit.unit_index} | {unit.name} | мусор | «{unit.full_quote or '—'}»")

        units_registry.append(
            {
                "product_key": PRODUCT_KEY,
                "unit_index": unit.unit_index,
                "name": unit.name,
                "date": unit.date,
                "stars": unit.stars,
                "source": unit.source,
                "full_quote": f"«{unit.full_quote or '—'}»",
            }
        )

    # Recompute trash correctly: only units without signals/manual.
    units_with_signal = {entry["unit_index"] for entry in signals_registry}
    units_in_manual = {entry.split(" | ", 1)[0] for entry in manual_queue}
    trash = []
    for unit in units_registry:
        if unit["unit_index"] not in units_with_signal and unit["unit_index"] not in units_in_manual:
            trash.append(f"{unit['unit_index']} | {unit['name']} | мусор | {unit['full_quote']}")

    stats = {
        "B_total": len(units_registry),
        "N_trash": len(trash),
        "B_clean": len(units_registry) - len(trash),
        "N_manual": len(manual_queue),
        "N_units_with_signals": len(units_with_signal),
        "N_signals_total": len(signals_registry),
        "signals_by_category": dict(Counter(entry["category"] for entry in signals_registry)),
    }

    return {
        "product_key": PRODUCT_KEY,
        "units_registry": units_registry,
        "signals_registry": signals_registry,
        "manual_queue": manual_queue,
        "trash": trash,
        "stats": stats,
    }


def main() -> None:
    registry = build_registry()
    OUTPUT_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2))
    print(f"written {OUTPUT_PATH}")
    print(json.dumps(registry["stats"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
