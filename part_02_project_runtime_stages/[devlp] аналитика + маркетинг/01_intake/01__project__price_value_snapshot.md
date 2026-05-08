# Price Value Snapshot

Статус: рабочая сводка этапа `01_intake`.

Цель файла:

- собрать в одном месте цену, объём и цену за единицу;
- зафиксировать карточечный фон доверия перед этапом `03`;
- не придумывать точность там, где карточка или выгрузка дают только частично читаемые данные.

## Правило Чтения

- `price`, `volume` и `unit_price` используем как рабочую базу для сравнения.
- `rating`, `evaluations_count` и `questions_count` читаем как карточечные метрики доверия, а не как финальную истину о качестве SKU.
- если карточка объединяет несколько вариантов линейки, карточечные метрики считаем общими для линейки и не делим вручную на число ароматов или артикулов.
- если цифра в PDF-разметке повреждена или обрезана, фиксируем только ту часть, в которой уверены, а остальное помечаем как `unclear`.

## Snapshot Table

| product_key | role | product_label | price | volume | unit_price_basis | unit_price | rating | evaluations_count | questions_count | status_note |
|---|---|---|---|---|---|---|---|---|---|---|
| `hero_offscrub_hand_cream_226382131` | hero | Off.Scrub, крем для рук, 75 мл | 364 руб | 75 мл | 1 мл | 4,85 руб/мл | 4,8 | 622 | unclear | карточечная метрика восстановлена из signal markup; достаточно для рабочего сравнения |
| `direct_the_act_virgin_hand_cream_65ml` | direct_competitor | The Act Virgin, крем для рук, 65 мл | 507 руб | 65 мл | 1 мл | 7,80 руб/мл | 4,9 | 4 920 | unclear | карточечная метрика восстановлена из signal markup; годится как рабочий рыночный ориентир |
| `direct_touchy_hand_cream_50ml` | direct_competitor | Touchy, крем для рук, 50 мл | 488 руб | 50 мл | 1 мл | 9,76 руб/мл | 4,7 | 1 572 | unclear | карточечная метрика восстановлена из signal markup; карточка читается достаточно стабильно |
| `indirect_mixit_vanilla_hand_body_cream` | indirect_competitor | MIXIT Vanilla, крем для рук и тела, 250 мл | 631 руб | 250 мл | 1 мл | 2,52 руб/мл | 4,8 | unclear | unclear | рейтинг читается фрагментарно из signal markup; число оценок в выгрузке повреждено, поэтому не фиксируем точно |
| `indirect_zeitun_samarkand_hand_body_lotion_200ml` | indirect_competitor | Zeitun Samarkand, лосьон для рук и тела, 200 мл | 462 руб | 200 мл | 1 мл | 2,31 руб/мл | unclear | 966 | unclear | карточка ассортиментная; 966 оценок относятся к общей карточке линейки, а не только к аромату Самарканд |

## Быстрый Порядок По Цене За 1 Мл

От более дешёвого к более дорогому:

1. `indirect_zeitun_samarkand_hand_body_lotion_200ml` — 2,31 руб/мл
2. `indirect_mixit_vanilla_hand_body_cream` — 2,52 руб/мл
3. `hero_offscrub_hand_cream_226382131` — 4,85 руб/мл
4. `direct_the_act_virgin_hand_cream_65ml` — 7,80 руб/мл
5. `direct_touchy_hand_cream_50ml` — 9,76 руб/мл

## Что Это Уже Даёт Для Следующего Этапа

- герой не самый дешёвый, но и не премиум-экстремум по цене за мл;
- прямые конкуренты заметно дороже героя по цене за мл;
- косвенные конкуренты дают более дешёвый объёмный уходовой фон;
- для этапа `03a` уже можно оценивать, какие минусы рынок терпит при каком ценовом контексте.

## Что Ещё Можно Добрать Позже, Но Это Не Блокер

- `questions_count` для всех карточек;
- точное `evaluations_count` для `indirect_mixit_vanilla_hand_body_cream`;
- точное `rating` для `indirect_zeitun_samarkand_hand_body_lotion_200ml`;
- `marketplace` и `product_url`, если захочется довести intake до совсем аккуратного состояния.

## Source Anchors

- `hero_offscrub_hand_cream_226382131`: product passport + signal markup
- `direct_the_act_virgin_hand_cream_65ml`: product passport + signal markup
- `direct_touchy_hand_cream_50ml`: product passport + signal markup
- `indirect_mixit_vanilla_hand_body_cream`: product passport + signal markup
- `indirect_zeitun_samarkand_hand_body_lotion_200ml`: product passport + signal markup + ручная пометка по общей ассортиментной карточке
