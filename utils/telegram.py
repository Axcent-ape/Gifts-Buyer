import asyncio
from utils.core import load_from_json, save_to_json, logger
from pyrogram import Client, types
from data import config


async def snipe_new_gifts(bot_client: Client, tg_client: Client):
    gifts = await tg_client.get_available_gifts()
    gifts_in_json = load_from_json('gifts.json')

    for gift in gifts:
        gift_dict = {'id': gift.id, 'price': gift.price}

        if gift_dict not in gifts_in_json:
            save_to_json('gifts.json', gift_dict)
            gifts_in_json.append(gift_dict)

            if config.SEND_NOTIFICATIONS:
                limited = f'Limited ({gift.available_amount})' if gift.is_limited else 'No limits'
                try:
                    sticker_data = await bot_client.download_media(gift.sticker.file_id, in_memory=True)
                    sticker_data.name = 'sticker.tgs'
                    await bot_client.send_sticker(chat_id=config.NOTIFICATIONS_ID, sticker=sticker_data)
                except Exception as e:
                    logger.error(f"Error while sending a sticker to {config.NOTIFICATIONS_ID} chat id: {e}")

                try:
                    txt = f'<b>⬆️ NEW GIFT AVAILABLE ⬆️\n❗️ {limited}\n\n⭐ Price: {gift.price} STAR\n🎁 Supply: {gift.total_amount}</b>\n🌟 Only premium: {"✅" if gift.raw.require_premium else "❌"}'
                    await bot_client.send_message(chat_id=config.NOTIFICATIONS_ID, text=txt)
                except Exception as e:
                    logger.error(
                        f"Error while sending a message about new gift to {config.NOTIFICATIONS_ID} chat id: {e}")

            if config.ONLY_PREMIUM and not gift.raw.per_user_remains:
                continue

            if not gift.is_limited or gift.total_amount < config.SUPPLY_LIMIT["FROM"] or gift.total_amount > config.SUPPLY_LIMIT["TO"]:
                continue

            if gift.price < config.PRICE_LIMIT['FROM'] or gift.price > config.PRICE_LIMIT['TO']:
                continue

            if config.BUY_GIFT:
                await buy_gift(
                    bot_client=bot_client,
                    tg_client=tg_client,
                    count=config.GIFT_COUNT_TO_BUY,
                    chat_id=config.ID_TO_BUY,
                    gift=gift
                )


async def buy_gift(bot_client: Client, tg_client: Client, count: int, chat_id: [int, str], gift: types.Gift):
    star_balance_before = await tg_client.get_stars_balance()
    have_premium = (await tg_client.get_me()).is_premium

    number, bough_gifts = 0, 0
    balance = star_balance_before
    available_amount = gift.raw.per_user_remains if gift.raw.limited_per_user and gift.available_amount > gift.raw.per_user_remains else gift.available_amount

    errors = []
    for number in range(1, count + 1):
        if balance < gift.price:
            logger.warning(f"Not enough stars to buy a gift_id: {gift.id}")
            number -= 1
            break

        if not available_amount:
            logger.warning(f"No gifts with gift_id {gift.id} available")
            number -= 1
            break

        if gift.raw.require_premium and not have_premium:
            logger.warning(f"Need premium to buy a gift_id {gift.id}")
            number -= 1
            break

        try:
            await tg_client.send_gift(chat_id=chat_id, gift_id=gift.id, text='Gift was bought via @ApeCryptor soft')
            bough_gifts += 1
            balance -= gift.price
        except Exception as e:
            error_txt = f"{number}/{count} | Error while buying a gift {gift.id}: {e}"

            logger.error(error_txt)

            if len(errors) <= 2:
                errors.append(error_txt)

        if number % 3 == 0:
            available_amount = await get_gift_available_amount(tg_client, gift.id)
            await asyncio.sleep(1)

    star_balance_after = await tg_client.get_stars_balance()
    f_errors = "\n".join(errors)
    errors_txt = f'<b>Errors while buying (first 3):</b>\n<blockquote expandable>{f_errors}</blockquote>' if errors else ''

    await bot_client.send_message(
        chat_id=config.ADMIN_ID,
        text=f'<b>✅ Successfully bought {bough_gifts} of {number} new gifts!\n\n⭐ Stars spent: {star_balance_before - balance}({star_balance_before - star_balance_after})\n⭐ Balance before: {star_balance_before}\n⭐ Balance after: {star_balance_after}</b>\n\n{errors_txt}'
    )

    return bough_gifts


async def get_gift_available_amount(tg_client: Client, gift_id: int):
    gifts = await tg_client.get_available_gifts()

    for gift in gifts:
        if gift.id == gift_id:
            return gift.raw.per_user_remains if gift.raw.limited_per_user and gift.available_amount > gift.raw.per_user_remains else gift.available_amount
