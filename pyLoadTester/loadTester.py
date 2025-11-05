import asyncio
import aiohttp
import time

async def fetch(session, url):
    start = time.time()
    try:
        async with session.get(url) as response:
            await response.text()
            return (response.status, time.time() - start)
    except Exception as e:
        return (None, time.time() - start)

async def run_load_test(url, total_requests, concurrency):
    tasks = []
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        for _ in range(total_requests):
            tasks.append(fetch(session, url))
        results = await asyncio.gather(*tasks)

    success = sum(1 for r, _ in results if r == 200)
    failed = sum(1 for r, _ in results if r != 200)
    avg_time = sum(t for _, t in results) / len(results)

    print(f"Total Requests: {total_requests}")
    print(f"Success: {success}, Failed: {failed}")
    print(f"Average Response Time: {avg_time:.3f} sec")

if __name__ == "__main__":
    url = input("Enter IP or Link (with http or https): ")
    asyncio.run(run_load_test(url, total_requests=1000, concurrency=10))
