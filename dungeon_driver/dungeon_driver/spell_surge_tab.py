from dungeon_driver.spell_surge_generator import SpellSurgeGenerator
import gradio as gr
import httpx
from loguru import logger

timeout = httpx.Timeout(600.0)


##########################
async def endpoint_test(prompt: str):
    response = await make_request(prompt, "pinecone")
    response2 = await make_request(prompt, "local_llm")
    if response.status_code == 200:
        print("Server is up and running!")
    else:
        print("Server is not responding.")
    return response.json()["result"], response2.json()["result"]


async def make_request(prompt, endpoint):
    async with httpx.AsyncClient(timeout=timeout) as client:
        logger.info(f"Making request to {endpoint} with query {prompt}")
        response = await client.get(
            f"http://ai_driver:28001/api/v1/chat/{endpoint}/{prompt}"
        )
        logger.info(response.text)
        return response


###########################
def generate_random_event():
    """
    Generates a random event string using SpellSurgeGenerator.

    Returns:
        str: A random event string.
    """
    ssg = SpellSurgeGenerator()
    return ssg.generate()


def create_spell_surge_generator():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(label="Enter a prompt")
                # temp_1 = gr.Slider(minimum=0, maximum=1.5, label="Temperature 1")
                # temp_2 = gr.Slider(minimum=0, maximum=1.5, label="Temperature 2")

            with gr.Column():
                response1 = gr.Textbox(label="Pinecone / OAI Response")
            with gr.Column():
                response2 = gr.Textbox(label="FAISS / LLaMa Response")

        generate_button = gr.Button("Generate Response")
        generate_button.click(
            fn=endpoint_test, inputs=[prompt], outputs=[response1, response2]
        )
        ssg_btn = gr.Button("Generate Spell Surge")
        ssg_btn.click(fn=generate_random_event, outputs=prompt)
