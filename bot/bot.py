from config import VK_TOKEN, GROUP_ID
from keyboards import Menu, Answers
from verses import get_verse, random_verse

from vkwave.bots import SimpleLongPollBot
from vkwave.bots.core.dispatching import filters
from vkwave.bots.core.dispatching.filters import filter_caster
from vkwave.bots import SimpleBotEvent, BotEvent
from vkwave.bots.storage.storages import TTLStorage
from vkwave.bots.storage.types import Key

import random
import json

from typing import Callable

bot = SimpleLongPollBot(tokens=VK_TOKEN, group_id=GROUP_ID)
storage = TTLStorage(default_ttl=120)
task_id = 0

def for_entry(command: str):
    
    def func(event: BotEvent) -> bool:
        payload = event.object.object.message.payload
        if not payload:
            return False
        payload = json.loads(payload)
        return payload.get("command") == command 

    return filter_caster.cast(func)

for_hello = filter_caster.cast(
    lambda event: not event.object.object.message.payload
)



@bot.message_handler(for_entry("start") | for_hello)
async def hello(event: SimpleBotEvent):
    await event.answer(
        message="Привет, я помогу тебе проверить твое знание Четвероевангелия. "
                "Для начала нажми на кнопку \"Новый стих\".",
        keyboard=Menu.main()
    )

@bot.message_handler(for_entry("tasks.new"))
async def task_request(event: SimpleBotEvent):
    global task_id
    amount = 3
    answers = [random_verse() for i in range(amount)]
    picked = random.randint(0,amount - 1)


    await storage.put(Key(task_id), picked)

    await event.answer(
        message=get_verse(answers[picked]),
        keyboard=Answers.generate(task_id, answers)
    )
    task_id += 1

@bot.message_handler(for_entry("tasks.answer"))
async def task_answer(event: SimpleBotEvent):
    payload = event.payload
    args = payload.get("args")
    task_id = args.get("task_id")
    value = await storage.get(task_id, -1)

    
    if value == args.get("answer"):
        await event.answer(
            message="Верный ответ!"        
        ) 
        await storage.delete(task_id)
    elif value != -1:
        await event.answer(
            message="Неверный ответ!"        
        )
        await storage.delete(task_id)
    else:
        await event.answer(
            message="Ты уже ответил на этот вопрос или потратил на него слишком много времени!"
        )

bot.run_forever()
