---
name: buyer-logic-interpretation
description: Use when the user already has a final signal registry and needs buyer-side interpretation rather than extraction. Best for product-truth checks, promise safety, heuristic bridges, diagnostic buyer lenses, deterrence mapping, and shared funnel implications without designing the final product card.
---

# Skill 2: buyer-logic-interpretation

## Назначение

Skill 2 принимает на вход `final_signal_registry` из первого слоя разметки и переводит карту сигналов в карту покупательских решений.

Skill **интерпретирует** сигналы, а не пересчитывает их заново.

Работа skill 2 — ответить на три вопроса:

1. **Что мы можем обещать?**  
   Слой A: `Product Truth`
2. **Как это увидят разные покупательские линзы?**  
   Слой B: `Buyer Perception`
3. **Что это меняет в одной общей воронке и в разрешённых углах подачи?**

Skill 2 не даёт финальных рекомендаций по карточке товара. Это задача skill 3.

---

## Два слоя

### Слой A: Product Truth — «что мы можем обещать?»

Работает с расхождением между обещаниями производителя и цифровым следом. Не решает вопрос «правда ли это», а решает «насколько рискованно это обещать».

**Выдаёт:**
- `weighted_signal_map`
- `counterweight_report`
- `promise_safety_map`
- `claim_conflict_report`

### Слой B: Buyer Perception — «как это увидят разные линзы?»

Работает с восприятием: что произойдёт в голове покупателя, когда он откроет отзывы.

Здесь нельзя делать вид, что существует один универсальный покупатель.

Но и нельзя превращать skill в генератор отдельных воронок под каждого.

Поэтому skill использует:

- `observed profiles` — реальные профили, поддержанные данными;
- `diagnostic lenses` — аналитические линзы, нужные для стресс-теста общей подачи;
- `heuristic bridges` — эвристические переходы вида `сигнал -> воспринимаемый вывод`.

**Выдаёт:**
- `persona_profiles`
- `heuristic_bridges_map`
- `contextual_severity_map`
- `buyer_deterrence_map`
- `perception_simulation`

### Финальный выход

- `shared_funnel_implications`
- `creative_reserve`
- `interpretive_summary`

---

## Когда использовать

- После завершения первого слоя разметки и получения `final_signal_registry`
- Когда нужно понять, что можно обещать и чего стоит опасаться
- Когда нужно стресс-тестировать одну общую воронку через разные покупательские линзы
- Когда нужно найти скрытые барьеры, скрытые эвристики и неожиданные углы подачи

---

## Вход

| Параметр | Источник | Обязательность |
|---|---|---|
| `final_signal_registry` | Первый слой разметки | Обязательно |
| `stats` | Первый слой разметки | Обязательно |
| `producer_claims` | Бриф / упаковка / карточка товара | Обязательно |
| `client_brief` | Заказчик | Опционально |

---

## Выход

| Артефакт | Слой | Описание |
|---|---|---|
| `weighted_signal_map` | A | Каждая тема с базовой severity, reversibility, evidence_strength |
| `counterweight_report` | A | По каждой оси: позитив, негатив, вердикт |
| `promise_safety_map` | A | По каждому обещанию производителя: вердикт безопасности |
| `claim_conflict_report` | A | Конфликты между обещаниями и данными |
| `persona_profiles` | B | Наблюдаемые профили и диагностические линзы |
| `heuristic_bridges_map` | B | Мосты между сигналом и воспринимаемым риском |
| `contextual_severity_map` | B | Severity каждой темы для каждого профиля или линзы |
| `buyer_deterrence_map` | B | Ранжированная карта барьеров покупки |
| `perception_simulation` | B | Что каждая линза вскрывает для общей подачи |
| `shared_funnel_implications` | Финал | Что обязано попасть в одну общую подачу |
| `creative_reserve` | Финал | Материалы для дальнейшей работы |
| `interpretive_summary` | Финал | Финальная сводка с главными выводами |

---

## Pipeline flow

```text
Вход: final_signal_registry + stats + producer_claims + client_brief
    ↓
=== СЛОЙ A: PRODUCT TRUTH ===
[01-weight-signals] → weighted_signal_map
    ↓
[02-counterweight-analysis] → counterweight_report
    ↓
[03-promise-safety] → promise_safety_map
    ↓
[04-claim-conflict] → claim_conflict_report
    ↓
=== СЛОЙ B: BUYER PERCEPTION ===
[05-persona-extraction] → persona_profiles
    ↓
[06b-heuristic-bridges] → heuristic_bridges_map
    ↓
[06-contextual-severity] → contextual_severity_map
    ↓
[07-deterrence-map] → buyer_deterrence_map
    ↓
[08-perception-simulation] → perception_simulation
    ↓
=== ФИНАЛ ===
[09-interpretive-summary] → shared_funnel_implications + creative_reserve + interpretive_summary
```

---

## Жёсткие запреты

1. Не придумывать сигналы. Работать только с тем, что пришло из skill 1.
2. Не менять категории. Skill 1 разметил — skill 2 не переразмечает.
3. Не делать вид, что один усреднённый покупатель описывает весь рынок.
4. Не превращать каждую линзу в отдельную готовую воронку.
5. Не скрывать `critical`. Один `critical` всплывает везде независимо от частоты.
6. Базовая severity не зависит от частоты.
7. Контекстная severity может только повышать базовую, не понижать `critical`.
8. Не строить эвристические мосты без опоры на данные или устойчивую рыночную эвристику.
9. Не давать финальных рекомендаций по карточке — это skill 3.
10. Не округлять эвристики до красивых цифр и не выдавать их за науку.

---

## Инварианты

- Уровня `noise` не существует. Если написали — это сигнал.
- Один `critical` негатив блокирует ось в `counterweight_report` независимо от количества позитивов.
- Всего линз: не меньше 2 и не больше 6.
- `Observed profiles` обычно должны занимать ≥5% массива.
- `Diagnostic lenses` могут быть ниже 5%, если они вскрывают полезный скрытый риск или угол подачи.
- Контекстная severity: только повышение.
- Base severity не отменяет эвристические усилители.
- На выходе должна усиливаться одна общая воронка, а не автоматически рождаться несколько разных.

---

## Ссылки

### References
- [Двухслойная модель](references/two-layer-model.md)
- [Базовая шкала severity](references/base-severity-scale.md)
- [Правила контекстной severity](references/contextual-severity-rules.md)
- [Правила противовеса](references/counterweight-rules.md)
- [Матрица безопасности обещаний](references/promise-safety-matrix.md)
- [Протокол CLAIM_CONFLICT](references/claim-conflict-protocol.md)
- [Правила извлечения персон](references/persona-extraction-rules.md)
- [Эвристические мосты](references/heuristic-bridges.md)
- [Формула deterrence_score](references/deterrence-scoring.md)
- [Гайд Creative Reserve](references/creative-reserve-guide.md)
- [Контракт выходных данных](references/output-contract.md)
- [Спорные случаи](references/edge-cases.md)

### Prompts
- [01 — Взвешивание сигналов](prompts/01-weight-signals.md)
- [02 — Противовесный анализ](prompts/02-counterweight-analysis.md)
- [03 — Безопасность обещаний](prompts/03-promise-safety.md)
- [04 — CLAIM_CONFLICT](prompts/04-claim-conflict.md)
- [05 — Извлечение профилей и линз](prompts/05-persona-extraction.md)
- [06b — Эвристические мосты](prompts/06b-heuristic-bridges.md)
- [06 — Контекстная severity](prompts/06-contextual-severity.md)
- [07 — Карта отпугивания](prompts/07-deterrence-map.md)
- [08 — Симуляция восприятия](prompts/08-perception-simulation.md)
- [09 — Итоговая сводка](prompts/09-interpretive-summary.md)
