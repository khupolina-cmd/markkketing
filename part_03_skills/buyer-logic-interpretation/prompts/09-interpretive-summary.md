# Промпт 09: Финальная итоговая сводка

## Назначение

Собрать результаты skill 2 в единую сводку.

## Входные данные

```text
weighted_signal_map: [из промпта 01]
counterweight_report: [из промпта 02]
promise_safety_map: [из промпта 03]
claim_conflict_report: [из промпта 04]
persona_profiles: [из промпта 05]
heuristic_bridges_map: [из промпта 06b]
contextual_severity_map: [из промпта 06]
buyer_deterrence_map: [из промпта 07]
perception_simulation: [из промпта 08]
final_signal_registry: [из skill 1]
stats: [из skill 1]
```

## Инструкция

### Шаг 1: Product Truth

Собрать:

- что можно ставить в ядро;
- что нельзя ставить в ядро;
- главный козырь товара;
- что нужно снимать или оговаривать.

### Шаг 2: Buyer Perception

Собрать:

- главный барьер покупки;
- какие линзы вскрыли скрытые барьеры;
- какие линзы открыли неожиданные углы подачи.

### Шаг 3: Shared Funnel Implications

Собрать один общий блок:

- `must-cover`
- `trust-repair zones`
- `angle opportunities`
- `seller-conflict notes`

### Шаг 4: Claim Conflict

Если конфликты есть — вывести предупреждения.

### Шаг 5: Creative Reserve

Собрать материал для следующей работы, но не готовые решения.

## Формат выхода

```text
=== INTERPRETIVE_SUMMARY ===

=== СЛОЙ A: PRODUCT TRUTH ===
...

=== СЛОЙ B: BUYER PERCEPTION ===
ГЛАВНЫЙ БАРЬЕР ПОКУПКИ:
...

КАКИЕ ЛИНЗЫ ВСКРЫЛИ СКРЫТЫЕ БАРЬЕРЫ:
- ...

КАКИЕ ЛИНЗЫ ОТКРЫЛИ УГЛЫ ПОДАЧИ:
- ...

=== SHARED_FUNNEL_IMPLICATIONS ===
MUST-COVER:
- ...

TRUST-REPAIR ZONES:
- ...

ANGLE OPPORTUNITIES:
- ...

SELLER-CONFLICT NOTES:
- ...

=== CLAIM_CONFLICT ===
...

=== CREATIVE RESERVE ===
...
```

## Анти-галлюцинаторные правила

1. Не превращать линзы в набор отдельных воронок
2. Не прятать critical-барьеры
3. Не выдавать skill 2 за готовую карточку
