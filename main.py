from __future__ import annotations

import sys
import asyncio
import logging
import argparse

from collections import namedtuple

from typing import Callable, List

import commands

Task = namedtuple("Task", "func args kwargs")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s::%(levelname)s::%(module)s.%(funcName)s::%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__file__)
USERS_FILE_NAME = "users.txt"


def construct_task(func: Callable, *args, **kwargs):
    if not args:
        args = []
    if not kwargs:
        kwargs = {}
    return Task(func=func, args=args, kwargs=kwargs)

def pass_task_to_taskgroup(tg, task):
    if task.args and task.kwargs:
        tg.create_task(task.func(*task.args, **task.kwargs))
    elif task.args:
        tg.create_task(task.func(*task.args)) 
    else:
        tg.create_task(task.func())

def argument_parsing(args: List[str]) -> argparse.Namespace:
    """Parse all arguments"""
    parser = argparse.ArgumentParser()
    return parser.parse_args(args)

async def main(main_loop_tasks: List[Task] = None, pre_loop_tasks: List[Task] = None) -> None:
    """Run main loop"""
    async with asyncio.TaskGroup() as tg:
        if pre_loop_tasks:
            for task in pre_loop_tasks:
                pass_task_to_taskgroup(tg, task)

    async with asyncio.TaskGroup() as tg:
        if main_loop_tasks:
            for task in main_loop_tasks:
                pass_task_to_taskgroup(tg, task)      


async def print_shit():
    for i in range(10):
        print("hello\n")


if __name__== "__main__":
    parsed_args = argument_parsing(sys.argv[1:])

    #TODO: Task to look at registered users and poll them
    #Oh wait might not be necessary, I might just need to call tgbot.begin_liostening
    maintask = construct_task(commands.dispatcher.start_polling, commands.tgbot)
    listening_task = construct_task(commands.prequel_bot.begin_listening)
    main_loop_tasks = []
    main_loop_tasks.append(maintask)
    main_loop_tasks.append(listening_task)

    asyncio.run(main(main_loop_tasks=main_loop_tasks))