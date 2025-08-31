import asyncio
from utils.core import load_from_json, save_to_json, logger
from pyrogram import Client
from data import config
from pyrogram.raw.functions.payments import GetStarGifts
from pyrogram.raw.types import StarGift
from typing import List
from pyrogram.file_id import FileId, FileType


async def snipe_new_gifts(bot_client: Client, tg_client: Client):
    gifts: List[StarGift] = (await tg_client.invoke(GetStarGifts(hash=0))).gifts
    gifts_in_json = load_from_json('gifts.json')

    for gift in gifts:
        gift_dict = {'id': gift.id, 'price': gift.stars}

        if gift_dict not in gifts_in_json:
            logger.success(f"Founded new gift ({gift.title}) {gift.id}")
            save_to_json('gifts.json', gift_dict)
            gifts_in_json.append(gift_dict)

            if config.SEND_NOTIFICATIONS:
                limited = f'Limited ({gift.availability_total})' if gift.limited else 'No limits'
                try:
                    sticker_data = await bot_client.download_media(
                        message=FileId(
                            file_type=FileType.STICKER,
                            dc_id=gift.sticker.dc_id,
                            media_id=gift.sticker.id,
                            access_hash=gift.sticker.access_hash,
                            file_reference=gift.sticker.file_reference
                        ).encode(),
                        in_memory=True,
                        file_name='sticker.tgs'
                    )
                    await bot_client.send_sticker(chat_id=config.NOTIFICATIONS_ID, sticker=sticker_data)
                except Exception as e:
                    logger.error(f"Error while sending a sticker to {config.NOTIFICATIONS_ID} chat id: {e}")

                try:
                    txt = f'<b>⬆️ NEW GIFT AVAILABLE ⬆️\n❗️ {limited}\n\n⭐ Price: {gift.stars} STAR\n🎁 Supply: {gift.availability_total}</b>\n🌟 Only premium: {"✅" if gift.require_premium else "❌"}\n\n🆔 {gift.id}'
                    await bot_client.send_message(chat_id=config.NOTIFICATIONS_ID, text=txt)
                except Exception as e:
                    logger.error(f"Error while sending a message about new gift ({gift.title}) to {config.NOTIFICATIONS_ID} chat id: {e}")

            if config.ONLY_PREMIUM and not gift.per_user_remains:
                continue

            if not gift.limited or gift.availability_total < config.SUPPLY_LIMIT["FROM"] or gift.availability_total > config.SUPPLY_LIMIT["TO"]:
                continue

            if gift.stars < config.PRICE_LIMIT['FROM'] or gift.stars > config.PRICE_LIMIT['TO']:
                continue

            if config.BUY_GIFT:
                await buy_gift(
                    bot_client=bot_client,
                    tg_client=tg_client,
                    count=config.GIFT_COUNT_TO_BUY,
                    chat_id=config.ID_TO_BUY,
                    gift=gift
                )


async def buy_gift(bot_client: Client, tg_client: Client, count: int, chat_id: [int, str], gift: StarGift):
    logger.debug(f"[{gift.id}] Trying to buy a gift")
    star_balance_before = await tg_client.get_stars_balance()
    have_premium = (await tg_client.get_me()).is_premium

    number, bough_gifts = 0, 0
    balance = star_balance_before
    count_to_buy = count if gift.availability_remains > count else gift.availability_remains

    errors = []
    for number in range(1, count_to_buy + 1):
        if balance < gift.stars:
            logger.warning(f"Not enough stars to buy a gift_id: {gift.id}")
            number -= 1
            break

        if not count_to_buy:
            logger.warning(f"No gifts with gift_id {gift.id} available")
            number -= 1
            break

        if gift.require_premium and not have_premium:
            logger.warning(f"Need premium to buy a gift_id {gift.id}")
            number -= 1
            break

        try:
            await tg_client.send_gift(chat_id=chat_id, gift_id=gift.id, text='Gift was bought via @ApeCryptor soft')
            bough_gifts += 1
            balance -= gift.stars
        except Exception as e:
            error_txt = f"{number}/{count_to_buy} | Error while buying a gift {gift.id}: {e}"

            logger.error(error_txt)

            if len(errors) <= 2:
                errors.append(error_txt)

            if any(error in str(e) for error in ['USAGE_LIMITED', 'BALANCE_TOO_LOW', 'PREMIUM']):
                logger.debug(f"Stop error: {e}")
                break

    star_balance_after = await tg_client.get_stars_balance()
    f_errors = "\n".join(errors)
    errors_txt = f'<b>Errors while buying (first 3):</b>\n<blockquote expandable>{f_errors}</blockquote>' if errors else ''

    await bot_client.send_message(
        chat_id=config.ADMIN_ID,
        text=f'<b>✅ Successfully bought {bough_gifts} of {number} new gifts!\n\n⭐ Stars spent: {star_balance_before - balance}({star_balance_before - star_balance_after})\n⭐ Balance before: {star_balance_before}\n⭐ Balance after: {star_balance_after}</b>\n\n{errors_txt}'
    )

    return bough_gifts
