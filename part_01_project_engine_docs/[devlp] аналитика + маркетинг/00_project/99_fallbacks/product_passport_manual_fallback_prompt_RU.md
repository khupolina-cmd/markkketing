# Product Passport Без Skill

Если `product-passport-builder` не отображается в сессии, это не блокер.

Можно запустить ту же логику вручную в новом чате.

## Главное Правило

Не пытайся через один запрос собрать всё сразу:

- не рынок;
- не конкурентов;
- не отзывы;
- не контент карточки;
- не стратегию.

В этом чате нужен только `product_passport`.

То есть:

- факты о товаре;
- claims селлера;
- характеристики;
- база для цены и проверки по отзывам;
- всё неясное в `unclear`.

---

## Готовый Промпт Для Нового Чата

Скопируй это как первое сообщение:

````text
Собери готовый product passport из сырого ввода ниже.

Отвечай только по-русски.
Не анализируй стратегию.
Не критикуй карточку.
Не сравнивай с конкурентами.
Не описывай визуальный стиль.
Не придумывай отсутствующие факты.
Если что-то неясно, пиши unclear.
Текст со слайдов и инфографики считай claims карточки.

Верни ответ так:
1. Одна строка: Рекомендуемое имя файла: 01__{product_key}__product_passport.md
2. Потом один markdown-блок с готовым содержимым файла.
3. После блока ничего длинного не объясняй.

Используй именно такую структуру паспорта:

# Product Passport

Статус: паспорт товара для ранней матрицы.

Это слой фактов и текстовых обещаний селлера.

Не критика. Не стратегия. Не анализ отзывов. Не визуальная интерпретация.

```text
product_key:
product_role: hero / direct / indirect
marketplace:
product_url:
source: screenshot / copied_page_text / voice_notes / manual / mixed
source_refs:
snapshot_date:
```

## 1. Кто Продаёт И Что Это За Товар

```text
product_name:
brand:
seller:
category:
```

## 2. Описание Селлера

```text
seller_description_short:
seller_description_raw_fragments:
```

## 3. Текстовые Обещания Селлера

```text
seller_main_claim:
seller_secondary_claims:
image_text_claims:
declared_use_cases:
declared_target_buyer:
```

## 4. Характеристики

```text
volume_weight_count:
unit_basis: ml / g / kg / шт / dose / unclear
package_count:
size:
composition_or_material:
key_characteristics:
```

## 5. Цена И Единица Сравнения

```text
price_snapshot_ref:
unit_price_basis:
how_to_calculate_unit_price:
```

## 6. Claims, Которые Нужно Проверить По Отзывам

```text
claims_to_check_in_reviews:
possible_overpromises:
what_reviews_must_confirm:
```

## 7. Что Нельзя Понять Из Карточки

```text
missing_or_unclear:
needs_manual_check:
```

## 8. Куда Это Пойдёт Дальше

```text
feeds_price_value_snapshot:
feeds_contracts_matrix:
feeds_product_honesty_check:
```

Сырой ввод:
````

---

## Короткая Рабочая Форма

Вот форма, которую реально удобно заполнять.

Она уже заточена под наш pipeline и не тащит лишние слои.

```text
product_key:
product_role: hero / direct / indirect
marketplace:
product_url:
snapshot_date:

current_price:
old_price_if_visible:
volume_weight_count:
rating:
reviews_count:
purchases_count_if_visible:

product_name:
brand:
seller:
category:

copied_page_text:

image_claims_voice_notes:
- 
- 
- 

key_characteristics_if_visible:
- 
- 
- 

declared_use_cases_if_visible:
- 
- 

declared_target_buyer_if_visible:
- 
- 

composition_or_material_if_visible:

unclear_or_missing:
- 
- 
- 
```

---

## Что Не Надо Совать В Product Passport

Вот это пока не клади:

- разбор конкурентов;
- что людям нравится по отзывам;
- что людям не нравится по отзывам;
- боли и возражения;
- идеи для слайдов;
- фото для карточки;
- оффер;
- позиционирование;
- почему купят именно у нас;
- чем мы лучше рынка.

Это всё пойдёт позже в другие этапы.

---

## Минимум Для Старта

Если совсем нет сил, достаточно вот этого:

```text
product_key:
product_role:
marketplace:
current_price:
volume_weight_count:
rating:
reviews_count:
copied_page_text:
image_claims_voice_notes:
- 
- 
```

Этого уже хватит, чтобы собрать первый нормальный паспорт без красивостей.
