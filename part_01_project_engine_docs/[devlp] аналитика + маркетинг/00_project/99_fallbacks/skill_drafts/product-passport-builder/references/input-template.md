# Шаблон Сырого Ввода Для Product Passport

Пользователь может вставлять сырьё в любом порядке.

Если вход грязный и хаотичный, сначала мысленно приведи его к этой форме, а уже потом собирай паспорт.

Используй эту структуру, если нужно попросить у пользователя более аккуратный ввод:

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

copied_page_text:

image_claims_voice_notes:
- 
- 
- 

unclear_or_missing:
```

Примечания:

- `product_key`, `product_role` и `marketplace` — это единственные реально блокирующие минимумы.
- `copied_page_text` может быть длинным и неаккуратным.
- `image_claims_voice_notes` может быть грубой голосовой диктовкой.
- Если пользователь пропустил поле, лучше ставить `unclear`, чем додумывать.
