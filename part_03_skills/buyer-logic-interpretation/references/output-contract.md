# Контракт выходных данных (output-contract)

## Назначение

Описание форматов всех выходных артефактов skill 2.

---

## 1. weighted_signal_map

Каждая уникальная тема с:

- базовой severity;
- reversibility;
- evidence_strength.

---

## 2. counterweight_report

Противовесный анализ по осям критериев.

Ключевые поля:

- ось;
- позитивы;
- негативы;
- баланс;
- max severity;
- вердикт;
- рекомендация.

---

## 3. promise_safety_map

Оценка безопасности каждого обещания производителя.

---

## 4. claim_conflict_report

Список конфликтов между обещаниями и данными.

---

## 5. persona_profiles

Наблюдаемые профили и диагностические линзы.

Формат:

```text
=== PERSONA_PROFILES ===
Всего линз: N

=== Профиль/линза: [название] ===
Класс: [observed / diagnostic]
...
```

---

## 6. heuristic_bridges_map

Мосты между самим сигналом и воспринимаемым выводом.

Формат:

```text
=== HEURISTIC_BRIDGES_MAP ===

Источник сигнала: [...]
Bridge type: [...]
Промежуточный вывод покупателя: [...]
Кому особенно релевантно: [...]
Сила моста: weak / moderate / strong
Основание: [...]
Что вскрывает: [...]
```

---

## 7. contextual_severity_map

Severity каждой темы для каждого профиля или линзы.

Формат:

```text
=== CONTEXTUAL_SEVERITY_MAP ===

Тема | Базовая | [Линза 1] | [Линза 2] | Bridge uplift | Обоснование повышений
```

---

## 8. buyer_deterrence_map

Общая карта барьеров покупки плюс карты по линзам.

---

## 9. perception_simulation

Что каждая линза вскрывает для общей подачи.

Формат:

```text
=== PERCEPTION_SIMULATION ===

=== Тип: [название] ===
Класс: [observed / diagnostic]

ЧТО ПРИВЛЕЧЁТ:
...

ЧТО ОСТАНОВИТ:
...

ЧТО ОН УВИДИТ ПЕРВЫМ:
...

КАКОЙ СКРЫТЫЙ БАРЬЕР ВСКРЫВАЕТ:
...

КАКОЙ УГОЛ ПОДАЧИ ОТКРЫВАЕТ:
...

ЧТО ЭТО ДОБАВЛЯЕТ В ОБЩУЮ ВОРОНКУ:
...

ДИАГНОСТИЧЕСКИЙ ВЕРДИКТ:
...
```

---

## 10. shared_funnel_implications

Итоги не про "разные воронки", а про одну общую воронку после стресс-теста линзами.

Формат:

```text
=== SHARED_FUNNEL_IMPLICATIONS ===

MUST-COVER:
- ...

TRUST-REPAIR ZONES:
- ...

ANGLE OPPORTUNITIES:
- ...

SELLER-CONFLICT NOTES:
- ...
```

---

## 11. creative_reserve

Материалы для дальнейшей работы.

---

## 12. interpretive_summary

Итоговая сводка по всем слоям, включая:

- Product Truth;
- Buyer Perception;
- Shared Funnel Implications;
- Claim Conflict;
- Creative Reserve.
