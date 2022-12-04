import time
import asyncio


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


@function_speedo
async def main():
    # using arguments
    results = await asyncio.gather(sleep_and_print(3), sleep_and_print(6))
    print(results)


asyncio.run(main())