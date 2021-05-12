from asyncio import CancelledError
from time import sleep

import async_timeout
import asyncio

async def wait_time(time):
    try:
        await asyncio.sleep(time)
    except CancelledError:
        print("Sleep is cancelled")


async def test_timeout():
    try:
        async with async_timeout.timeout(3) as to:
            await wait_time(6)
    except TimeoutError:
        print("oops took longer than 3s!")
    finally:
        print(to.expired)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_timeout())
    loop.close()