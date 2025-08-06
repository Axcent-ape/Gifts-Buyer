API_ID = 1234
API_HASH = 'abcde123'

# Bot token from @BotFather
BOT_TOKEN_WRITER = '12345:kvhjkjJKJKklKLFK-skld'

# chat/channel id to which notifications about new gifts will be sent. For a bot to send notifications to a channel, it needs to be added there
SEND_NOTIFICATIONS = True
NOTIFICATIONS_ID = 6008239182

# id account to which the bot will write about gift buy. !!!Before you run the soft, you should write first to the bot
ADMIN_ID = 6008239182


# # # Auto-purchase settings

# True/False.
BUY_GIFT = True

# buy only premium gifts
ONLY_PREMIUM = False

# Price limit. A purchase will be made if the price of the gift is in the FROM-TO range
PRICE_LIMIT = {
    "FROM": 0,
    "TO": 500
}

# Supply limit. A purchase will be made if the gift supply is between FROM-TO
SUPPLY_LIMIT = {
    "FROM": 1,
    "TO": 50000
}

# count of gifts per purchase from the collection
GIFT_COUNT_TO_BUY = 2

# chat/channel id on which the gifts will be purchased.
ID_TO_BUY = 6008239182

# check ID_TO_BUY to correct
CHECK_ID_TO_BUY = True
