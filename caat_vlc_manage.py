for evn import BOTKEY,CHATID
from stat import UF_IMMUTABLE
from aiogram import Bot, Dispatcher, types, executor
import asyncio
import dbus

bot = Bot(token=BOTKEY)
dp = Dispatcher(bot=bot)

sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object(
    'org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')


@dp.message_handler(commands='start')
async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!,{event.chat.id}",
        parse_mode=types.ParseMode.HTML,
    )


@dp.message_handler(chat_id=CHATID, commands='statusvnc')
# @dp.message_handler(commands='statusvnc')
async def test_handler(msg: types.Message):
    u_id = argtoint(msg.get_args())
    if isinstance(u_id, int):
        t = await asyncio.create_subprocess_shell("sudo systemctl status vncserver@:"+str(
            u_id), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await t.communicate()
    await msg.answer(stdout.decode())


@dp.message_handler(chat_id=CHATID, commands='startvnc')
# @dp.message_handler(commands='startvnc')
async def startvnc_handler(msg: types.Message):
    u_id = argtoint(msg.get_args())
    if isinstance(u_id, int):
        t = await asyncio.create_subprocess_shell("sudo systemctl start vncserver@:"+str(
            u_id), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await t.communicate()
        if stderr.decode() == '':
            out = str(u_id)+" start"
        else:
            out = stderr.decode()
    await msg.answer(out)


@dp.message_handler(chat_id=CHATID, commands='stopvnc')
# @dp.message_handler(commands='stopvnc')
async def stopvnc_handler(msg: types.Message):
    u_id = argtoint(msg.get_args())
    if isinstance(u_id, int):
        job = manager.StopUnit("vncserver@:"+str(u_id)+".service", "fail")
    await msg.answer(str(u_id)+" stop")


def argtoint(str):
    id = "id is four digits, you can use 'id -u' to query"
    if len(str) == 4:
        try:
            id = int(str)
        except:
            id = "id is four digits, you can use 'id -u' to query"
    return id


if __name__ == '__main__':
    executor.start_polling(dp)
