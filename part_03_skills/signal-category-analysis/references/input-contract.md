# Input Contract

Вход:

- `category`: одна из 6 категорий
- один или несколько registry packages из предыдущего этапа разметки

Каждый пакет обязан содержать:

- `product_key`
- `units_registry`
- `signals_registry`
- `stats`

Если продуктов несколько, не смешивать их идентификаторы.
