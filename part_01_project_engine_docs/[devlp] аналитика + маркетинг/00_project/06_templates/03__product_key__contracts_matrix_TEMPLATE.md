# Template: Stage 3 Contracts Matrix

Используется и для локальной матрицы продукта, и для мастер-матрицы героя.

Главное правило:

```text
это не технический AI-черновик
это специалистская рабочая матрица после 03a
это слой покупательского восприятия, а не суд над продуктовой правдой
отзывы здесь читаются как видимые социальные сигналы, а не истина
большая часть материала передаётся маркетологу / креативной команде с ярлыком, а не выбрасывается
не писать длинную аналитику рядом
не заводить лишние колонки заранее
не превращать матрицу в стратегию
```

---

## 1. Шапка

```text
product_key:
product_role:
product_name:
matrix_type: local | master
generated_by: specialist_review
owner:
specialist_inputs:
based_on_signal_markup:
based_on_product_passport:
based_on_price_snapshot:
based_on_technical_draft:
toolkits_used:
```

---

## 2. Матрица

| Контракт / сценарий | Видимый минус / риск | Кому стоп | Когда терпимо | Что удерживает покупку | Цена / контекст | Риск / переформулировка claim | Evidence IDs | Статус / маршрут |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
| | | | | | | | | |

Важно:

```text
Evidence IDs = где это видно в материале
Evidence IDs не означают "это доказано"
```

---

## 3. Короткие Выводы

```text
perception_ready_contracts:
stop_factors:
tolerable_negatives:
claim_reframe_material:
difference_material:
parity_must_show:
fear_material:
composition_material:
what_to_carry_forward:
hard_drops_only:
```

---

## 4. Для Мастер-Матрицы Героя

Если `matrix_type: master`, добавить короткую строку происхождения внутри ячейки или после таблицы:

```text
draft_from_hero
confirmed_by_direct
enriched_by_indirect
weakened_by_market
visible_delta
parity_but_must_show
claim_to_reframe
risk_material
composition_material
angle_candidate
hold
hard_reject
```

Читать статусы так:

```text
confirmed_by_direct = безопасное/знакомое покупательское чтение, не лабораторное доказательство
angle_candidate = перспективный угол, который можно передать дальше как гипотезу восприятия
hold = парковка, а не отказ
claim_to_reframe = нельзя тащить в лоб, но можно передать как материал для мягкой формулировки
parity_but_must_show = не уникальность, но это важно показать как норму категории
visible_delta = видимая разница с конкурентами, без выбора победителя
risk_material = материал важен как страх / стоп / риск ожидания
composition_material = состав может быть полезным материалом, но требует точечной проверки
hard_reject = жёстко убрать только дубль / невозможное / абсурд / опасную чушь
```
