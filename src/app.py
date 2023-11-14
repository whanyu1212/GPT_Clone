import streamlit as st
from openai import OpenAI
from streamlit_lottie import st_lottie
from util.css_functions import set_button_style

st.set_page_config(layout="wide")
st_lottie(
    "https://lottie.host/40f2b045-cfe3-48c1-99fb-8d9d959fad39/HZEetoX5H1.json",
    height=300,
    width=600,
    speed=1,
    # key="initial",
)
# Set your OpenAI API key from Streamlit secrets
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=st.secrets["OPENAI_API_KEY"],
)


# Default temperature
default_temperature = 0.3
available_models = ["gpt-4-1106-preview", "gpt-4", "gpt-4-32k", "gpt-4-32k-0613"]

# add_logo_to_bg_from_local("./pictures/bg.png")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

if "main_chat" not in st.session_state:
    st.session_state.main_chat = []

if "side_chat" not in st.session_state:
    st.session_state.side_chat = []


# Function to display chat history in the sidebar
def display_chat_history():
    chat_history_display = st.sidebar.empty()
    chat_history = st.session_state.side_chat

    if chat_history:
        chat_history_with_linebreaks = ""
        for index, message in enumerate(chat_history):
            content = message["content"]
            if index % 2 == 0:
                content = f"User: {content}"  # Add user prompt prefix for even indexed messages
            else:
                content = f"Assistant: {content}"  # Add assistant response prefix for odd indexed messages
            chat_history_with_linebreaks += f"{content}<hr>"

        chat_history_display.markdown(
            chat_history_with_linebreaks, unsafe_allow_html=True
        )

    return chat_history_display


# Create a container for the chat history
chat_history_container = display_chat_history()


# Function to handle user prompt and generate assistant response
def generate_response(prompt):
    st.session_state.main_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.main_chat
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.main_chat.append({"role": "assistant", "content": full_response})
    st.session_state.side_chat.append({"role": "user", "content": prompt})
    st.session_state.side_chat.append({"role": "assistant", "content": full_response})


# Function to handle "Clear Chat" button click
def handle_clear_chat():
    st.session_state.main_chat = []


# Main function
def main():
    st.title("J.A.R.V.I.S")
    set_button_style()

    st.sidebar.subheader("Filters")
    st.sidebar.selectbox("Select Model", available_models)
    st.sidebar.slider(
        "Temperature", min_value=0.1, max_value=1.0, value=default_temperature, step=0.1
    )

    st.sidebar.subheader("Chat History")

    display_chat_history()

    prompt = st.chat_input("At your service, Sir")
    if "stop_streaming" not in st.session_state:
        st.session_state.stop_streaming = False

    # Create two buttons side by side using columns
    col1, col2, col3 = st.sidebar.columns(3)

    # Place "Clear Chat" button in the first column
    if col3.button("Clear Chat"):
        handle_clear_chat()

    if prompt:
        generate_response(prompt)


# Call the main function
if __name__ == "__main__":
    main()
