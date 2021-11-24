from bot import bot
from db import db_init
from vkwave.bots.addons.easy import TaskManager

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.add_task(db_init)
    task_manager.add_task(bot.run)
    task_manager.run()
