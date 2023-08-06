import gradio as gr
import httpx
from loguru import logger
from pathlib import Path

timeout = httpx.Timeout(600.0)


async def make_request(prompt, endpoint):
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.info(f"Making request to {endpoint} with query {prompt}")
        request = {"query": prompt}
        response = await client.post(
            f"http://ai_driver:28001/api/v1/chat/{endpoint}",
            json=request,
        )
        logger.debug(response.text)
        return response


async def chat(chat_history, message: str):
    logger.info(f"Chatbot received message: {message}")
    logger.info(f"Chatbot chat history: {chat_history}")
    response = await make_request(message, "cloudllm")
    response = response.json()
    history = chat_history + [(message, response["result"])]
    return history


def create_chat_interface() -> gr.Blocks:
    with gr.Blocks() as chat_tab:
        gr.Markdown("# Chatbot")
        chat_history = [("Hello", "Hi!")]
        chat_display = gr.Chatbot(
            chat_history, elem_id="chatbot", height=650, placeholder="Type a message..."
        )
        chat_input = gr.Textbox("")
        chat_input.submit(
            chat, inputs=[chat_display, chat_input], outputs=[chat_display]
        )

    return chat_tab
