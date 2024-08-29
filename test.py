import streamlit as st
import streamlit.components.v1 as components


# Function to inject custom CSS
def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Upload or link to your background image
background_image_url = "C:/Users/suhas/PycharmProjects/PC_Part_Picker_LLM/Fut_PC_AI.jpeg"

# Set the background image
set_background_image(background_image_url)

# Your Streamlit app code
st.title("My Streamlit App with Background Image")
st.write("Welcome to my app with a custom background image!")
