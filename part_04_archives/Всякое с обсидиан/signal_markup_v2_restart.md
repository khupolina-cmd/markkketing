# Signal Markup V2 Restart

## Что сломано в старом контуре

Старый контур стабильно давал плохой результат не потому, что “модель тупит”, а потому что центр системы был выбран неправильно.

Главная ошибка:

- первичным артефактом сделали `signals_registry`

Из-за этого модель каждый раз оптимизировалась под:

- сбор строк;
- техничный список;
- код сигнала;
- package output;

А не под:

- чтение человеком;
- проверку глазами;
- удобный батч на следующие товары.

## Правильный центр системы

Первичный артефакт должен быть таким:

`raw export -> normalized numbered reviews -> inline colored signal dashboard -> final stats`

То есть сначала человек читает нормализованные отзывы и видит, где именно какие сигналы выделены.

Только потом можно делать sidecar-реестры и машинные форматы.

## Минимальная рабочая версия

Если резать до основы, система обязана делать только 4 вещи:

1. вытащить отзывы из сырого массива;
2. присвоить каждому отзыву стабильный id;
3. разметить сигналы по 6 категориям прямо рядом с отзывом;
4. в конце посчитать статистику по уникальным review ids.

Этого уже достаточно, чтобы:

- читать результат;
- валидировать разметку;
- батчить на другие товары.

## Что нельзя терять

- отзыв можно переиспользовать много раз;
- сигнал нельзя переиспользовать дважды;
- один сигнал = одна категория;
- правила категорий должны читаться до разметки;
- пустая похвала не должна захламлять статистику;
- спорное должно честно уходить в manual.

## Новый базовый выход

Правильный выход теперь такой:

1. `Legend`
2. `Normalized Reviews Table`
3. `Review Dashboard`
4. `Manual Queue`
5. `Trash`
6. `Signal Stats`

## Почему это лучше для батча

Потому что на каждом следующем товаре ты получаешь один и тот же визуальный каркас:

- таблица отзывов;
- карточки review-by-review;
- цветные сигналы;
- итоговая статистика.

Так проще:

- ловить системные ошибки;
- сравнивать товары;
- замечать ложные срабатывания;
- улучшать одну и ту же инструкцию по одному и тому же интерфейсу.

## Что уже собрано

В проекте теперь есть новый локальный пакет:

- [skills/signal-markup-v2/SKILL.md](/Users/alittlepinkie/Documents/New project/skills/signal-markup-v2/SKILL.md)
- [skills/signal-markup-v2/references/category-rules.md](/Users/alittlepinkie/Documents/New project/skills/signal-markup-v2/references/category-rules.md)
- [skills/signal-markup-v2/references/output-contract.md](/Users/alittlepinkie/Documents/New project/skills/signal-markup-v2/references/output-contract.md)
- [skills/signal-markup-v2/references/flow-and-guardrails.md](/Users/alittlepinkie/Documents/New project/skills/signal-markup-v2/references/flow-and-guardrails.md)
- [skills/signal-markup-v2/prompts/single-product-dashboard.md](/Users/alittlepinkie/Documents/New project/skills/signal-markup-v2/prompts/single-product-dashboard.md)

И новый человекочитаемый рендер:

- [signal_dashboard_v2.py](/Users/alittlepinkie/Documents/New project/signal_dashboard_v2.py)

## Следующий правильный шаг

Не усложнять дальше.

Сначала стабилизировать только одно:

`один товар -> хороший цветной dashboard -> понятная stats section`

Когда эта форма станет стабильной, только тогда:

- пакетный режим на 7 товаров;
- sidecar json;
- deeper analytics;
- buyer interpretation.

