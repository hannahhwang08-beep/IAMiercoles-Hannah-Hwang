from groq import Groq
import streamlit as st


st.set_page_config(page_title="El chat de IA de Hannah Hwang", page_icon="👍")
st.title("La primera aplicacion con Streamlit de Hannah Hwang")


nombre = st.text_input("Cual es tu nombre?")
if st.button("Saludar!"):
    st.write(f"Hola {nombre}! Bienvenido a talento tech")


MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile']


def configurar_pagina():
    st.title("Mi Chat de IA - Hannah Hwang")
    st.sidebar.title("Configuracion de la IA")


    elegirModelo = st.sidebar.selectbox(
        "Elegi un modelo",
        options = MODELOS,
        index = 0
    )


    return elegirModelo


def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key= clave_secreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role":"user", "content": mensajeDeEntrada}],
        stream=False
    )


def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat: mostrar_historial()



clienteUsuario = crear_usuario_groq()
inicializar_estado()
modelo = configurar_pagina()
area_chat()
mensaje = st.chat_input("Escribi tu mensaje:")


#-----Dentro del condicional-------------------------------------
if mensaje:
    actualizar_historial("user", mensaje, "😁")
    chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
    actualizar_historial("assistant", chat_completo, "🤖")
    st.rerun()