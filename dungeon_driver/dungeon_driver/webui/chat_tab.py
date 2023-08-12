import gradio as gr
import httpx
from loguru import logger
from pathlib import Path
import secrets
from dungeon_driver.webui.auth import auth_service

timeout = httpx.Timeout(600.0)


async def make_request(prompt, session_id, endpoint):
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Call add_auth_headers to include the authentication token in the headers
        client = auth_service.add_auth_headers(client)

        logger.info(f"Making request to {endpoint} with query {prompt}")
        request = {"query": prompt, "session_id": session_id}
        response = await client.post(
            f"http://ai_driver:28001/api/v1/chat/{endpoint}",
            json=request,
        )
        logger.debug(response.text)
        return response


async def chat(chat_history, message: str, session_id: str):
    logger.info(f"Chatbot received message: {message}")
    response = await make_request(message, session_id, "cloudllm")
    response = response.json()
    history = chat_history + [(message, response["result"])]
    return history


async def get_history(session_id: str):
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Call add_auth_headers to include the authentication token in the headers
        client = auth_service.add_auth_headers(client)

        logger.info(f"Making request to history with session {session_id}")
        request = {"session_id": session_id}
        response = await client.post(
            f"http://ai_driver:28001/api/v1/chat/cloudllm/history",
            json=request,
        )
        logger.debug(response.text)
        history_pairs = response.json()["history"]
        history = []
        for pair in history_pairs:
            history.append((pair["human"], pair["ai"]))

        return history


def create_chat_interface() -> gr.Blocks:
    session_id = secrets.randbits(32)
    with gr.Blocks() as chat_tab:
        gr.Markdown("# Chatbot")
        with gr.Row():
            chat_history = []
            chat_display = gr.Chatbot(
                chat_history,
                elem_id="chatbot",
                height=1250,
                placeholder="Type a message...",
            )
        with gr.Row():
            chat_input = gr.Textbox("")
            session_id_label = gr.Textbox(session_id, label="Session ID")
            chat_input.submit(
                chat,
                inputs=[chat_display, chat_input, session_id_label],
                outputs=[chat_display],
            )
            refresh_button = gr.Button("Refresh History")
            refresh_button.click(
                get_history, inputs=[session_id_label], outputs=[chat_display]
            )

    return chat_tab
