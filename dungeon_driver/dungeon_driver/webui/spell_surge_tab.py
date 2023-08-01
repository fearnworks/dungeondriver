from dungeon_driver.mechanics.spell_surge_generator import SpellSurgeGenerator
from dungeon_driver.prompts.prompt_builder import replace_prompt
from dungeon_driver.prompts.img_gen import OPENAI_RPG_SD_AGENT_PROMPT
import gradio as gr
import httpx
from loguru import logger

timeout = httpx.Timeout(600.0)


def generate_sd_prompt(random_event: str):
    prompt = replace_prompt(OPENAI_RPG_SD_AGENT_PROMPT, {"prompt": random_event})
    return prompt


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

            with gr.Column():
                sd_prompt = gr.Textbox(label="Pinecone / OAI Response")
            # with gr.Column():
            #     response2 = gr.Textbox(label="FAISS / LLaMa Response")

        ssg_btn = gr.Button("Generate Spell Surge")
        ssg_btn.click(fn=generate_random_event, outputs=prompt)
        img_gen_btn = gr.Button("Generate Stable Diffusion Prompt")
        img_gen_btn.click(fn=generate_sd_prompt, inputs=prompt, outputs=sd_prompt)
    return spell_surge_gen_tab
