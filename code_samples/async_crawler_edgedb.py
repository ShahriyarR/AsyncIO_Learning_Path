# This code is from the video tutorial ->
# https://www.youtube.com/watch?v=-CzqsgaXUM8&list=PLhNSoGM2ik6SIkVGXWBwerucXjgP1rHmB&index=3

import asyncio
import httpx
import time
from typing import Coroutine, Callable


async def progress(url: str, algo: Callable[..., Coroutine],) -> None:
    task = asyncio.create_task(algo(url), name=url,)
    todo.add(task)
    start = time.time()
    while len(todo):
        done, _pending = await asyncio.wait(todo, timeout=0.5)
        todo.difference_update(done)
        urls = (t.get_name() for t in todo)
        print(f"{len(todo)}: " + ", ".join(sorted(urls))[-75:])
    end = time.time()
    print(f"Took {int(end - start)}" + " seconds")


async def crawl2(prefix: str, url: str = "") -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    try:
        res = await client.get(url)
    finally:
        await client.aclose()
    for line in res.text.splitlines():
        if line.startswith(prefix):
            # Speeder version with background tasks
            task = asyncio.create_task(crawl2(prefix, line), name=line,)
            todo.add(task)


async def async_main() -> None:
    try:
        await progress(addr, crawl2)
    except asyncio.CancelledError:
        for task_ in todo:
            task_.cancel()
        done, pending = await asyncio.wait(todo, timeout=0.1)
        todo.difference_update(done)
        todo.difference_update(pending)
        if todo:
            print("warning: more tasks added while we were cancelling")


if __name__ == "__main__":
    todo = set()
    addr = "https://langa.pl/crawl"
    loop = asyncio.get_event_loop()
    task = loop.create_task(async_main())
    loop.call_later(10, task.cancel)
    loop.run_until_complete(task)