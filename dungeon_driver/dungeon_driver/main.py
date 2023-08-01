import httpx
from loguru import logger
import gradio as gr
from dungeon_driver.spell_surge_tab import create_spell_surge_generator
import time


def init_interface():
    title = "Dungeon Driver AI Web Ui"
    with gr.Blocks(analytics_enabled=False, title=title) as ui:
        create_spell_surge_generator()
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
