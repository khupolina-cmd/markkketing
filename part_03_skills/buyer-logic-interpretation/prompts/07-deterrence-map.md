# Промпт 07: Карта отпугивания

## Назначение

Построить общую карту барьеров покупки и карты по линзам.

## Входные данные

```text
contextual_severity_map: [из промпта 06]
heuristic_bridges_map: [из промпта 06b]
final_signal_registry: [из skill 1 — ожидания и сомнения]
stats: [из skill 1]
weighted_signal_map: [из промпта 01]
```

## Инструкция

### Шаг 1: Определить amplifiers

Проверить для каждой темы:

- `expectation_violated`
- `doubt_confirmed`

### Шаг 2: Учесть bridge multiplier

- нет моста -> `1.0`
- weak -> `1.1`
- moderate -> `1.25`
- strong -> `1.5`

### Шаг 3: Рассчитать score

Общая карта:

`deterrence_score = severity_weight × frequency_factor × amplifier × bridge_multiplier`

Карты по линзам:

`deterrence_score_lens = contextual_severity_weight × frequency_factor × amplifier × bridge_multiplier`

## Формат выхода

```text
=== BUYER_DETERRENCE_MAP ===

Общая карта:
# | Тема | N | % | Severity | Amplifiers | Bridges | Score | Вердикт

Карта по линзе:
# | Тема | Баз. severity | Контекст. severity | Bridges | Score | Δ vs общая | Вердикт
```

## Анти-галлюцинаторные правила

1. Не ставить amplifier без подтверждения в данных
2. Не игнорировать сильный bridge
3. Не выдавать score за процент потери продаж
4. Не опускать critical-темы, даже если они редкие
