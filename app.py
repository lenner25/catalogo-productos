import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Catálogo JK", layout="wide")

# =========================
# CONFIG
# =========================
DATA_FILE = "productos.csv"
IMG_FOLDER = "imagenes"
WHATSAPP = "50588065551"

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

os.makedirs(IMG_FOLDER, exist_ok=True)

# Crear archivo si no existe
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["nombre", "precio", "estado", "imagen"])
    df.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

# =========================
# SESSION LOGIN
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN UI
# =========================
st.sidebar.title("🔐 Administración")

if not st.session_state.logged_in:
    user = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Ingresar"):
        if user == ADMIN_USER and password == ADMIN_PASS:
            st.session_state.logged_in = True
            st.sidebar.success("Bienvenido administrador")
        else:
            st.sidebar.error("Credenciales incorrectas")

else:
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False

# =========================
# ESTILOS
# =========================
st.markdown("""
    <style>
    .card {
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        background-color: #ffffff;
    }
    .precio {
        font-size: 22px;
        font-weight: bold;
        color: #27ae60;
    }
    .vendido {
        color: red;
        font-weight: bold;
    }
    .disponible {
        color: green;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🛍️ Catálogo de Productos JKM")

# =========================
# FILTROS
# =========================
st.sidebar.header("🔍 Filtros")

filtro_estado = st.sidebar.selectbox(
    "Estado",
    ["Todos", "Disponible", "Vendido"]
)

busqueda = st.sidebar.text_input("Buscar producto")

# =========================
# FORMULARIO (SOLO ADMIN)
# =========================
if st.session_state.logged_in:
    st.sidebar.header("➕ Agregar producto")

    nombre = st.sidebar.text_input("Nombre")
    precio = st.sidebar.number_input("Precio", min_value=0)
    estado = st.sidebar.selectbox("Estado producto", ["Disponible", "Vendido"])
    imagen = st.sidebar.file_uploader("Imagen", type=["jpg", "png"])

    if st.sidebar.button("Guardar"):
        if nombre and imagen:
            ruta = os.path.join(IMG_FOLDER, imagen.name)

            with open(ruta, "wb") as f:
                f.write(imagen.getbuffer())

            nuevo = pd.DataFrame([[nombre, precio, estado, ruta]],
                                 columns=df.columns)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.sidebar.success("Producto agregado")

# =========================
# FILTRO DE DATOS
# =========================
df_filtrado = df.copy()

if filtro_estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["estado"] == filtro_estado]

if busqueda:
    df_filtrado = df_filtrado[df_filtrado["nombre"].str.contains(busqueda, case=False)]

# =========================
# CATÁLOGO
# =========================
cols = st.columns(4)

for i, row in df_filtrado.iterrows():
    col = cols[i % 4]

    with col:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        
        st.image(row["imagen"], use_container_width=True)
        st.subheader(row["nombre"])
        st.markdown(f'<div class="precio">$ {row["precio"]}</div>', unsafe_allow_html=True)

        if row["estado"] == "Disponible":
            st.markdown('<div class="disponible">🟢 Disponible</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="vendido">🔴 Vendido</div>', unsafe_allow_html=True)

        mensaje = f"Hola, me interesa el producto: {row['nombre']}"
        url = f"https://wa.me/{WHATSAPP}?text={mensaje.replace(' ', '%20')}"

        st.markdown(f"[📲 Consultar por WhatsApp]({url})")

        st.markdown('</div>', unsafe_allow_html=True)