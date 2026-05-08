# Product Folder Routing

Статус: правило раскладки товаров по папкам.

Цель: чтобы герой, прямые и косвенные конкуренты не смешивались, но каждый товар оставался цельным маленьким объектом.

---

## 1. Главное Решение

Не складываем все товары в одну общую кучу до разметки.

Сразу раскладываем по роли:

```text
hero
direct_competitors
indirect_competitors
```

Но внутри каждой роли создаём отдельную папку продукта:

```text
brand_product_key
```

Почему так:

- человеку проще видеть, где герой, где прямые, где косвенные;
- ИИ проще понимать роль продукта;
- все документы одного продукта лежат рядом;
- если роль изменилась, переносим одну папку, а не ловим файлы по всему проекту.

---

## 2. Product Key

У каждого товара должен быть один стабильный `product_key`.

Пример:

```text
hero_loreal_hand_cream_50ml
direct_nivea_hand_cream_75ml
indirect_body_oil_aroma_100ml
```

Правило:

```text
role + brand + short_product_name + volume_if_useful
```

Писать латиницей, маленькими буквами, через `_`.

---

## 3. Паспорта Товаров

Папка:

```text
01_intake/product_passports/
```

Структура:

```text
01_intake/product_passports/
  00__product_index.md
  hero/
    hero_brand_product_key/
      sources/
      01__hero_brand_product_key__product_passport_INPUT.md
      01__hero_brand_product_key__product_passport.md
  direct_competitors/
    direct_brand_product_key/
      sources/
      01__direct_brand_product_key__product_passport_INPUT.md
      01__direct_brand_product_key__product_passport.md
  indirect_competitors/
    indirect_brand_product_key/
      sources/
      01__indirect_brand_product_key__product_passport_INPUT.md
      01__indirect_brand_product_key__product_passport.md
  _unclassified/
```

`sources/` можно использовать для:

- скриншотов;
- скопированного текста;
- голосовых заметок, если они сохранены файлом;
- любых сырых материалов карточки.

---

## 3.1. Сырые Отзывы

Папка:

```text
01_intake/raw_reviews/
```

Структура:

```text
01_intake/raw_reviews/
  hero/
    hero_brand_product_key/
      sources/
      00__hero_brand_product_key__raw_reviews.md
  direct_competitors/
    direct_brand_product_key/
      sources/
      00__direct_brand_product_key__raw_reviews.md
  indirect_competitors/
    indirect_brand_product_key/
      sources/
      00__indirect_brand_product_key__raw_reviews.md
  _unclassified/
```

В `sources/` кладём PDF, выгрузки и исходные файлы отзывов.

В `00__...__raw_reviews.md` кладём уже собранный рабочий текст отзывов для разметки.

Не кладём туда критику карточки, скриншоты обещаний и заметки по выдаче.

Для карточки есть `sources/` внутри паспорта товара.

---

## 4. Когда Использовать `_unclassified`

Только если на входе реально непонятно:

```text
прямой это конкурент или косвенный?
```

Но это временная папка.

Перед этапом 3 продукт должен быть перенесён в:

```text
direct_competitors
```

или:

```text
indirect_competitors
```

Иначе ветвление после разметки будет мутным.

---

## 5. Разметка Отзывов

Разметку складываем по той же логике, с тем же `product_key`:

```text
02_signal_markup/
  hero/
    hero_brand_product_key/
      02__hero_brand_product_key__signal_markup.md
  direct_competitors/
    direct_brand_product_key/
      02__direct_brand_product_key__signal_markup.md
  indirect_competitors/
    indirect_brand_product_key/
      02__indirect_brand_product_key__signal_markup.md
```

Так паспорт и разметка товара всегда связываются по одному ключу.

---

## 6. Снимок Цен

Цены не живут внутри отдельных папок как главный источник.

Они собираются в общий файл:

```text
01_intake/01__project__price_value_snapshot.md
```

Почему:

цены нужны для сравнения, а сравнение удобнее видеть одной таблицей.

Но каждая строка таблицы должна ссылаться на:

```text
product_key
```

и на паспорт товара.

---

## 7. Матрицы Контрактов

После signal markup у каждого товара появляется своя локальная матрица контрактов.

Папка:

```text
03_contract_matrices/
```

Структура:

```text
03_contract_matrices/
  hero/
    hero_brand_product_key/
      03a__hero_brand_product_key__technical_matrix_draft.md
      03__hero_brand_product_key__contracts_matrix.md
      03__hero_brand_product_key__master_contracts_matrix.md
  direct_competitors/
    direct_brand_product_key/
      03a__direct_brand_product_key__technical_matrix_draft.md
      03__direct_brand_product_key__contracts_matrix.md
  indirect_competitors/
    indirect_brand_product_key/
      03a__indirect_brand_product_key__technical_matrix_draft.md
      03__indirect_brand_product_key__contracts_matrix.md
```

Правило:

- у героя есть локальная матрица;
- у каждого прямого конкурента есть локальная матрица в его личной папке;
- у каждого косвенного конкурента есть локальная матрица в его личной папке;
- итоговая мастер-матрица тоже живёт в папке героя, потому что именно герой идёт дальше в стратегию.

Почему так:

- матрицы конкурентов не теряются в общей куче;
- по каждому продукту рядом лежат паспорт, разметка и его контрактная логика;
- мастер-матрица героя не висит отдельно от героя.

Цена решения:

- появляется ещё одна папка этапа;
- зато исчезает путаница "где локальный документ продукта, а где сводка".

---

## 8. Выводы По Матрице

Папка:

```text
04_matrix_conclusions/
```

Структура:

```text
04_matrix_conclusions/
  hero/
    hero_brand_product_key/
      04__hero_brand_product_key__matrix_conclusions.md
```

Почему отдельно от стратегии:

```text
этап 4 ещё не выбирает стратегию
он только разделяет факты и интерпретации
```

---

## 9. Стратегия

Папка:

```text
05_strategy/
```

Структура:

```text
05_strategy/
  hero/
    hero_brand_product_key/
      05__hero_brand_product_key__strategy_decision.md
```

Критика карточек и выдачи теперь лежит не здесь, а как вход этапа 4:

```text
04_matrix_conclusions/card_and_shelf_critiques/
  04_input__project__shelf_snapshot.md
  04_input__hero_brand_product_key__card_critique.md
```

---

## 10. Воронка И Слой Карточки

```text
06_funnel/
  hero/
    hero_brand_product_key/
      06__hero_brand_product_key__funnel_architecture.md

07_card_layer/
  hero/
    hero_brand_product_key/
      07__hero_brand_product_key__card_layer.md
```

---

## 11. Если Роль Товара Меняется

Например, косвенный конкурент оказался прямым.

Действие:

1. Перенести папку продукта из `indirect_competitors` в `direct_competitors`.
2. Обновить `product_role` в паспорте.
3. Обновить строку в `00__product_index.md`.
4. Обновить роль в `price_value_snapshot`.

Не создавать новый паспорт заново.

---

## 12. Главное Правило

```text
роль продукта задаёт ветку
product_key связывает все документы
папка товара держит всё, что относится к одному продукту
```
