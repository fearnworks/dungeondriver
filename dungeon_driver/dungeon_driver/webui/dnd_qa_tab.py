import gradio as gr
import httpx
from loguru import logger
from dungeon_driver.webui.auth import auth_service

timeout = httpx.Timeout(600.0)


##########################
async def endpoint_test(prompt: str):
    response = await make_request(prompt, "pinecone")
    response2 = await make_request(prompt, "local_llm")
    logger.info(response)
    # logger.info(response2)
    if response.status_code == 200:
        print("Server is up and running!")
    else:
        print("Server is not responding.")
    return response.json()["result"], response2.json()["result"]


async def make_request(prompt, endpoint):
    async with httpx.AsyncClient(timeout=timeout) as client:
        client = auth_service.add_auth_headers(client)
        logger.info(f"Making request to {endpoint} with query {prompt}")
        request = {"query": prompt}
        response = await client.post(
            f"http://ai_driver:28001/api/v1/retrieval/{endpoint}",
            json=request,
        )
        logger.debug(response.text)
        return response


def create_dnd_qa() -> gr.Blocks:
    with gr.Blocks() as question_tab:
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
    return question_tab
