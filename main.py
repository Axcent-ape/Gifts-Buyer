import asyncio
import random
from utils.core import logger, Client
from data import config
from utils.telegram import snipe_new_gifts


async def init_clients():
    bot_client = Client('TgBot', bot_token=config.BOT_TOKEN_WRITER, api_hash=config.API_HASH, api_id=config.API_ID)
    await bot_client.start()

    bot = await bot_client.get_me()
    logger.info(f"Initialized bot client. Bot: {bot.full_name} (@{bot.username}); id:{bot.id} ")

    tg_client = Client("TgAccount", api_hash=config.API_HASH, api_id=config.API_ID)

    await tg_client.start()

    user = await tg_client.get_me()
    star_balance = await tg_client.get_stars_balance()

    if config.CHECK_ID_TO_BUY and config.BUY_GIFT:
        try:
            await tg_client.resolve_peer(peer_id=config.ID_TO_BUY)
        except Exception as e:
            logger.critical(f'Incorrect ID_TO_BUY! {e}')
            exit()

    logger.info(f"Initialized account client. User: {user.full_name} (@{user.username}); id:{user.id}; star balance: {star_balance}; Id to buy gifts: {config.ID_TO_BUY}")

    return bot_client, tg_client


async def main():
    bot_client, tg_client = await init_clients()

    logger.info("Soft is waiting for new gifts...")

    while True:
        try:
            await snipe_new_gifts(bot_client=bot_client, tg_client=tg_client)
            await asyncio.sleep(random.uniform(8, 15))

        except Exception as e:
            await asyncio.sleep(1)
            logger.error(f"Error in main function: {e}")


if __name__ == '__main__':
    print("""
 ██████╗ ██╗███████╗████████╗███████╗    ██████╗ ██╗   ██╗██╗   ██╗███████╗██████╗ 
██╔════╝ ██║██╔════╝╚══██╔══╝██╔════╝    ██╔══██╗██║   ██║╚██╗ ██╔╝██╔════╝██╔══██╗
██║  ███╗██║█████╗     ██║   ███████╗    ██████╔╝██║   ██║ ╚████╔╝ █████╗  ██████╔╝
██║   ██║██║██╔══╝     ██║   ╚════██║    ██╔══██╗██║   ██║  ╚██╔╝  ██╔══╝  ██╔══██╗
╚██████╔╝██║██║        ██║   ███████║    ██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║
 ╚═════╝ ╚═╝╚═╝        ╚═╝   ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                   
Soft's author: https://t.me/ApeCryptor
Soft's author: https://t.me/ApeCryptor
Soft's author: https://t.me/ApeCryptor
    """)
    print('Information about the premium version of Gifts Bayer: https://t.me/ApeCryptorSoft/150'.center(20))
    asyncio.run(main())
