# 00 Project: Навигация

Эта папка хранит не рабочие результаты по товару, а управляющую логику проекта:

- фокус системы;
- маршрутизацию;
- роли специалистов;
- методы;
- учебные примеры;
- запасные варианты.

Рабочие артефакты товара должны лежать в этапных папках проекта:

```text
01_intake
02_signal_markup
03_contract_matrices
04_matrix_conclusions
05_strategy
06_funnel
07_card_layer
08_qa
99_archive
```

---

## 00_navigation

Для понимания, что такое папка, этап, специалист, скилл и документ.

- `00_navigation/PROJECT_OBJECTS.md`
- `00_navigation/PRODUCT_FOLDER_ROUTING.md`
- `00_navigation/CANONICAL_NAMING_AND_FOLDER_MAP.md`

---

## 01_core_focus

Главный фокус системы.

Читать первым.

- `01_core_focus/CORE_FOCUS_REVIEW_READER.md`

Коротко:

```text
мы не ищем объективную правду о продукте
мы анализируем, что покупатель увидит в отзывах и где он отвалится
```

---

## 02_routing

Маршруты пайплайна.

- `02_routing/MASTER_ROUTING.md`
- `02_routing/FULL_MARKUP_BRANCHING_PIPELINE.md`
- `02_routing/READY_PIPELINE_01_05_RU.md`
- `02_routing/READY_PIPELINE_06_07_RU.md`
- `02_routing/PIPELINE_TO_STAGE_4_DECISION_SCHEMA_RU.md`

Активная маршрутизация:

```text
02_routing/READY_PIPELINE_01_05_RU.md
02_routing/READY_PIPELINE_06_07_RU.md
```

Активное правило изоляции:

```text
04_methods/STAGE_ISOLATION_AND_ANTI_BIAS_PROTOCOL.md
```

`MASTER_ROUTING.md`, `FULL_MARKUP_BRANCHING_PIPELINE.md` и `PIPELINE_TO_STAGE_4_DECISION_SCHEMA_RU.md` сейчас считать архивом мыслей.

Они полезны как история проектирования, но не как источник активного маршрута.

Сейчас основной маршрут:

```text
паспорта товаров и снимок цен
полная разметка всех продуктов
локальные матрицы героя и конкурентов
мастер-матрица героя с подтверждением от конкурентов
выводы по матрице
выбор стратегии
архитектура воронки
слой карточки: copy + visual task
```

Критика выдачи и карточек не входит в техническую матрицу и мастер-матрицу.

Она может быть передана на этап 4 как человеческий слой восприятия рынка:

```text
04_matrix_conclusions/card_and_shelf_critiques/
```

---

## 03_roles

Специалисты, их функции и компетенции.

- `03_roles/AGENCY_TEAM_MODEL_RU.md`
- `03_roles/ACTIVE_TEAM_GROUPS_AND_ROUTING_RU.md`
- `03_roles/ROLE_NAMES_RU.md`
- `03_roles/SPECIALISTS_AND_TOOLKITS.md`
- `03_roles/SPECIALIST_COMPETENCY_MAP.md`
- `03_roles/SPECIALIST_ROSTER.md`
- `03_roles/SPECIALIST_INVOCATION_AND_TRAINING_MODEL.md`
- `03_roles/ACTIVE_TOOLKIT_FORMAT_RU.md`
- `03_roles/ACTIVE_SPECIALIST_PROFILE_TEMPLATE_RU.md`
- `03_roles/FULL_PIPELINE_TOOLKIT_MAP_RU.md`
- `03_roles/ACTIVE_USER_MODIFIER_LONG_TEMPLATE_RU.md`

Текущая логика:

```text
оставляем только реальные решающие роли
не плодим отдельного специалиста на каждую задачу
не держим отдельного специалиста по честности
```

Рабочие документы сейчас:

```text
03_roles/ACTIVE_TEAM_GROUPS_AND_ROUTING_RU.md
03_roles/SPECIALIST_INVOCATION_AND_TRAINING_MODEL.md
03_roles/ACTIVE_TOOLKIT_FORMAT_RU.md
03_roles/ACTIVE_SPECIALIST_PROFILE_TEMPLATE_RU.md
03_roles/FULL_PIPELINE_TOOLKIT_MAP_RU.md
03_roles/ACTIVE_USER_MODIFIER_LONG_TEMPLATE_RU.md
```

Остальные role-docs пока считать расширенными заготовками и архивом мыслей, а не главным маршрутом.

---

## 04_methods

Методы сборки конкретных артефактов.

- `04_methods/DIAGNOSTIC_MATRIX_METHOD.md`
- `04_methods/CHOICE_CONTEXT_METHOD.md`
- `04_methods/PRODUCT_FACTS_PRICE_AND_DEFERRED_CARD_CRITIQUE_METHOD.md`
- `04_methods/TECHNICAL_LAYER_SORTING_AND_GAP_SCAN_RU.md`
- `04_methods/STRATEGY_SELECTION_WITH_STYLE_MATRIX_METHOD.md`
- `04_methods/STAGE_ISOLATION_AND_ANTI_BIAS_PROTOCOL.md`

---

## 05_examples

Учебные примеры для проверки логики.

- `05_examples/TOY_EXAMPLE_POTATO.md`
- `05_examples/TOY_POTATO_PIPELINE_TO_STAGE_4.md`
- `05_examples/TOY_POTATO_03A_TECHNICAL_DRAFT.md`
- `05_examples/TOY_POTATO_FULL_RUN_01_05.md`
- `05_examples/NEXT_BLIND_TEST_RUN_PROTOCOL.md`
- `05_examples/TOY_POTATO_ROLE_RUN_03_05.md`

---

## 06_templates

Шаблоны рабочих документов.

- `06_templates/01__product_key__product_passport_TEMPLATE.md`
- `06_templates/01__product_key__product_passport_INPUT_TEMPLATE.md`
- `06_templates/01__project__price_value_snapshot_TEMPLATE.md`
- `06_templates/03a__product_key__technical_matrix_draft_TEMPLATE.md`
- `06_templates/03__product_key__contracts_matrix_TEMPLATE.md`
- `06_templates/04__product_key__matrix_conclusions_TEMPLATE.md`
- `06_templates/05__product_key__strategy_decision_TEMPLATE.md`
- `06_templates/05a__project__shelf_snapshot_TEMPLATE.md`
- `06_templates/05a__product_key__card_critique_TEMPLATE.md`
- `06_templates/06__product_key__funnel_architecture_TEMPLATE.md`
- `06_templates/07__product_key__card_layer_TEMPLATE.md`

Шаблон `05__...` нужен для выбора стратегии.

Шаблоны `05a__...` больше не означают отдельный этап.

Они описывают человеческий слой критики карточек и выдачи, который можно передать как дополнительный вход в `04 Matrix conclusions`.

---

## 99_fallbacks

Запасные методы, которые не являются текущим основным маршрутом.

- `99_fallbacks/COMPETITOR_COMPRESSION_METHOD.md`

---

## Важное Правило

Пока мы не решили, что станет отдельным скиллом, а что останется инструкцией проекта, реальные рабочие файлы не мигрируем массово.

Сначала стабилизируем:

1. фокус;
2. маршрут;
3. роли;
4. метод матрицы;
5. пример на картошке;
6. нейминг и папки.

Потом переносим рабочие артефакты.
