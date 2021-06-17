import unittest
from asyncio import CancelledError
from unittest import TestCase


import asyncio

async def wait_time(time):
    try:
        await asyncio.sleep(time)
    except CancelledError:
        print("Sleep is cancelled")


async def test_timeout():
    try:
        async with asyncio.timeout(3) as to:
            await wait_time(6)
    except TimeoutError:
        print("oops took longer than 3s!")
    finally:
        print(to.expired)


class TimeoutTest(TestCase):
    @unittest.skip
    def test_timeout(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_timeout())
        loop.close()