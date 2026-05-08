#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = ROOT / "00_dashboard"
DATA_JS = DASHBOARD_DIR / "data.js"
GENERIC_COMPARISON_MARKERS = (
    "другим запахом",
    "другим продуктом",
    "другими кремами",
    "ожидаемым образом",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def cleanup(text: str) -> str:
    return text.replace("<br>", "\n").replace("`", "").strip()


def slugify(text: str) -> str:
    text = re.sub(r"[^\w]+", "-", text.lower(), flags=re.U)
    return re.sub(r"-{2,}", "-", text).strip("-") or "item"


def visible_files(base: Path, suffix: str = ".md") -> list[Path]:
    paths = []
    for path in sorted(base.rglob(f"*{suffix}")):
        if path.name.startswith("."):
            continue
        if path.name.endswith("_INPUT.md"):
            continue
        if "__view." in path.name:
            continue
        paths.append(path)
    return paths


def extract_key(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return cleanup(match.group(1)) if match else None


def extract_heading_block(text: str, heading: str) -> str:
    match = re.search(
        rf"## {re.escape(heading)}\n\n(.*?)(?:\n## |\Z)",
        text,
        re.S,
    )
    return match.group(1).strip() if match else ""


def extract_list_after_key(text: str, list_key: str) -> list[str]:
    match = re.search(
        rf"{re.escape(list_key)}:\n((?:- .+\n)+)",
        text,
        re.S,
    )
    if not match:
        return []
    return [cleanup(line[2:]) for line in match.group(1).splitlines() if line.startswith("- ")]


def extract_markdown_table(text: str, heading: str) -> list[list[str]]:
    if heading not in text:
        return []
    after = text.split(heading, 1)[1]
    lines = after.splitlines()
    table_lines: list[str] = []
    started = False
    for line in lines:
        if line.startswith("|"):
            started = True
            table_lines.append(line)
            continue
        if started and not line.strip():
            break
    if len(table_lines) < 3:
        return []
    rows: list[list[str]] = []
    for line in table_lines:
        parts = [cleanup(cell) for cell in line.strip().strip("|").split("|")]
        rows.append(parts)
    return [rows[0]] + [row for row in rows[2:] if len(row) == len(rows[0])]


def parse_signal_entries(cell: str) -> list[dict]:
    entries: list[dict] = []
    for raw_line in cleanup(cell).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        label = line
        evidence = ""
        if " — " in line:
            label, evidence = line.split(" — ", 1)
        evidence = cleanup(evidence).strip('"')
        entries.append(
            {
                "label": cleanup(label),
                "evidence": evidence,
                "raw": cleanup(line),
                "type": cleanup(label)[:1],
            }
        )
    return entries


def parse_overlay_rows(text: str) -> list[dict]:
    table = extract_markdown_table(text, "## Overlay Table")
    if not table:
        return []
    headers = table[0]
    rows: list[dict] = []
    for raw_row in table[1:]:
        row = {headers[i]: raw_row[i] if i < len(raw_row) else "" for i in range(len(headers))}
        signals = parse_signal_entries(row.get("signals", ""))
        rows.append(
            {
                "id": cleanup(row.get("id", "")),
                "author": cleanup(row.get("author", "")),
                "date": cleanup(row.get("date", "")),
                "review": cleanup(row.get("review", "")),
                "signals": signals,
                "signal_labels": [entry["label"] for entry in signals],
            }
        )
    return rows


def parse_price_snapshot(path: Path) -> dict:
    text = read_text(path)
    table = extract_markdown_table(text, "## Snapshot Table")
    return {
        "title": "Price Value Snapshot",
        "path": str(path),
        "rows": [
            {table[0][i]: row[i] for i in range(len(table[0]))}
            for row in table[1:]
        ] if table else [],
        "insights": extract_bullets(text, "## Что Это Уже Даёт Для Следующего Этапа"),
    }


def extract_bullets(text: str, heading: str) -> list[str]:
    block = extract_heading_block(text, heading)
    return [cleanup(line[2:]) for line in block.splitlines() if line.startswith("- ")]


def extract_toolkit_tools(path: Path, limit: int = 3) -> list[dict]:
    if not path.exists():
        return []
    text = read_text(path)
    tools: list[dict] = []
    for match in re.finditer(r"## Инструмент:\s*(.+?)\n(.*?)(?=\n## Инструмент:|\Z)", text, re.S):
        name = cleanup(match.group(1))
        body = match.group(2)
        why_match = re.search(r"### Зачем нужен\n(.*?)(?:\n### |\Z)", body, re.S)
        why_lines = cleanup(why_match.group(1)).splitlines() if why_match else []
        tools.append({"name": name, "why": why_lines[0] if why_lines else ""})
        if len(tools) >= limit:
            break
    return tools


def user_modifier_status(path: Path) -> str:
    if not path.exists():
        return "Файл модификаторов ещё не создан."
    text = read_text(path)
    meaningful_lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.startswith("#") and "Сюда ты потом добавляешь" not in line
    ]
    return "Есть пользовательские override-правила." if meaningful_lines else "Пользовательские модификаторы пока пустые."


def build_stage03_specialists() -> list[dict]:
    roles_root = ROOT / "00_project" / "03_roles"
    marketplace_profile = roles_root / "specialists" / "strategy_group" / "marketplace_strategist.md"
    behavioral_profile = roles_root / "specialists" / "strategy_group" / "behavioral_strategist.md"
    marketplace_tools = roles_root / "toolkits" / "marketplace_strategist" / "default_tools.md"
    behavioral_tools = roles_root / "toolkits" / "behavioral_strategist" / "default_tools.md"
    marketplace_mods = roles_root / "toolkits" / "marketplace_strategist" / "user_modifiers.md"
    behavioral_mods = roles_root / "toolkits" / "behavioral_strategist" / "user_modifiers.md"

    return [
        {
            "name": "Техническая сборка по правилам",
            "type": "service_ai_layer",
            "stage": "3A",
            "decision_role": "service owner",
            "authority": "Собирает широкий черновик, но не принимает маркетинговые решения.",
            "does": [
                "дедупликация",
                "отсев невозможного",
                "привязка строк к видимой опоре",
                "visible modifiers: цена, объём, claims",
            ],
            "does_not": [
                "не делает мастер-матрицу",
                "не решает, что важно для рынка",
                "не выбирает стратегию",
            ],
            "influence": "Даёт специалистам чистый кандидатник, чтобы они не начинали с хаоса.",
            "profile_path": "",
            "toolkit_path": str(ROOT / "00_project" / "06_templates" / "03a__product_key__technical_matrix_draft_TEMPLATE.md"),
            "tools": [
                {"name": "keep", "why": "видимо возможная строка должна дойти до специалиста"},
                {"name": "hold_for_specialist", "why": "спорная, но живая строка не убивается автоматически"},
                {"name": "drop_no_evidence", "why": "строка без видимой опоры не идёт дальше"},
            ],
            "modifier_status": "Пользовательские модификаторы не применяются: это сервисный слой.",
        },
        {
            "name": "Маркетплейс-стратег / категорийный стратег",
            "type": "specialist",
            "stage": "3B-3C",
            "decision_role": "owner",
            "authority": "Принимает решение по рабочим матрицам и собирает мастер-матрицу.",
            "does": [
                "проверяет категорийную норму",
                "отличает безопасное покупательское чтение от прямого переноса",
                "ставит статусы confirmed / weakened / angle_candidate / hold / reject",
                "держит риск обещаний",
            ],
            "does_not": [
                "не придумывает финальную стратегию",
                "не переносит силу конкурента на героя без видимой опоры",
            ],
            "influence": "Определяет, какие строки можно читать как perception-ready, а какие только как гипотезу или ограничение.",
            "profile_path": str(marketplace_profile),
            "toolkit_path": str(marketplace_tools),
            "tools": extract_toolkit_tools(marketplace_tools),
            "modifier_status": user_modifier_status(marketplace_mods),
        },
        {
            "name": "Поведенческий стратег",
            "type": "specialist",
            "stage": "3B-3C",
            "decision_role": "input",
            "authority": "Предлагает человеческую логику чтения, но не финально утверждает матрицу.",
            "does": [
                "разводит кому стоп и когда терпимо",
                "ищет удерживающий мотив",
                "проверяет сценарии использования",
                "не даёт минусам читаться слишком широко",
            ],
            "does_not": [
                "не выдаёт гипотезу за видимый сигнал",
                "не переписывает итог вместо owner",
            ],
            "influence": "Заполняет человеческую часть строк: стоп, терпимость, удержание покупки.",
            "profile_path": str(behavioral_profile),
            "toolkit_path": str(behavioral_tools),
            "tools": extract_toolkit_tools(behavioral_tools),
            "modifier_status": user_modifier_status(behavioral_mods),
        },
    ]


def build_stage04_specialists() -> list[dict]:
    roles_root = ROOT / "00_project" / "03_roles"
    brand_profile = roles_root / "specialists" / "strategy_group" / "brand_strategist.md"
    behavioral_profile = roles_root / "specialists" / "strategy_group" / "behavioral_strategist.md"
    marketplace_profile = roles_root / "specialists" / "strategy_group" / "marketplace_strategist.md"
    brand_tools = roles_root / "toolkits" / "brand_strategist" / "default_tools.md"
    behavioral_tools = roles_root / "toolkits" / "behavioral_strategist" / "default_tools.md"
    marketplace_tools = roles_root / "toolkits" / "marketplace_strategist" / "default_tools.md"
    brand_mods = roles_root / "toolkits" / "brand_strategist" / "user_modifiers.md"
    behavioral_mods = roles_root / "toolkits" / "behavioral_strategist" / "user_modifiers.md"
    marketplace_mods = roles_root / "toolkits" / "marketplace_strategist" / "user_modifiers.md"

    return [
        {
            "name": "Стратег позиционирования",
            "type": "specialist",
            "stage": "4",
            "decision_role": "owner",
            "authority": "Собирает выводы по мастер-матрице и отделяет видимые выводы от интерпретаций.",
            "does": [
                "фиксирует perception-ready контракты",
                "разводит выводы и гипотезы",
                "решает, что достойно стратегии",
            ],
            "does_not": [
                "не выбирает ещё финальную рекламную механику",
                "не смешивает всё в одну серую формулировку",
            ],
            "influence": "Даёт чистый мост между мастер-матрицей и стратегическим выбором.",
            "profile_path": str(brand_profile),
            "toolkit_path": str(brand_tools),
            "tools": extract_toolkit_tools(brand_tools),
            "modifier_status": user_modifier_status(brand_mods),
        },
        {
            "name": "Поведенческий стратег",
            "type": "specialist",
            "stage": "4",
            "decision_role": "input",
            "authority": "Проверяет, почему человек поверит линии, испугается её или отмахнётся.",
            "does": [
                "отделяет видимый сигнал от гипотезы",
                "объясняет терпимость к минусам",
                "ищет человеческую логику чтения",
            ],
            "does_not": [
                "не переписывает итог вместо owner",
                "не натягивает теорию на слабый сигнал",
            ],
            "influence": "Помогает не спутать интерпретацию с тем, что реально считывает покупатель.",
            "profile_path": str(behavioral_profile),
            "toolkit_path": str(behavioral_tools),
            "tools": extract_toolkit_tools(behavioral_tools),
            "modifier_status": user_modifier_status(behavioral_mods),
        },
        {
            "name": "Маркетплейс-стратег",
            "type": "specialist",
            "stage": "4",
            "decision_role": "filter",
            "authority": "Режет то, что не держится категорией и покупательским чтением рынка.",
            "does": [
                "проверяет категорийную норму",
                "держит границу обещаний",
                "убирает ложные переносы с конкурентов",
            ],
            "does_not": [
                "не превращает выводы в креативные идеи",
                "не даёт косвенным конкурентам говорить за героя",
            ],
            "influence": "Сохраняет выводы в границах реального восприятия маркетплейса.",
            "profile_path": str(marketplace_profile),
            "toolkit_path": str(marketplace_tools),
            "tools": extract_toolkit_tools(marketplace_tools),
            "modifier_status": user_modifier_status(marketplace_mods),
        },
    ]


def build_stage05_specialists() -> list[dict]:
    roles_root = ROOT / "00_project" / "03_roles"
    brand_profile = roles_root / "specialists" / "strategy_group" / "brand_strategist.md"
    behavioral_profile = roles_root / "specialists" / "strategy_group" / "behavioral_strategist.md"
    marketplace_profile = roles_root / "specialists" / "strategy_group" / "marketplace_strategist.md"
    creative_profile = roles_root / "specialists" / "creative_group" / "creative_director.md"
    brand_tools = roles_root / "toolkits" / "brand_strategist" / "default_tools.md"
    behavioral_tools = roles_root / "toolkits" / "behavioral_strategist" / "default_tools.md"
    marketplace_tools = roles_root / "toolkits" / "marketplace_strategist" / "default_tools.md"
    creative_tools = roles_root / "toolkits" / "creative_director" / "default_tools.md"
    brand_mods = roles_root / "toolkits" / "brand_strategist" / "user_modifiers.md"
    behavioral_mods = roles_root / "toolkits" / "behavioral_strategist" / "user_modifiers.md"
    marketplace_mods = roles_root / "toolkits" / "marketplace_strategist" / "user_modifiers.md"
    creative_mods = roles_root / "toolkits" / "creative_director" / "user_modifiers.md"

    return [
        {
            "name": "Стратег позиционирования",
            "type": "specialist",
            "stage": "5",
            "decision_role": "owner",
            "authority": "Выбирает primary + support и собирает стратегическое ядро без компромиссной каши.",
            "does": [
                "фильтрует допустимые линии",
                "собирает пару primary + support",
                "фиксирует жертвы и rejected-линии",
            ],
            "does_not": [
                "не берёт стратегию из вкуса",
                "не обещает то, что не выдержит восприятие",
            ],
            "influence": "Определяет, какой именно рекламный ход мы понесём дальше в воронку.",
            "profile_path": str(brand_profile),
            "toolkit_path": str(brand_tools),
            "tools": extract_toolkit_tools(brand_tools),
            "modifier_status": user_modifier_status(brand_mods),
        },
        {
            "name": "Поведенческий стратег",
            "type": "specialist",
            "stage": "5",
            "decision_role": "input",
            "authority": "Проверяет, поверит ли человек выбранной линии после карточки и отзывов.",
            "does": [
                "проверяет человеческую правдоподобность",
                "смотрит, не натянута ли линия",
                "ловит риск расхождения ожидания и чтения отзывов",
            ],
            "does_not": [
                "не решает финально вместо owner",
                "не раздувает объяснения сверх опоры",
            ],
            "influence": "Не даёт стратегии стать красивой, но психологически пустой.",
            "profile_path": str(behavioral_profile),
            "toolkit_path": str(behavioral_tools),
            "tools": extract_toolkit_tools(behavioral_tools),
            "modifier_status": user_modifier_status(behavioral_mods),
        },
        {
            "name": "Маркетплейс-стратег",
            "type": "specialist",
            "stage": "5",
            "decision_role": "filter",
            "authority": "Отсекает линии, которые конфликтуют с категорией, рынком и видимыми отзывами.",
            "does": [
                "режет слабые claims",
                "держит границу обещаний",
                "не даёт сделать паритет уникальностью",
            ],
            "does_not": [
                "не пишет стратегию вместо owner",
                "не усиливает линию только потому, что она красиво звучит",
            ],
            "influence": "Делает стратегию живой на маркетплейсе, а не только красивой на бумаге.",
            "profile_path": str(marketplace_profile),
            "toolkit_path": str(marketplace_tools),
            "tools": extract_toolkit_tools(marketplace_tools),
            "modifier_status": user_modifier_status(marketplace_mods),
        },
        {
            "name": "Креативный директор",
            "type": "specialist",
            "stage": "5",
            "decision_role": "variant",
            "authority": "Даёт отдельный вариант B, если рядом есть второй сильный рекламный ход.",
            "does": [
                "ищет альтернативный рефрейм",
                "усиливает контраст без вранья",
                "проверяет стратегию на банальность",
            ],
            "does_not": [
                "не смешивает два хода в серое среднее",
                "не спорит с review reality",
            ],
            "influence": "Нужен, когда хочется не просто безопасный выбор, а живую рекламную энергию без потери опоры.",
            "profile_path": str(creative_profile),
            "toolkit_path": str(creative_tools),
            "tools": extract_toolkit_tools(creative_tools),
            "modifier_status": user_modifier_status(creative_mods),
        },
    ]


def build_stage06_specialists() -> list[dict]:
    roles_root = ROOT / "00_project" / "03_roles"
    comm_profile = roles_root / "specialists" / "strategy_group" / "communication_strategist.md"
    brand_profile = roles_root / "specialists" / "strategy_group" / "brand_strategist.md"
    behavioral_profile = roles_root / "specialists" / "strategy_group" / "behavioral_strategist.md"
    marketplace_profile = roles_root / "specialists" / "strategy_group" / "marketplace_strategist.md"
    creative_profile = roles_root / "specialists" / "creative_group" / "creative_director.md"
    comm_tools = roles_root / "toolkits" / "communication_strategist" / "default_tools.md"
    brand_tools = roles_root / "toolkits" / "brand_strategist" / "default_tools.md"
    behavioral_tools = roles_root / "toolkits" / "behavioral_strategist" / "default_tools.md"
    marketplace_tools = roles_root / "toolkits" / "marketplace_strategist" / "default_tools.md"
    creative_tools = roles_root / "toolkits" / "creative_director" / "default_tools.md"
    comm_mods = roles_root / "toolkits" / "communication_strategist" / "user_modifiers.md"
    brand_mods = roles_root / "toolkits" / "brand_strategist" / "user_modifiers.md"
    behavioral_mods = roles_root / "toolkits" / "behavioral_strategist" / "user_modifiers.md"
    marketplace_mods = roles_root / "toolkits" / "marketplace_strategist" / "user_modifiers.md"
    creative_mods = roles_root / "toolkits" / "creative_director" / "user_modifiers.md"

    return [
        {
            "name": "Коммуникационный стратег / архитектор воронки",
            "type": "specialist",
            "stage": "6",
            "decision_role": "owner",
            "authority": "Собирает порядок слайдов и назначает работу каждому слайду.",
            "does": [
                "строит маршрут убеждения",
                "назначает buyer question каждому слайду",
                "держит one slide = one job",
            ],
            "does_not": [
                "не пишет финальный copy",
                "не оживляет rejected-линии",
            ],
            "influence": "Превращает стратегию в рабочую последовательность карточки.",
            "profile_path": str(comm_profile),
            "toolkit_path": str(comm_tools),
            "tools": extract_toolkit_tools(comm_tools),
            "modifier_status": user_modifier_status(comm_mods),
        },
        {
            "name": "Стратег позиционирования",
            "type": "specialist",
            "stage": "6",
            "decision_role": "input",
            "authority": "Следит, чтобы воронка не потеряла primary + support.",
            "does": [
                "передаёт стратегическое ядро",
                "удерживает rejected-линии закрытыми",
                "проверяет связность со стратегией",
            ],
            "does_not": [
                "не меняет воронку ради вкуса",
                "не пишет copy вместо owner",
            ],
            "influence": "Не даёт архитектуре уйти в чужую стратегию.",
            "profile_path": str(brand_profile),
            "toolkit_path": str(brand_tools),
            "tools": extract_toolkit_tools(brand_tools),
            "modifier_status": user_modifier_status(brand_mods),
        },
        {
            "name": "Поведенческий стратег",
            "type": "specialist",
            "stage": "6",
            "decision_role": "input",
            "authority": "Подсказывает порядок тревог и what-must-be-closed-next.",
            "does": [
                "строит ladder buyer fears",
                "проверяет правдоподобность порядка",
                "ловит необработанные страхи",
            ],
            "does_not": [
                "не переписывает структуру вместо owner",
                "не превращает воронку в психологический трактат",
            ],
            "influence": "Помогает поставить слайды в том порядке, как реально думает покупатель.",
            "profile_path": str(behavioral_profile),
            "toolkit_path": str(behavioral_tools),
            "tools": extract_toolkit_tools(behavioral_tools),
            "modifier_status": user_modifier_status(behavioral_mods),
        },
        {
            "name": "Маркетплейс-стратег",
            "type": "specialist",
            "stage": "6",
            "decision_role": "filter",
            "authority": "Режет слайды и claims, которые плохо читаются в маркетплейс-скролле.",
            "does": [
                "убирает когнитивный шум",
                "держит promise boundary",
                "не даёт паритету прикинуться отличием",
            ],
            "does_not": [
                "не делает креатив ради креатива",
                "не допускает claims без видимой опоры",
            ],
            "influence": "Оставляет только те слайды, которые реально двигают выбор.",
            "profile_path": str(marketplace_profile),
            "toolkit_path": str(marketplace_tools),
            "tools": extract_toolkit_tools(marketplace_tools),
            "modifier_status": user_modifier_status(marketplace_mods),
        },
        {
            "name": "Креативный директор",
            "type": "specialist",
            "stage": "6",
            "decision_role": "variant",
            "authority": "Даёт альтернативную структуру только если текущая воронка слишком плоская.",
            "does": [
                "ищет второй сильный ход",
                "может собрать variant B",
                "усиливает контраст без вранья",
            ],
            "does_not": [
                "не смешивает варианты в серую кашу",
                "не переписывает основной документ без запроса",
            ],
            "influence": "Нужен, когда базовая логика уже есть, но хочется отдельный сильный вариант.",
            "profile_path": str(creative_profile),
            "toolkit_path": str(creative_tools),
            "tools": extract_toolkit_tools(creative_tools),
            "modifier_status": user_modifier_status(creative_mods),
        },
    ]


def build_stage07_specialists() -> list[dict]:
    roles_root = ROOT / "00_project" / "03_roles"
    copy_profile = roles_root / "specialists" / "creative_group" / "copywriter.md"
    art_profile = roles_root / "specialists" / "creative_group" / "art_director.md"
    comm_profile = roles_root / "specialists" / "strategy_group" / "communication_strategist.md"
    marketplace_profile = roles_root / "specialists" / "strategy_group" / "marketplace_strategist.md"
    creative_profile = roles_root / "specialists" / "creative_group" / "creative_director.md"
    copy_tools = roles_root / "toolkits" / "copywriter" / "default_tools.md"
    art_tools = roles_root / "toolkits" / "art_director" / "default_tools.md"
    comm_tools = roles_root / "toolkits" / "communication_strategist" / "default_tools.md"
    marketplace_tools = roles_root / "toolkits" / "marketplace_strategist" / "default_tools.md"
    creative_tools = roles_root / "toolkits" / "creative_director" / "default_tools.md"
    copy_mods = roles_root / "toolkits" / "copywriter" / "user_modifiers.md"
    art_mods = roles_root / "toolkits" / "art_director" / "user_modifiers.md"
    comm_mods = roles_root / "toolkits" / "communication_strategist" / "user_modifiers.md"
    marketplace_mods = roles_root / "toolkits" / "marketplace_strategist" / "user_modifiers.md"
    creative_mods = roles_root / "toolkits" / "creative_director" / "user_modifiers.md"

    return [
        {
            "name": "Копирайтер",
            "type": "specialist",
            "stage": "7A",
            "decision_role": "owner",
            "authority": "Пишет заголовки, подзаголовки и микротекст внутри locked funnel.",
            "does": [
                "пишет strict и bolder варианты",
                "держит white marketing",
                "привязывает текст к visible support",
            ],
            "does_not": [
                "не меняет порядок слайдов",
                "не усиливает claim без опоры",
            ],
            "influence": "Переводит роли слайдов в человеческий текст без кликбейта.",
            "profile_path": str(copy_profile),
            "toolkit_path": str(copy_tools),
            "tools": extract_toolkit_tools(copy_tools),
            "modifier_status": user_modifier_status(copy_mods),
        },
        {
            "name": "Арт-директор",
            "type": "specialist",
            "stage": "7B",
            "decision_role": "owner",
            "authority": "Назначает визуальную задачу и иерархию внимания каждому слайду.",
            "does": [
                "строит visual hierarchy",
                "ищет visual proof",
                "держит visual honesty",
            ],
            "does_not": [
                "не врёт картинкой",
                "не рисует чужую премиальность",
            ],
            "influence": "Делает так, чтобы слайд показывал смысл, а не только украшал его.",
            "profile_path": str(art_profile),
            "toolkit_path": str(art_tools),
            "tools": extract_toolkit_tools(art_tools),
            "modifier_status": user_modifier_status(art_mods),
        },
        {
            "name": "Коммуникационный стратег",
            "type": "specialist",
            "stage": "7",
            "decision_role": "input",
            "authority": "Следит, чтобы copy и visual не разрушили роль слайда из funnel.",
            "does": [
                "удерживает функцию каждого слайда",
                "проверяет question-to-slide fit",
                "ловит архитектурные сдвиги",
            ],
            "does_not": [
                "не меняет funnel внутри этапа 7",
                "не пишет финальный текст вместо copywriter",
            ],
            "influence": "Помогает не потерять маршрут убеждения при наполнении карточки.",
            "profile_path": str(comm_profile),
            "toolkit_path": str(comm_tools),
            "tools": extract_toolkit_tools(comm_tools),
            "modifier_status": user_modifier_status(comm_mods),
        },
        {
            "name": "Маркетплейс-стратег",
            "type": "specialist",
            "stage": "7",
            "decision_role": "filter",
            "authority": "Режет текст и визуал, которые обещают больше, чем выдерживает восприятие.",
            "does": [
                "держит claim limits",
                "режет overpromise",
                "проверяет маркетплейс-читаемость",
            ],
            "does_not": [
                "не даёт визуалу лгать",
                "не допускает rejected-линий обратно",
            ],
            "influence": "Сохраняет карточку продающей, но не конфликтующей с отзывами.",
            "profile_path": str(marketplace_profile),
            "toolkit_path": str(marketplace_tools),
            "tools": extract_toolkit_tools(marketplace_tools),
            "modifier_status": user_modifier_status(marketplace_mods),
        },
        {
            "name": "Креативный директор",
            "type": "specialist",
            "stage": "7C",
            "decision_role": "owner",
            "authority": "Проводит integration pass и ловит конфликт между copy, visual и funnel.",
            "does": [
                "проверяет цельность сборки",
                "ловит банальность и шум",
                "не даёт карточке стать серой кашей",
            ],
            "does_not": [
                "не переписывает всё заново",
                "не меняет стратегию на этом этапе",
            ],
            "influence": "Собирает текст и визуал в одну живую систему перед QA.",
            "profile_path": str(creative_profile),
            "toolkit_path": str(creative_tools),
            "tools": extract_toolkit_tools(creative_tools),
            "modifier_status": user_modifier_status(creative_mods),
        },
    ]


def detect_role_from_path(path: Path) -> str:
    if "hero" in path.parts:
        return "hero"
    if "direct_competitors" in path.parts:
        return "direct_competitors"
    if "indirect_competitors" in path.parts:
        return "indirect_competitors"
    return "project"


def parse_passport(path: Path) -> dict:
    text = read_text(path)
    return {
        "path": str(path),
        "role": extract_key(text, "product_role") or detect_role_from_path(path),
        "product_key": extract_key(text, "product_key") or path.parent.name,
        "product_name": extract_key(text, "product_name") or path.stem,
        "brand": extract_key(text, "brand") or "—",
        "category": extract_key(text, "category") or "—",
        "price": extract_key(text, "price_snapshot_ref") or "unclear",
        "unit_price": extract_key(text, "how_to_calculate_unit_price") or "unclear",
        "volume": extract_key(text, "volume_weight_count") or "unclear",
        "seller_main_claim": extract_key(text, "seller_main_claim") or "—",
        "declared_use_cases": extract_list_after_key(text, "declared_use_cases"),
        "claims_to_check": extract_list_after_key(text, "claims_to_check_in_reviews"),
        "possible_overpromises": extract_list_after_key(text, "possible_overpromises"),
        "missing_or_unclear": extract_list_after_key(text, "missing_or_unclear"),
        "feeds_contracts_matrix": extract_list_after_key(text, "feeds_contracts_matrix"),
    }


def is_generic_comparison(label: str) -> bool:
    label = label.lower()
    return any(marker in label for marker in GENERIC_COMPARISON_MARKERS)


def parse_pattern_inventory(text: str, section_title: str, group_key: str) -> list[dict]:
    block_match = re.search(
        rf"### {re.escape(section_title)}\n(.*?)(?:\n### |\n## |\Z)",
        text,
        re.S,
    )
    if not block_match:
        return []
    items = []
    for index, line in enumerate(block_match.group(1).splitlines(), start=1):
        if not line.startswith("- "):
            continue
        raw = cleanup(line[2:])
        count_match = re.search(r"— reviews (\d+)", line)
        signals_match = re.search(r"\|\s*signals\s+(\d+)", line)
        example_match = re.search(r'пример:\s*"([^"]+)"', raw)
        label = raw.split("— reviews", 1)[0].strip()
        items.append(
            {
                "id": f"{group_key}:{index}:{slugify(label)}",
                "group": group_key,
                "label": cleanup(label),
                "reviews": int(count_match.group(1)) if count_match else 0,
                "signals": int(signals_match.group(1)) if signals_match else 0,
                "example": cleanup(example_match.group(1)) if example_match else "",
                "generic": group_key == "comparisons" and is_generic_comparison(label),
                "raw": raw,
            }
        )
    return items


def enrich_patterns(items: list[dict], overlay_rows: list[dict]) -> list[dict]:
    review_ids_by_label: dict[str, list[str]] = {}
    evidence_by_label: dict[str, str] = {}
    for row in overlay_rows:
        for entry in row["signals"]:
            label = entry["label"]
            if not label:
                continue
            review_ids_by_label.setdefault(label, [])
            if row["id"] and row["id"] not in review_ids_by_label[label]:
                review_ids_by_label[label].append(row["id"])
            if label not in evidence_by_label and entry.get("evidence"):
                evidence_by_label[label] = entry["evidence"]
    for item in items:
        item["review_ids"] = review_ids_by_label.get(item["label"], [])
        if not item.get("example"):
            item["example"] = evidence_by_label.get(item["label"], "")
    return items


def parse_signal_stats(text: str) -> dict:
    stats = {}
    match = re.search(r"## Signal Stats\n(.*?)(?:\n## |\Z)", text, re.S)
    if not match:
        return stats
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        line = line[2:]
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        stats[cleanup(key)] = cleanup(value)
    return stats


def parse_signal_markup(path: Path) -> dict:
    text = read_text(path)
    title = text.splitlines()[0].replace("#", "").strip() if text else path.stem
    overlay_rows = parse_overlay_rows(text)
    positives = enrich_patterns(parse_pattern_inventory(text, "🟢 Позитив", "positives"), overlay_rows)
    negatives = enrich_patterns(parse_pattern_inventory(text, "🔴 Негатив", "negatives"), overlay_rows)
    scenarios = enrich_patterns(parse_pattern_inventory(text, "🟣 Сценарий", "scenarios"), overlay_rows)
    comparisons = enrich_patterns(parse_pattern_inventory(text, "🔵 Сравнение", "comparisons"), overlay_rows)
    return {
        "path": str(path),
        "role": detect_role_from_path(path),
        "product_key": path.parent.name,
        "title": title,
        "stats": parse_signal_stats(text),
        "positives": positives,
        "negatives": negatives,
        "scenarios": scenarios,
        "comparisons": comparisons,
        "overlay_rows": overlay_rows,
    }


def parse_matrix(path: Path) -> dict:
    text = read_text(path)
    if path.name.startswith("03a__"):
        matrix_kind = "technical"
    elif "master_contracts_matrix" in path.name:
        matrix_kind = "master"
    else:
        matrix_kind = "local"
    heading = "## Таблица Кандидатов" if matrix_kind == "technical" else "## Матрица"
    rows = extract_markdown_table(text, heading)
    row_dicts = [
        {rows[0][i]: row[i] for i in range(len(rows[0]))}
        for row in rows[1:]
    ] if rows else []
    status_key = "Technical action" if matrix_kind == "technical" else "Статус"
    counts = Counter(row.get(status_key, "unclear") for row in row_dicts)
    anchors = extract_bullets(text, "## Visible Anchors") or extract_bullets(text, "## Factual Anchors")
    product_key = extract_key(text, "product_key") or path.parent.name
    return {
        "path": str(path),
        "role": detect_role_from_path(path),
        "product_key": product_key,
        "matrix_key": f"{product_key}::{matrix_kind}",
        "matrix_kind": matrix_kind,
        "routing_status": extract_key(text, "routing_status") or "approved_or_not_marked",
        "routing_note": extract_key(text, "routing_note") or "",
        "status_key": status_key,
        "title": "Technical Matrix Draft" if matrix_kind == "technical" else "Contracts Matrix",
        "anchors": anchors,
        "counts": counts,
        "rows": row_dicts,
        "columns": rows[0] if rows else [],
    }


def parse_hypotheses(text: str) -> list[dict]:
    hypotheses = []
    for match in re.finditer(r"(hypothesis_\d+):\n((?:  .+\n?)*)", text):
        name = cleanup(match.group(1))
        body = match.group(2)
        fields = {}
        for key in ("based_on", "interpretation", "confidence_level", "why_it_matters"):
            field_match = re.search(rf"  {key}:\s*(.+)", body)
            fields[key] = cleanup(field_match.group(1)) if field_match else ""
        hypotheses.append({"id": name, **fields})
    return hypotheses


def parse_matrix_conclusions(path: Path) -> dict:
    text = read_text(path)
    return {
        "path": str(path),
        "role": detect_role_from_path(path),
        "product_key": extract_key(text, "hero_product_key") or path.parent.name,
        "title": "Matrix Conclusions",
        "perception_ready_contracts": extract_list_after_key(text, "perception_ready_contracts"),
        "non_target_buyers": extract_list_after_key(text, "non_target_buyers"),
        "tolerable_negatives": extract_list_after_key(text, "tolerable_negatives"),
        "dangerous_negatives": extract_list_after_key(text, "dangerous_negatives"),
        "claim_risks": extract_list_after_key(text, "claim_risks"),
        "market_norms": extract_list_after_key(text, "market_norms_visible_in_direct_competitors"),
        "hypotheses": parse_hypotheses(text),
        "worth_developing": extract_list_after_key(text, "worth_developing_into_strategy"),
        "worth_testing": extract_list_after_key(text, "worth_testing_as_positioning_hypothesis"),
        "do_not_carry": extract_list_after_key(text, "do_not_carry_forward"),
    }


def parse_strategy_decision(path: Path) -> dict:
    text = read_text(path)
    table = extract_markdown_table(text, "## Допустимые Стратегические Линии")
    return {
        "path": str(path),
        "role": detect_role_from_path(path),
        "product_key": extract_key(text, "hero_product_key") or path.parent.name,
        "title": "Strategy Decision",
        "allowed": extract_list_after_key(text, "allowed_by_visible_perception_map"),
        "blocked": extract_list_after_key(text, "blocked_by_visible_perception_map"),
        "claim_limits": extract_list_after_key(text, "important_claim_limits"),
        "category_limits": extract_list_after_key(text, "important_category_limits"),
        "strategy_lines": [
            {table[0][i]: row[i] for i in range(len(table[0]))}
            for row in table[1:]
        ] if table else [],
        "rejected_lines": extract_list_after_key(text, "rejected_lines"),
        "outside_style_matrix": extract_list_after_key(text, "outside_of_style_matrix"),
        "primary_direction": extract_key(text, "primary_direction") or "—",
        "why_primary": extract_key(text, "why_primary") or "—",
        "supporting_direction": extract_key(text, "supporting_direction") or "—",
        "why_support": extract_key(text, "why_support") or "—",
        "why_pair_works": extract_key(text, "why_this_pair_works") or "—",
        "tradeoffs": extract_list_after_key(text, "tradeoffs"),
        "strategy_core": extract_list_after_key(text, "strategy_core"),
        "do_not_do": extract_list_after_key(text, "do_not_do"),
        "open_questions": extract_list_after_key(text, "open_questions"),
    }


def parse_slide_blocks(text: str) -> list[dict]:
    slides = []
    for match in re.finditer(r"### Слайд (\d+)\. (.*?)\n\n```text\n(.*?)```", text, re.S):
        number = int(match.group(1))
        title = cleanup(match.group(2))
        block = match.group(3)
        fields = {}
        for line in block.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            fields[cleanup(key)] = cleanup(value)
        slides.append({"number": number, "title": title, **fields})
    return slides


def parse_funnel_architecture(path: Path) -> dict:
    text = read_text(path)
    table = extract_markdown_table(text, "## Сводная Таблица Слайдов")
    return {
        "path": str(path),
        "role": detect_role_from_path(path),
        "product_key": extract_key(text, "hero_product_key") or path.parent.name,
        "title": "Funnel Architecture",
        "primary_direction": extract_key(text, "primary_direction") or "—",
        "supporting_direction": extract_key(text, "supporting_direction") or "—",
        "do_not_do": extract_list_after_key(text, "do_not_do"),
        "main_buyer_question": extract_key(text, "main_buyer_question") or "—",
        "main_buyer_fear": extract_key(text, "main_buyer_fear") or "—",
        "main_reassurance_needed": extract_key(text, "main_reassurance_needed") or "—",
        "slides_table": [
            {table[0][i]: row[i] for i in range(len(table[0]))}
            for row in table[1:]
        ] if table else [],
        "slides": parse_slide_blocks(text),
        "slide_necessity_check": extract_list_after_key(text, "slide_necessity_check"),
        "duplicate_check": extract_list_after_key(text, "duplicate_check"),
        "cognitive_noise_check": extract_list_after_key(text, "cognitive_noise_check"),
        "reassurance_sufficiency_check": extract_list_after_key(text, "reassurance_sufficiency_check"),
        "rejected_lines_check": extract_list_after_key(text, "rejected_lines_check"),
        "ready_for_card_layer": extract_key(text, "ready_for_card_layer") or "no",
        "open_questions": extract_list_after_key(text, "open_questions"),
        "return_needed": extract_list_after_key(text, "return_needed") or [extract_key(text, "return_needed") or "none"],
    }


def parse_card_layer(path: Path) -> dict:
    text = read_text(path)
    table = extract_markdown_table(text, "## Сводная Таблица Слайдов")
    return {
        "path": str(path),
        "role": detect_role_from_path(path),
        "product_key": extract_key(text, "hero_product_key") or path.parent.name,
        "title": "Card Layer",
        "primary_direction": extract_key(text, "primary_direction") or "—",
        "supporting_direction": extract_key(text, "supporting_direction") or "—",
        "locked_slide_order": extract_list_after_key(text, "locked_slide_order"),
        "do_not_do": extract_list_after_key(text, "do_not_do"),
        "claim_limits": extract_list_after_key(text, "claim_limits"),
        "visual_limits": extract_list_after_key(text, "visual_limits"),
        "slides_table": [
            {table[0][i]: row[i] for i in range(len(table[0]))}
            for row in table[1:]
        ] if table else [],
        "slides": parse_slide_blocks(text),
        "copy_vs_visual_conflicts": extract_list_after_key(text, "copy_vs_visual_conflicts"),
        "funnel_role_preserved": extract_list_after_key(text, "funnel_role_preserved"),
        "claim_risks": extract_list_after_key(text, "claim_risks"),
        "visual_overpromise_risks": extract_list_after_key(text, "visual_overpromise_risks"),
        "needs_return_to_stage_6": extract_list_after_key(text, "needs_return_to_stage_6") or [extract_key(text, "needs_return_to_stage_6") or "no"],
        "needs_return_to_stage_5": extract_list_after_key(text, "needs_return_to_stage_5") or [extract_key(text, "needs_return_to_stage_5") or "no"],
        "ready_for_qa": extract_key(text, "ready_for_qa") or "no",
        "open_questions": extract_list_after_key(text, "open_questions"),
    }


def sort_products(items: Iterable[dict]) -> list[dict]:
    order = {"hero": 0, "direct_competitors": 1, "indirect_competitors": 2}
    return sorted(items, key=lambda x: (order.get(x.get("role", ""), 9), x.get("product_key", "")))


def build_data() -> dict:
    passports = sort_products(
        parse_passport(path)
        for path in visible_files(ROOT / "01_intake" / "product_passports")
    )
    signal_markups = sort_products(
        parse_signal_markup(path)
        for path in visible_files(ROOT / "02_signal_markup")
        if "__signal_markup" in path.name
    )
    matrices = sort_products(
        parse_matrix(path)
        for path in visible_files(ROOT / "03_contract_matrices")
        if (path.name.startswith("03a__") or path.name.startswith("03__")) and path.suffix == ".md"
    )
    matrix_conclusions = sort_products(
        parse_matrix_conclusions(path)
        for path in visible_files(ROOT / "04_matrix_conclusions")
        if "__matrix_conclusions" in path.name
    )
    strategies = sort_products(
        parse_strategy_decision(path)
        for path in visible_files(ROOT / "05_strategy")
        if "__strategy_decision" in path.name
    )
    funnels = sort_products(
        parse_funnel_architecture(path)
        for path in visible_files(ROOT / "06_funnel")
        if "__funnel_architecture" in path.name
    )
    card_layers = sort_products(
        parse_card_layer(path)
        for path in visible_files(ROOT / "07_card_layer")
        if "__card_layer" in path.name
    )
    price_snapshot = parse_price_snapshot(ROOT / "01_intake" / "01__project__price_value_snapshot.md")

    return {
        "project": {
            "name": "Pipeline Dashboard",
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "root": str(ROOT),
            "counts": {
                "passports": len(passports),
                "signal_markups": len(signal_markups),
                "matrices": len(matrices),
                "matrix_conclusions": len(matrix_conclusions),
                "strategies": len(strategies),
                "funnels": len(funnels),
                "card_layers": len(card_layers),
            },
        },
        "stages": [
            {
                "id": "01",
                "title": "Intake",
                "label": "Паспорта и цена",
                "folder": "01_intake",
            "summary": "Слой видимых данных: кто есть кто, карточечные claims, цена, объём и опорные ограничения перед разметкой.",
                "price_snapshot": price_snapshot,
                "passports": passports,
            },
            {
                "id": "02",
                "title": "Signal Markup",
                "label": "Отзывы и сигналы",
                "folder": "02_signal_markup",
                "summary": "Разметка buyer-сигналов по каждому продукту: паттерны, частоты, сценарии, сравнения и зоны риска.",
                "markups": signal_markups,
            },
            {
                "id": "03",
                "title": "Contracts Matrix",
                "label": "Широкая матрица",
                "folder": "03_contract_matrices",
                "summary": "03A даёт видимые черновики, 03B-03C переводят их в покупательское восприятие: отзывы здесь сигналы, а не правда продукта.",
                "specialists": build_stage03_specialists(),
                "matrices": matrices,
            },
            {
                "id": "04",
                "title": "Matrix Conclusions",
                "label": "Выводы специалистов",
                "folder": "04_matrix_conclusions",
                "summary": "Стратег позиционирования собирает, что покупатель реально может считать из мастер-матрицы, а что пока остаётся гипотезой.",
                "specialists": build_stage04_specialists(),
                "conclusions": matrix_conclusions,
            },
            {
                "id": "05",
                "title": "Strategy Decision",
                "label": "Рекламная концепция",
                "folder": "05_strategy",
                "summary": "Здесь выбирается стратегическая пара и формулируется ядро рекламного хода, которое можно нести дальше в воронку.",
                "specialists": build_stage05_specialists(),
                "strategies": strategies,
            },
            {
                "id": "06",
                "title": "Funnel Architecture",
                "label": "Архитектура воронки",
                "folder": "06_funnel",
                "summary": "Этап 6 превращает стратегию в маршрут убеждения: какие слайды нужны, в каком порядке и какой вопрос закрывает каждый.",
                "specialists": build_stage06_specialists(),
                "funnels": funnels,
            },
            {
                "id": "07",
                "title": "Card Layer",
                "label": "Слой карточки",
                "folder": "07_card_layer",
                "summary": "Этап 7 заполняет воронку текстом и визуальными задачами, не меняя саму логику слайдов.",
                "specialists": build_stage07_specialists(),
                "card_layers": card_layers,
            },
        ],
    }


def main() -> int:
    data = build_data()
    payload = "window.PIPELINE_DASHBOARD_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    DATA_JS.write_text(payload, encoding="utf-8")
    print(DATA_JS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
