from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    # print(response[0])
    return response


def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        image_parts = [
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No fole uploaded")


st.set_page_config(page_title="Multilanguage Invoice Extractor")

st.header("Image data extraction Application")

upload_file = st.file_uploader("choose an image of invoice...", type=["jpg", "jpeg", "png"])
image = ""

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

input = st.text_input("Input Prompt: ", key="imput")
submit = st.button("Submit Query")

input_prompt = """ 
You are an expert in understanding images. we will upload a images and
you will have to answer any questions based on the uploaded image
"""

input_prompt = """ 
You are an expert in understanding input images. we will upload a image and
you will have edit image according to input prompt and return edited image in jpg format. use output format {"image":edited image}.
"""

if submit:
    image_data = input_image_setup(upload_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response.text)
