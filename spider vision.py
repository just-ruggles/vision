import os
import base64
import streamlit as st
from openai import OpenAI


# Configuración general de la página
st.set_page_config(page_title="🕷️ Spider-Vision", layout="centered", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://pbs.twimg.com/media/F2sr38KWYAAj0bc.jpg:large");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 💅 Estilos personalizados
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        color: #FF3131;
        text-align: center;
        font-size: 50px;
        text-shadow: 2px 2px 10px black;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        background-color: #1e1e1e !important;
        color: white !important;
        border-radius: 8px;
        border: 1px solid #555;
    }
    .stButton > button {
        background-color: #FF3131;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 20px;
    }
    .stExpanderHeader {
        font-weight: bold;
        color: #FF3131 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🕸️ Título principal
st.title("🕷️ SPIDER-VISION")

# 🧠 Función para codificar la imagen a base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# 🔑 Ingreso de API Key
ke = st.text_input("🔐 Ingresa tu clave de OpenAI", type="password")
if ke:
    os.environ["OPENAI_API_KEY"] = ke
    api_key = ke
    client = OpenAI(api_key=api_key)
else:
    api_key = None

# 📤 Subida de imagen
uploaded_file = st.file_uploader("📸 Sube una imagen", type=["jpg", "jpeg", "png"])

# Mostrar imagen si fue cargada
if uploaded_file:
    with st.expander("📷 Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# 📝 Input adicional opcional
show_details = st.toggle("🗒️ Añadir detalles sobre la imagen")
additional_details = ""
if show_details:
    additional_details = st.text_area("Agrega aquí un poco de contexto:")

# 🧪 Botón para analizar imagen
analyze_button = st.button("🔍 Analizar imagen")

# 🧠 Procesamiento de imagen
if uploaded_file and api_key and analyze_button:
    with st.spinner("🧠 Analizando la imagen..."):
        try:
            base64_image = encode_image(uploaded_file)
            prompt_text = "Describe lo que ves en la imagen, en español."

            if additional_details:
                prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ]

            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True,
            ):
                if completion.choices[0].delta.content:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Ocurrió un error al analizar la imagen: {e}")

# 🧯 Validaciones
if analyze_button and not uploaded_file:
    st.warning("⚠️ Debes subir una imagen para analizar.")
elif analyze_button and not api_key:
    st.warning("⚠️ Ingresa tu clave de API para continuar.")
