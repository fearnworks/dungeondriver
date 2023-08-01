from dungeon_driver.mechanics.spell_surge_generator import SpellSurgeGenerator
import gradio as gr
import httpx
from loguru import logger

timeout = httpx.Timeout(600.0)


###########################
def generate_random_event():
    """
    Generates a random event string using SpellSurgeGenerator.

    Returns:
        str: A random event string.
    """
    ssg = SpellSurgeGenerator()
    return ssg.generate()


def create_spell_surge_generator() -> gr.Blocks:
    with gr.Blocks() as spell_surge_gen_tab:
        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(label="Enter a prompt")
                # temp_1 = gr.Slider(minimum=0, maximum=1.5, label="Temperature 1")
                # temp_2 = gr.Slider(minimum=0, maximum=1.5, label="Temperature 2")

            # with gr.Column():
            #     response1 = gr.Textbox(label="Pinecone / OAI Response")
            # with gr.Column():
            #     response2 = gr.Textbox(label="FAISS / LLaMa Response")

        ssg_btn = gr.Button("Generate Spell Surge")
        ssg_btn.click(fn=generate_random_event, outputs=prompt)
    return spell_surge_gen_tab
