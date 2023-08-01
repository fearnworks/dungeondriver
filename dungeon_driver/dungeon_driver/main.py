import httpx
from loguru import logger

timeout = httpx.Timeout(600.0)


async def make_request(query, endpoint):
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.info(f"Making request to {endpoint} with query {query}")
        response = await client.get(
            f"http://ai_driver:28001/api/v1/chat/{endpoint}/{query}"
        )
        logger.info(response.text)
        return response


async def main():
    query = "How do saving throws work?"
    response = await make_request(query, "pinecone")
    response2 = await make_request(query, "local_llm")
    if response.status_code == 200:
        print("Server is up and running!")
    else:
        print("Server is not responding.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
