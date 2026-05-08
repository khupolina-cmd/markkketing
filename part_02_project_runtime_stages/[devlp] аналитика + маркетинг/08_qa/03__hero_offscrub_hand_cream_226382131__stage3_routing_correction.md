# Stage 3 Routing Correction

product_key: hero_offscrub_hand_cream_226382131
date: 2026-04-21
status: corrected_with_specialist_rebuild
related_core_focus_audit: 08_qa/03__hero_offscrub_hand_cream_226382131__core_focus_audit.md

## Что Было Не Так

В прогоне смешались два разных слоя:

1. `03A` технический AI-черновик.
2. `03B-03C` специалистская сборка локальных матриц и мастер-матрицы.

По задумке проекта `03A` должен быть только техническим слоем:

- широкая сборка кандидатов;
- дедупликация;
- отсев невозможного;
- привязка к evidence;
- factual modifiers.

Он не должен сам делать мастер-матрицу.

## Правильная Архитектура

```text
02 signal markup
  ↓
03A technical matrix drafts
  ↓
03B local specialist matrices
  ↓
03C hero master matrix
  ↓
04 matrix conclusions
```

## Кто Должен Работать На 3B-3C

### Owner

`Маркетплейс-стратег / категорийный стратег`

Он отвечает за:

- категорийную норму;
- безопасное покупательское чтение на фоне конкурентов;
- границу переноса с косвенных конкурентов;
- отсечение строк, которые не держатся рынком;
- мастер-матрицу как общий знаменатель.

### Input

`Поведенческий стратег`

Он отвечает за:

- кому минус стоп;
- когда минус терпим;
- что удерживает покупку;
- где сценарий меняет чтение риска.

## Какие Чемоданчики Обязательны

Перед пересборкой нужно открыть:

```text
00_project/03_roles/specialists/strategy_group/marketplace_strategist.md
00_project/03_roles/toolkits/marketplace_strategist/default_tools.md
00_project/03_roles/toolkits/marketplace_strategist/user_modifiers.md
00_project/03_roles/specialists/strategy_group/behavioral_strategist.md
00_project/03_roles/toolkits/behavioral_strategist/default_tools.md
00_project/03_roles/toolkits/behavioral_strategist/user_modifiers.md
```

## Что Делать С Уже Созданными Файлами

Текущие локальные матрицы и мастер-матрица не удаляются.

Они помечены как:

```text
provisional_needs_specialist_review
invalid_until_specialist_rebuild
```

Их можно использовать как рабочий материал, но нельзя считать утверждённым этапом `03`.

## Почему Это Важно

Если мастер-матрицу делает технический слой, он неизбежно начинает играть в маркетолога:

- слишком рано отклоняет сценарии;
- смешивает физическое ограничение продукта с потенциальным углом;
- переносит или запрещает идеи без специалистской проверки.

Пример ошибки:

```text
body-SPA / дозатор / большой объём
```

и

```text
travel / сумка / ручная кладь / 75 мл
```

были слишком близко прочитаны как одна зона.

Правильно: body-SPA отклонять как обещание героя, но travel-сценарий держать отдельно и проверять через специалистский слой.

Дополнительная поправка после core-focus аудита:

```text
travel / сумка / до 100 мл
```

не должен лежать в `hold`, если линия живая для восприятия.

Текущий правильный статус:

```text
angle_candidate
```

## Решение

Перед этапом `04` нужно было пересобрать:

1. локальные рабочие матрицы через `3B`;
2. мастер-матрицу героя через `3C`;
3. только потом делать выводы по матрице.

## Выполнено

Пересборка выполнена.

Обновлены файлы:

- `03_contract_matrices/hero/hero_offscrub_hand_cream_226382131/03__hero_offscrub_hand_cream_226382131__contracts_matrix.md`
- `03_contract_matrices/direct_competitors/direct_the_act_virgin_hand_cream_65ml/03__direct_the_act_virgin_hand_cream_65ml__contracts_matrix.md`
- `03_contract_matrices/direct_competitors/direct_touchy_hand_cream_50ml/03__direct_touchy_hand_cream_50ml__contracts_matrix.md`
- `03_contract_matrices/indirect_competitors/indirect_mixit_vanilla_hand_body_cream/03__indirect_mixit_vanilla_hand_body_cream__contracts_matrix.md`
- `03_contract_matrices/indirect_competitors/indirect_zeitun_samarkand_hand_body_lotion_200ml/03__indirect_zeitun_samarkand_hand_body_lotion_200ml__contracts_matrix.md`
- `03_contract_matrices/hero/hero_offscrub_hand_cream_226382131/03__hero_offscrub_hand_cream_226382131__master_contracts_matrix.md`

Текущий статус:

```text
03B local matrices: specialist_reviewed_3B
03C master matrix: specialist_reviewed_3C
```
