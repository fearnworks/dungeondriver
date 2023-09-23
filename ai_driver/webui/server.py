import asyncio
from loguru import logger
import gradio as gr
import os
import time
from dotenv import load_dotenv, find_dotenv
from auth import auth_service
from chat import create_swarm_chat_interface

load_dotenv(find_dotenv())


def init_interface():
    title = "Dungeon Driver AI Web Ui"
    interface = {}
    with gr.Blocks(analytics_enabled=False, title=title) as ui:
        with gr.Tab("Authentication"):
            gr.Label("Login to the AI Driver")
        with gr.Tab("Swarm"):
            interface["chat"] = create_swarm_chat_interface()
    ui.queue()

    ui.launch(
        prevent_thread_lock=True,
        server_name="0.0.0.0",
        server_port=18000,
        inbrowser=True,
    )


async def main():
    token = await auth_service.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
    logger.info(token)
    init_interface()
    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
