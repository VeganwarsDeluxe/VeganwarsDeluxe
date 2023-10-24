PROFILE_COMMAND = '🏅Профиль'
INVENTORY_COMMAND = "📦Инвентарь"
CASTLE_COMMAND = "🏰Замок"

ATTACK_COMMAND = "🗡Атака"
DEFEND_COMMAND = "🛡Защита"
QUESTS_COMMAND = "🗺Квесты"

ABILITIES_COMMAND = "🧬Способности"
ITEMS_COMMAND = "💣Предметы"

CASTLE_ENTRANCE_TEXT = 'Ваш родной замок. В магазине можно найти базовые свитки изучения скиллов и оружие.'
NO_CASTLE_PLEASE_JOIN = '🤕У вас нет замка! Сначала вступите в какой-либо!'
SHOP_COMMAND = '🏚Магазин'
CRAFT_COMMAND = '🛠Крафт'
TRADE_COMMAND = '⚖️Биржа'
AUCTION_COMMAND = '🛎Аукцион'
REST_COMMAND = "🛏Лечь в кровать"
NO_CASTLE_REST_COMMAND = "🍂Лечь на сено"

RAT_CASTLE = "🐭Крысиный замок"
DARK_CASTLE = "👁Замок тьмы"
NECROMANCER_CASTLE = "🖤Замок некроманта"
EXPLOSION_CASTLE = "💮Замок магии взрывов"

SCROLLS_SHOP_COMMAND = "📜Свитки"
EQUIPMENT_SHOP_COMMAND = "⚙️Снаряжение"
DEC_RECIPE_COMMAND = "📓❓Расшифровка рецептов"
DEC_SCROLL_COMMAND = "🗞❓Расшифровка свитков"

JOIN_MARK = "📝"
ATTACK_MARK = "🗡"
CASTLE_JOIN_BUTTONS = {RAT_CASTLE+JOIN_MARK: 'rat',
                       DARK_CASTLE+JOIN_MARK: 'dark',
                       NECROMANCER_CASTLE+JOIN_MARK: 'necromancer',
                       EXPLOSION_CASTLE+JOIN_MARK: 'explosion'}
CASTLE_ATTACK_BUTTONS = {RAT_CASTLE+ATTACK_MARK: 'rat',
                         DARK_CASTLE+ATTACK_MARK: 'dark',
                         NECROMANCER_CASTLE+ATTACK_MARK: 'necromancer',
                         EXPLOSION_CASTLE+ATTACK_MARK: 'explosion'}

CASTLE_ID_TO_TEXT = {
    'outsider': '🤕Отшельник',
    'rat': RAT_CASTLE,
    'dark': DARK_CASTLE,
    'necromancer': NECROMANCER_CASTLE,
    'explosion': EXPLOSION_CASTLE
}


ACTION_ID_TO_TEXT = {
    'rest': '🛌Отдых',
    'defense': '🛡Защита',
    'attack': '🗡Атака'
}

RECIPE_COLOR_TO_NAME = {
    'red': 'Красный рецепт',
    'blue': 'Синий рецепт',
    'green': 'Зелёный рецепт'
}
