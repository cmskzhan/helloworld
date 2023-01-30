import time
import asyncio
import pandas_datareader.data as web

def function_speedo(f):
    async def _fn():
        starttime = time.time()
        await f()
        print(
            "child function run time is ",
            (time.time() - starttime) * 1000,
            "ms",
        )

    return _fn


async def sleep_and_print(seconds):
    print(f"starting async {seconds} sleep 😴")
    await asyncio.sleep(seconds)
    print(f"finished async {seconds} sleep ⏰")
    return seconds

async def coroutine_tasks():
    task = await asyncio.create_task(get_data("AAPL"))
    await task
    print(task)
    return task.result()

async def get_data(symbol:str):
    return web.DataReader(symbol, "yahoo", "2022-11-17")


@function_speedo
async def main():
    # using arguments
    # results = await asyncio.gather(sleep_and_print(3), sleep_and_print(6))
    # print(results)
    AAPL = await coroutine_tasks()
    print(AAPL)



asyncio.run(main())