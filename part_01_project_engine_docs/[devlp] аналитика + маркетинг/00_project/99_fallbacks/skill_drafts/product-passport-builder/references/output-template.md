# Шаблон Готового Product Passport

Используй именно эти имена полей в финальном паспорте.

Верни готовое содержимое файла в markdown.

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

Поведение полей:

- держи `source` честным: если паспорт собран и из копипасты, и из голосовых заметок, используй `mixed`
- держи `seller_description_raw_fragments` как можно ближе к исходной формулировке
- используй `image_text_claims` только для текстовых обещаний со слайдов или инфографики
- используй `unclear`, а не догадку
- не добавляй новые секции
