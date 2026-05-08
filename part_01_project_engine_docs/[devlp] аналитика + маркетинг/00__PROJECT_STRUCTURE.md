# Project Structure

Статус: короткая карта рабочей папки.

Главный стандарт нейминга:

```text
00_project/00_navigation/CANONICAL_NAMING_AND_FOLDER_MAP.md
```

---

## Рабочий Корень

```text
00_project/                  инструкции, роли, методы, шаблоны
01_intake/                   входы: сырые отзывы, паспорта, цены
02_signal_markup/            разметка отзывов
03_contract_matrices/        технические черновики и матрицы контрактов
04_matrix_conclusions/       выводы по мастер-матрице
05_strategy/                 выбор стратегии
06_funnel/                   архитектура воронки
07_card_layer/               слой карточки: copy + visual task
08_qa/                       проверки
99_archive/                  старые версии и неактивные маршруты
```

---

## Главное Правило

```text
номер папки = номер этапа = номер главного результата
```

Примеры:

```text
04_matrix_conclusions/.../04__...__matrix_conclusions.md
05_strategy/.../05__...__strategy_decision.md
07_card_layer/.../07__...__card_layer.md
```

---

## Где Старое

Старые папки `герой`, `прямые`, `косвенные`, `03_hero_diagnosis`, `04_market_context`, `07_copy` перенесены в:

```text
99_archive/old_versions/pre_canonical_root_folders/
```

Они сохранены как история, но не являются активным маршрутом.
