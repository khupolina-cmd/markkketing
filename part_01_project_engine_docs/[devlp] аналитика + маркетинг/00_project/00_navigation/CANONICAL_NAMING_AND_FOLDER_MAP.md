# Canonical Naming And Folder Map

Статус: главный стандарт нейминга и раскладки.

Цель: чтобы этап, папка, документ и шаблон назывались одинаково и не заставляли помнить историю проекта.

---

## 1. Главное Правило

```text
номер этапа = номер папки = номер главного выходного документа
```

Если этап называется `04 Matrix Conclusions`, то его главный документ начинается с `04__`.

Если этап называется `07 Card Layer`, то его главный документ начинается с `07__`.

Исключения допускаются только для внутренних подслоёв, например:

```text
03a__...__technical_matrix_draft.md
05a__...__card_critique.md
```

где буква показывает вспомогательный документ внутри этапа.

---

## 2. Канонические Рабочие Папки

```text
01_intake/
02_signal_markup/
03_contract_matrices/
04_matrix_conclusions/
05_strategy/
06_funnel/
07_card_layer/
08_qa/
99_archive/
```

`00_project/` не хранит результаты товара.

Там живут:

- маршрутизация;
- методы;
- роли;
- шаблоны;
- учебные примеры.

---

## 3. Канонический Маршрут

| Этап | Папка | Главный выход |
|---|---|---|
| `01 Intake` | `01_intake/` | `01__project__intake_map.md` |
| `01.5 Product Passports + Price` | `01_intake/` | `01__{product_key}__product_passport.md` + `01__project__price_value_snapshot.md` |
| `02 Signal Markup` | `02_signal_markup/` | `02__{product_key}__signal_markup.md` |
| `03 Contract Matrices` | `03_contract_matrices/` | `03__{product_key}__contracts_matrix.md` + `03__{hero_key}__master_contracts_matrix.md` |
| `03A Technical Draft` | `03_contract_matrices/` | `03a__{product_key}__technical_matrix_draft.md` |
| `04 Matrix Conclusions` | `04_matrix_conclusions/` | `04__{hero_key}__matrix_conclusions.md` |
| `05 Strategy Decision` | `05_strategy/` | `05__{hero_key}__strategy_decision.md` |
| `04 Input Card And Shelf Critiques` | `04_matrix_conclusions/card_and_shelf_critiques/` | `04_input__project__shelf_snapshot.md` + `04_input__{product_key}__card_critique.md` |
| `06 Funnel Architecture` | `06_funnel/` | `06__{hero_key}__funnel_architecture.md` |
| `07 Card Layer` | `07_card_layer/` | `07__{hero_key}__card_layer.md` |
| `08 QA` | `08_qa/` | позже |

---

## 4. Product Key

У товара должен быть один стабильный ключ:

```text
role_brand_product_volume
```

Примеры:

```text
hero_loreal_hand_cream_50ml
direct_nivea_hand_cream_75ml
indirect_body_oil_aroma_100ml
```

Правило:

- латиница;
- маленькие буквы;
- `_` вместо пробелов;
- роль продукта в начале.

---

## 5. Роли Продуктов В Папках

Внутри этапных папок используем одни и те же ветки:

```text
hero/
direct_competitors/
indirect_competitors/
_unclassified/
```

`_unclassified` разрешён только до этапа 3.

Перед матрицами роль продукта должна быть определена.

---

## 6. Где Что Лежит

### Паспорта

```text
01_intake/product_passports/{role}/{product_key}/01__{product_key}__product_passport.md
```

### Сырые Отзывы

```text
01_intake/raw_reviews/{role}/{product_key}/00__{product_key}__raw_reviews.md
01_intake/raw_reviews/{role}/{product_key}/sources/
```

`00__...__raw_reviews.md` — это рабочий текстовый вход для этапа разметки.

`sources/` — это место для PDF, выгрузок и других исходников отзывов.

Сырые материалы карточки кладём не сюда, а в:

```text
01_intake/product_passports/{role}/{product_key}/sources/
```

### Разметка

```text
02_signal_markup/{role}/{product_key}/02__{product_key}__signal_markup.md
```

### Матрицы

```text
03_contract_matrices/{role}/{product_key}/03a__{product_key}__technical_matrix_draft.md
03_contract_matrices/{role}/{product_key}/03__{product_key}__contracts_matrix.md
03_contract_matrices/hero/{hero_key}/03__{hero_key}__master_contracts_matrix.md
```

### Выводы По Матрице

```text
04_matrix_conclusions/hero/{hero_key}/04__{hero_key}__matrix_conclusions.md
```

### Стратегия

```text
05_strategy/hero/{hero_key}/05__{hero_key}__strategy_decision.md
```

### Критики Карточек И Выдачи Для Этапа 4

```text
04_matrix_conclusions/card_and_shelf_critiques/04_input__project__shelf_snapshot.md
04_matrix_conclusions/card_and_shelf_critiques/04_input__{product_key}__card_critique.md
```

Почему `04_input`:

```text
это не главный выход этапа 4,
а дополнительный человеческий слой восприятия рынка
```

### Воронка

```text
06_funnel/hero/{hero_key}/06__{hero_key}__funnel_architecture.md
```

### Слой Карточки

```text
07_card_layer/hero/{hero_key}/07__{hero_key}__card_layer.md
```

---

## 7. Что Считать Архивом

Если документ использует старую нумерацию вроде:

```text
07 Архитектура воронки
08 Copy Layer
07_copy/
04_market_context/
05__...__matrix_conclusions.md
```

то он считается архивным или историческим черновиком.

Активная логика берётся только из:

```text
02_routing/READY_PIPELINE_01_05_RU.md
02_routing/READY_PIPELINE_06_07_RU.md
03_roles/ACTIVE_TEAM_GROUPS_AND_ROUTING_RU.md
04_methods/STAGE_ISOLATION_AND_ANTI_BIAS_PROTOCOL.md
```

---

## 8. Проверка Перед Новым Прогоном

Перед запуском реального товара проверяем:

1. Есть ли `product_key` у каждого товара?
2. Лежит ли товар в правильной ветке: `hero`, `direct_competitors`, `indirect_competitors`?
3. Совпадает ли номер этапа с номером файла?
4. Нет ли главного результата этапа в чужой папке?
5. Не лежит ли поздняя критика карточки внутри ранней матрицы?
6. Не используется ли архивный маршрут вместо активного?

Если ответ где-то плохой, сначала чинится маршрутизация, потом запускается анализ.
