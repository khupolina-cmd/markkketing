# Technical Matrix Draft Template

Статус: внутренний сервисный шаблон этапа `03 Contract Matrices`.

Цель: собрать широкую, но уже очищенную от невозможного и дублей черновую матрицу до работы специалистов.

Важно:

```text
это ещё не рабочая матрица продукта
это технический слой ограничений
это технический слой сортировки
это не поиск продуктовой правды
отзывы здесь являются видимыми сигналами, а не источником истины
```

Подробный протокол сортировки:

```text
00_project/04_methods/TECHNICAL_LAYER_SORTING_AND_GAP_SCAN_RU.md
```

---

## Метаданные

```yaml
product_key:
role: hero | direct_competitor | indirect_competitor
source_docs:
  - signal_markup:
  - product_passport:
  - price_snapshot:
generated_by: technical_rules
stage: 03a_technical_matrix_draft
```

---

## Правила Слоя

Тут мы:

- не сужаем картину слишком рано;
- не интерпретируем глубоко;
- не выбираем стратегию;
- не решаем, что “это уже неважно для рынка”.
- не решаем, настоящий отзыв или нет.
- не превращаем "слабое подтверждение" в "выкинуть".

Тут мы только:

- убираем невозможное;
- убираем дубли;
- убираем явный абсурд или опасную чушь;
- прикрепляем factual-модификаторы, которые покупатель тоже увидит или легко считает.
- помечаем материал для маркетолога, креативной команды или специалиста.

---

## Таблица Кандидатов

| Candidate ID | Видимый минус / риск | Сценарий / ожидание / сравнение | Что рядом удерживает | Visible modifiers | Evidence IDs | Technical route | Technical tags | Почему |
|---|---|---|---|---|---|---|---|---|
| C1 |  |  |  |  |  | keep_as_core_material |  |  |
| C2 |  |  |  |  |  | keep_for_marketing |  |  |
| C3 |  |  |  |  |  | hold_for_specialist |  |  |
| C4 |  |  |  |  |  | drop_duplicate |  |  |

---

## Разрешённые Technical Route

```text
keep_as_core_material
keep_for_marketing
keep_for_creative
keep_as_risk
keep_as_parity_must_show
keep_as_difference
keep_as_fear
keep_as_claim_to_reframe
hold_for_specialist
drop_duplicate
drop_impossible
drop_absurd_or_illegal
```

`drop_no_evidence` больше не используем как грубое действие.

Если материал не подтверждён отзывами, но виден в карточке, составе, цене, объёме, рейтинге или у конкурентов, его надо не выбрасывать, а помечать:

```text
claim_visible_review_silent
weak_visible_trace
competitor_visible_only
composition_visible_needs_check
```

---

## Короткие Правила Чтения

### `keep_as_core_material`

Строка видимо возможна и должна дойти до специалиста.

### `keep_for_marketing`

Строка не обязана быть прямым claim, но может пригодиться маркетологу.

### `keep_for_creative`

Строка слабая как вывод, но может стать образом, языком, сценарием или крючком.

### `keep_as_risk`

Строка важна как риск восприятия.

### `keep_as_parity_must_show`

Это не уникальность, но покупатель ждёт это увидеть.

### `keep_as_difference`

Есть видимая разница между героем и конкурентом.

### `keep_as_fear`

Материал может включить страх или избегание риска.

### `keep_as_claim_to_reframe`

Прямой claim опасен или слабоподтверждён, но материал может жить в мягкой формулировке.

### `drop_duplicate`

Это дубль уже существующей строки.

### `drop_impossible`

Комбинация не может существовать одновременно или противоречит видимым данным карточки.

### `drop_absurd_or_illegal`

Явный абсурд, опасная медицинская/юридическая чушь или невозможное обещание.

### `hold_for_specialist`

Строка спорная, но видимо возможная.

Технический слой не должен её убивать.

Важно: это не отказ, а передача живой неопределённости специалисту.

---

## Что Передаётся Дальше

Специалистам уходит не весь сырой мусор, а только:

- все `keep_*`
- `hold_for_specialist`

Жёстко не уходит только:

- `drop_duplicate`
- `drop_impossible`
- `drop_absurd_or_illegal`

Именно из этого потом собирается:

```text
03__{product_key}__contracts_matrix.md
```
