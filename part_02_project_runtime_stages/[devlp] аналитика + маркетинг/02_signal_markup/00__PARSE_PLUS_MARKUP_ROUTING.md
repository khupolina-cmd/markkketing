# Этап 2. Парсинг Плюс Разметка

Это один рабочий шаг.

Не так:

```text
pdf -> отдельно парсер -> отдельно разметка
```

А так:

```text
pdf -> сразу парсинг + разметка -> готовый файл этапа 02
```

---

## Что Лежит Где

### Выход

Актуальный набор готовых разметок для этого проекта лежит здесь:

- герой:
  [`02__hero_offscrub_hand_cream_226382131__signal_markup.md`](/Users/alittlepinkie/Documents/пайплайн%20(аналитика%20+%20маркетинг)/02_signal_markup/hero/hero_offscrub_hand_cream_226382131/02__hero_offscrub_hand_cream_226382131__signal_markup.md)
- прямые конкуренты:
  [`02__direct_the_act_virgin_hand_cream_65ml__signal_markup.md`](/Users/alittlepinkie/Documents/пайплайн%20(аналитика%20+%20маркетинг)/02_signal_markup/direct_competitors/direct_the_act_virgin_hand_cream_65ml/02__direct_the_act_virgin_hand_cream_65ml__signal_markup.md)
  [`02__direct_touchy_hand_cream_50ml__signal_markup.md`](/Users/alittlepinkie/Documents/пайплайн%20(аналитика%20+%20маркетинг)/02_signal_markup/direct_competitors/direct_touchy_hand_cream_50ml/02__direct_touchy_hand_cream_50ml__signal_markup.md)
- косвенные конкуренты:
  [`02__indirect_mixit_vanilla_hand_body_cream__signal_markup.md`](/Users/alittlepinkie/Documents/пайплайн%20(аналитика%20+%20маркетинг)/02_signal_markup/indirect_competitors/indirect_mixit_vanilla_hand_body_cream/02__indirect_mixit_vanilla_hand_body_cream__signal_markup.md)
  [`02__indirect_zeitun_samarkand_hand_body_lotion_200ml__signal_markup.md`](/Users/alittlepinkie/Documents/пайплайн%20(аналитика%20+%20маркетинг)/02_signal_markup/indirect_competitors/indirect_zeitun_samarkand_hand_body_lotion_200ml/02__indirect_zeitun_samarkand_hand_body_lotion_200ml__signal_markup.md)

### Правило На Сейчас

Разметки уже разложены по канонической структуре этапа `02_signal_markup`.

Следующий слой должен использовать именно эти `product_key`:

```text
hero_offscrub_hand_cream_226382131
direct_the_act_virgin_hand_cream_65ml
direct_touchy_hand_cream_50ml
indirect_mixit_vanilla_hand_body_cream
indirect_zeitun_samarkand_hand_body_lotion_200ml
```

Если позже будут приходить паспорта, их нужно класть уже под эти же ключи, а не создавать новые похожие имена.

Для ассортиментных карточек вроде `Zeitun`:

```text
карточечные рейтинг / число оценок / вопросы = общий фон доверия по линейке
не делим вручную на число вариантов
ароматические и variant-specific выводы = только по явно релевантным отзывам
```

---

## Главное Правило Маршрутизации

В описании запуска всегда должны быть прямо прописаны:

1. `product_key`
2. `role`
3. где лежит входной PDF
4. куда положить итоговый markdown-файл

Не надо зашивать это жёстко внутрь скилла.

Скилл общий.

Маршрут задаётся в конкретном запуске.

---

## Готовый Формат Задания

Если нужно сделать ещё одну разметку, копируешь этот шаблон и меняешь роль, ключ и пути:

```text
Задача: возьми PDF отзывов, сделай парсинг и сразу полную разметку сигналов.

Роль продукта: hero
Product key: hero_offscrub_hand_cream_226382131

Входной источник:
/Users/alittlepinkie/Documents/пайплайн (аналитика + маркетинг)/01_intake/raw_reviews/hero/hero_offscrub_hand_cream_226382131/sources/

Целевой выходной файл:
/Users/alittlepinkie/Documents/пайплайн (аналитика + маркетинг)/02_signal_markup/hero/hero_offscrub_hand_cream_226382131/02__hero_offscrub_hand_cream_226382131__signal_markup.md

Если при парсинге нужен промежуточный текстовый дамп, положи его сюда:
/Users/alittlepinkie/Documents/пайплайн (аналитика + маркетинг)/01_intake/raw_reviews/hero/hero_offscrub_hand_cream_226382131/00__hero_offscrub_hand_cream_226382131__raw_reviews.md

Важно:
- это один проход, а не два отдельных этапа;
- итоговый основной результат должен лежать именно в папке этапа 02;
- не клади итог разметки обратно во intake.
```

---

## Что Считать Основным Результатом

Основной результат этапа:

```text
02__{product_key}__signal_markup.md
```

Файл `00__{product_key}__raw_reviews.md` вторичен.

Он нужен только как архив рабочего текста, если вообще понадобился.

Можно работать и без него, если PDF сразу успешно превращается в готовую разметку.
