# Contracts Matrix

product_key: direct_touchy_hand_cream_50ml
product_role: direct_competitor
product_name: TOUCHY, крем для рук увлажняющий парфюмированный, 50 мл
matrix_type: local
stage: 03B_local_specialist_matrix
generated_by: specialist_review
routing_status: specialist_reviewed_3B
owner: marketplace_strategist
specialist_inputs:
- behavioral_strategist
toolkits_used:
- 00_project/03_roles/toolkits/marketplace_strategist/default_tools.md
- 00_project/03_roles/toolkits/behavioral_strategist/default_tools.md
based_on_signal_markup: 02_signal_markup/direct_competitors/direct_touchy_hand_cream_50ml/02__direct_touchy_hand_cream_50ml__signal_markup.md
based_on_product_passport: 01_intake/product_passports/direct_competitors/direct_touchy_hand_cream_50ml/01__direct_touchy_hand_cream_50ml__product_passport.md
based_on_price_snapshot: 01_intake/01__project__price_value_snapshot.md
based_on_technical_draft: 03_contract_matrices/direct_competitors/direct_touchy_hand_cream_50ml/03a__direct_touchy_hand_cream_50ml__technical_matrix_draft.md

## Матрица

| Контракт / сценарий | Видимый минус / риск | Кому стоп | Когда терпимо | Что удерживает покупку | Цена / контекст | Риск обещания | Evidence IDs | Статус |
|---|---|---|---|---|---|---|---|---|
| Парфюмированный крем как маленький luxury-ритуал | аромат может оказаться взрослым, ретро или не тем направлением | тем, кто ждёт современный сладкий/нишевый вайб | если покупатель любит выраженную парфюмность | аромат, текстура, “как духи” | 488 руб; 50 мл; 9,76 руб/мл | не обещать универсально приятный аромат | DT1-DT3 | direct_norm |
| Время нанесения меняет оценку аромата | перед сном запах может мешать | чувствительным к запахам и тем, кто мажет руки на ночь | днём тот же аромат может быть плюсом | аромат как дневной ритуал | universal/night use спорен для парфюмированного крема | не писать “универсально на ночь” без осторожности | DT4 | direct_warning |
| Быстрый сухой финиш как норма дорогого крема | плёнка, жирность или слабое впитывание ломают ощущение премиальности | тем, кто сразу берётся за телефон/компьютер | если финиш сухой и не мешает | быстро впитывается, не жирный, нет плёнки | самый дорогой за мл конкурент | claim `без липкости` должен быть проверенным | DT5 | direct_norm |
| Лёгкая текстура против зимнего ухода | зимой или для сухих рук может хотеться плотнее | покупателям с сильной сухостью | весной, летом, днём, при запросе на лёгкость | лёгкость, комфорт, аромат | seller обещает холодное время, но отзывы спорят | не обещать зимнюю защиту без уточнения | DT6-DT7 | direct_warning |
| Упаковка, подарок и сумка | красивая упаковка не спасает, если пришёл другой вариант или туба трескается | подарочный покупатель и покупатель для сумки | если упаковка целая и покупка для себя | красивая упаковка, компактность 50 мл | gift claim; компактнее героя | не обещать “идеально в подарок/с собой” без рисков | DT8-DT9 | direct_norm |
| Линейка ароматов и повторные пробы | любовь к аромату может вести в другие ароматы, а не в этот SKU | если герой не имеет явной review-опоры на линейку | когда покупателю нравится ароматический мир бренда | интерес к другим ароматам, повтор | ароматическая линейка бренда | не переносить лояльность линейки напрямую на героя | DT10 | direct_context |

## Короткие Выводы Специалистов

market_norms:
- прямой рынок снова делает fragrance-first логику видимой;
- сухой финиш является нормой дорогого парфюмированного крема;
- packaging/gift/compactness нужно читать вместе, а не отдельно.

warnings_for_hero:
- ретро/взрослый ароматический код опасен для эстетичного продукта;
- ночное использование конфликтует с парфюмированностью;
- 50 мл у Touchy сильнее для сумки, чем 75 мл героя, поэтому сумку героя нельзя обещать слишком уверенно.
