import gradio as gr
import httpx
from loguru import logger
import asyncio
from dungeon_driver.webui.auth import AuthService, auth_service

client = httpx.Client()  # Create a client instance


async def login(email: str, password: str):
    # Delegate the login process to the auth_service instance
    token_data = await auth_service.login(email, password)
    logger.info(token_data)
    return token_data


async def get_current_user():
    # Delegate the retrieval of the current user to the auth_service instance
    user_data = await auth_service.get_current_user()
    return user_data


def create_login_interface():
    with gr.Blocks() as login_tab:
        gr.Markdown("# Login")
        with gr.Row():
            email_input = gr.Textbox("admin@api.com", label="Email")
            password_input = gr.Textbox("CHANGEME", label="Password")
            login_button = gr.Button("Login")
            login_button.click(
                login,  # Using the wrapper function here
                inputs=[email_input, password_input],
                outputs=[],
            )
        with gr.Row():
            user_info = gr.Textbox("", label="User Info")

            check_auth_button = gr.Button("Check Authentication")
            check_auth_button.click(
                get_current_user,
                inputs=[],  # Assuming you store the token in session_id_label
                outputs=[user_info],
            )

    return login_tab
