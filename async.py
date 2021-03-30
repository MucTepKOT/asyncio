import asyncio
import functools
import random
import signal
import sys

random_int_list = []
max_list = []
min_list = []
avrg_list = []

def ask_exit(signame, loop):
    print(f"got signal {signame}: exit")
    for task in asyncio.all_tasks():
        task.cancel()

async def random_int():
    loop = asyncio.get_running_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(ask_exit, signame, loop))
    try:
        while True:
            random_int_list.append(random.randint(1, 1000000))
            await asyncio.sleep(random.randint(0, 10))
            task1 = asyncio.create_task(max_int(random_int_list))
            task2 = asyncio.create_task(min_int(random_int_list))
            task3 = asyncio.create_task(avrg_int(random_int_list))
    except asyncio.CancelledError:
        pass
    loop.stop()
    sys.exit(1)


async def max_int(random_int_list):
    result = max(random_int_list)
    if result not in max_list:
        max_list.append(result)
        print(f"max_int: {result}")
    await asyncio.sleep(0)

async def min_int(random_int_list):
    result = min(random_int_list)
    if result not in min_list:
        min_list.append(result)
        print(f"min_int: {result}")
    await asyncio.sleep(0)

async def avrg_int(random_int_list):
    result = int(sum(random_int_list)/len(random_int_list))
    if result not in avrg_list:
        avrg_list.append(result)
        print(f"avrg_int: {result}")
    await asyncio.sleep(0)

asyncio.run(random_int())