import streamlit as st


def set_button_style():
    st.markdown(
        """
        <style>
        .stButton > button {
            width: 100%;  # Adjust this value as needed
            height: 20%;  # Adjust this value as needed
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
