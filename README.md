# 🎁 Telegram Gift Buyer and Sniper

Soft's author: [ApeCryptor](https://t.me/+_xCNXumUNWJkYjAy "ApeCryptor") 🦧
Premium version of Gifts Bayer: https://t.me/ApeCryptorSoft/150
#

### 🐍 Python Version 
Preferably python 3.11+

#
### Library Installation 📚
`pip install -r requirements.txt` 

#
### ⚙️ Configuration data/config.py:
1. **API_ID, API_HASH** - Get [here](https://my.telegram.org/auth)
2. **BOT_TOKEN_WRITER** - Token of tg bot, which will write about new gifts + send a log about buying a gift. Get it in the [bot](http://t.me/BotFather)
3. **NOTIFICATIONS_ID** - Chat ID (group/channel/id of your account - so that the bot will write to ls) in which the bot will write about new gifts.
4. **SEND_NOTIFICATIONS** - True/False - enable/disable notifications from the 3rd item
5. **ADMIN_ID** - the ID of your main account, to which the bot will send a log of gift purchases.
6. **BUY_GIFT** - True/False - enable/disable purchase of gifts
7. **PRICE_LIMIT** - allowable range for the price of the gift
8. **SUPPLY_LIMIT** - allowable range for the supply of the gift
9. **GIFT_COUNT_TO_BUY** - the number of gifts a bot must buy from a new collection
10. **ID_TO_BUY** - ID of the chat to buy a gift for (it could be a channel)
