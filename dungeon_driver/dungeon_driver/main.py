import httpx
from loguru import logger
import gradio as gr
import os
import dungeon_driver.webui as UIComponents
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def init_interface():
    title = "Dungeon Driver AI Web Ui"
    interface = {}
    with gr.Blocks(analytics_enabled=False, title=title) as ui:
        with gr.Tab("Authentication"):
            interface["login"] = UIComponents.login.create_login_interface()
            interface["login"]
        with gr.Tab("Spell Surge Generator"):
            interface[
                "ssg"
            ] = UIComponents.spell_surge_tab.create_spell_surge_generator()
            interface["ssg"]
        with gr.Tab("D&D Q&A"):
            interface["dnd_qa"] = UIComponents.dnd_qa_tab.create_dnd_qa()
            interface["dnd_qa"]
        with gr.Tab("Chatbot"):
            interface["chat"] = UIComponents.chat_tab.create_chat_interface()
            interface["chat"]

    ui.queue()

    ui.launch(
        prevent_thread_lock=True,
        server_name="0.0.0.0",
        server_port=18001,
        inbrowser=True,
    )


def main():
    init_interface()
    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    main()
