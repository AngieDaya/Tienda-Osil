import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use("Agg") #Sirve para evitar problemas al renderizar gráficos en Streamlit, especialmente en entornos sin interfaz gráfica (como servidores).

# ─────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Tienda OSIL",
    page_icon="🏪",
    layout="wide", #ocupa todo el ancho de la pantalla
    initial_sidebar_state="expanded", #la barrita de la derecha, que sirve para subir y bajar
)

# ─────────────────────────────────────────────
# ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap'); /* import de la fuente de texto general */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&display=swap');

/* Base */ 
/* fuente general para toda la app */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Fondo general */ 
.stApp {
    background-color: #0d0d0d;
    color: #f0ece0;
}

/* Sidebar */
/* barra lateral, que es la barra de la izquierda, donde se puede subir y bajar, y también tiene el botón de cerrar sesión */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #111 0%, #1a1a1a 100%); /* degradado sutil para dar profundidad */
    border-right: 1px solid #2a2a2a; /* borde que separa el contenido principal de la barra lateral izquierda */
}
[data-testid="stSidebar"] * { 
    color: #f0ece0 !important;
}

/* Tarjeta / contenedor */
.osil-card {
    background: #161616;
    border: 1px solid #2c2c2c;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
}

/* Título principal */
.osil-title {
    font-family: "Oswald", sans-serif;
    font-weight: 800;
    font-size: 3.8rem;
    color: #428af5;
    letter-spacing: -1px;
    line-height: 1.1;
}

.osil-subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #888;
    margin-top: 0.2rem;
}

/* Badge de rango */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.badge-jefe    { background: #428af5; color: #0d0d0d; }
.badge-gerente { background: #4ade80; color: #0d0d0d; }
.badge-empleado{ background: #60a5fa; color: #0d0d0d; }

/* Métricas personalizadas */
.metric-box {
    background: #1c1c1c;
    border: 1px solid #2c2c2c;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    color: #428af5;
}
.metric-label {
    font-size: 0.75rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 2px;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #f0ece0 !important;
    font-family: 'Space Mono', monospace !important;
}

/* Botones */
.stButton > button {
    background: #428af5 !important;
    color: #0d0d0d !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #ffd966 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(245,197,66,0.3) !important;
}

/* Alerts */
.stSuccess { background: #0f2a1a !important; border-left: 3px solid #4ade80 !important; }
.stError   { background: #2a0f0f !important; border-left: 3px solid #f87171 !important; }
.stWarning { background: #2a1f0f !important; border-left: 3px solid #fb923c !important; }
.stInfo    { background: #0f1e2a !important; border-left: 3px solid #60a5fa !important; }

/* Dataframe */
.dataframe { font-family: 'Space Mono', monospace !important; font-size: 0.8rem !important; }
[data-testid="stDataFrameResizable"] {
    border: 1px solid #2c2c2c !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Divider */
hr { border-color: #2c2c2c !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #161616; border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { color: #888 !important; font-family: 'Syne', sans-serif !important; border-radius: 7px !important; }
.stTabs [aria-selected="true"] { background: #428af5 !important; color: #0d0d0d !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
</style>
""", unsafe_allow_html=True) #Permite que el código HTML y CSS se renderice correctamente en Streamlit


# ─────────────────────────────────────────────
# LÓGICA DE PYTHON / ARCHIVOS
# ─────────────────────────────────────────────

USUARIOS_FILE = "usuarios.txt"
INVENTARIO_FILE = "inventario.txt"
VENTAS_FILE = "ventas.txt"


def usuario_jefe():
    """Crea el usuario jefe/jefe/jefe si no existe."""
    nuevo_usuario = ""
    existe = False

    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 3:
                    continue

                nombre, contraseña, rango = datos

                if nombre == "jefe":
                    existe = True

                nuevo_usuario += linea

        if not existe:
            nuevo_usuario += "jefe/jefe/jefe\n"

        with open(USUARIOS_FILE, "w", encoding="utf-8") as archivo:
            archivo.write(nuevo_usuario)

    except FileNotFoundError:
        nuevo_usuario = "jefe/jefe/jefe\n"
        with open(USUARIOS_FILE, "w", encoding="utf-8") as archivo:
            archivo.write(nuevo_usuario)


def verificar_login(usuario, contraseña):
    """
    Devuelve el rango si el usuario y la contraseña son correctos.
    """
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 3:
                    continue

                nombre, clave, rango = datos

                if nombre == usuario and clave == contraseña:
                    return rango

    except FileNotFoundError:
        return None

    return None


def registrar_usuario(nombre_usuario, contraseña_usuario, rango_usuario):
    """
    Retorna (estado, mensaje) para mostrarlo en Streamlit.
    """
    estado = False
    nuevo_usuario = ""

    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 3:
                    continue

                nombre, contraseña, rango = datos

                if nombre == nombre_usuario:
                    estado = True

                nuevo_usuario += linea

        if estado:
            return False, "El nombre de usuario ya existe."

        nuevo_usuario += f"{nombre_usuario}/{contraseña_usuario}/{rango_usuario}\n"

        with open(USUARIOS_FILE, "w", encoding="utf-8") as archivo:
            archivo.write(nuevo_usuario)

        return True, "Usuario registrado exitosamente."

    except FileNotFoundError:
        nuevo_usuario += f"{nombre_usuario}/{contraseña_usuario}/{rango_usuario}\n"
        with open(USUARIOS_FILE, "w", encoding="utf-8") as archivo:
            archivo.write(nuevo_usuario)
        return True, "El archivo no existía; se creó y el usuario fue registrado."


def cambiar_contraseña(usuario, nueva):
    """Cambia la contraseña del usuario indicado."""
    nuevo_texto = ""
    encontrado = False

    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 3:
                    continue

                n, c, r = datos

                if n == usuario and not encontrado:
                    nuevo_texto += n + "/" + nueva + "/" + r + "\n"
                    encontrado = True
                else:
                    nuevo_texto += linea

        with open(USUARIOS_FILE, "w", encoding="utf-8") as archivo:
            archivo.write(nuevo_texto)

        return encontrado

    except FileNotFoundError:
        return False


def leer_inventario():
    """Lee inventario.txt y lo devuelve como lista de diccionarios para la página."""
    productos = []

    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 4:
                    continue

                nombre, cantidad, precio, fecha = datos
                productos.append({
                    "Nombre": nombre,
                    "Cantidad": int(cantidad),
                    "Precio": float(precio),
                    "Fecha": fecha,
                })

    except FileNotFoundError:
        pass

    return productos


def buscar_producto(nombre):
    """Busca un producto por nombre y devuelve sus datos, o None si no existe."""
    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 4:
                    continue

                n, c, p, f = datos

                if n == nombre:
                    return {
                        "Nombre": n,
                        "Cantidad": int(c),
                        "Precio": float(p),
                        "Fecha": f,
                    }

    except FileNotFoundError:
        return None

    return None

def registrar_producto(nombre, cantidad, precio):
    """
    Retorna True si actualizó un producto existente y False si creó uno nuevo.
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")

    nuevo_texto = ""
    existe = False

    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 4:
                    continue

                n, c, p, f = datos

                if n == nombre:
                    nueva_cantidad = int(c) + cantidad
                    nuevo_texto += n + "/" + str(nueva_cantidad) + "/" + str(precio) + "/" + f + "\n"
                    existe = True
                else:
                    nuevo_texto += linea

    except FileNotFoundError:
        pass

    if not existe:
        nuevo_texto += nombre + "/" + str(cantidad) + "/" + str(precio) + "/" + fecha + "\n"

    with open(INVENTARIO_FILE, "w", encoding="utf-8") as archivo:
        archivo.write(nuevo_texto)

    return existe


def registrar_venta(nombre, cantidad_vendida):
    """
    Estados: ok, stock_insuficiente, no_encontrado, no_inventario.
    """
    nuevo_inventario = ""
    encontrado = False
    stock_insuficiente = False
    precio_usado = None

    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 4:
                    continue

                n, c, p, f = datos

                if n == nombre:
                    encontrado = True

                    if cantidad_vendida <= int(c):
                        nueva_cantidad = int(c) - cantidad_vendida
                        nuevo_inventario += n + "/" + str(nueva_cantidad) + "/" + p + "/" + f + "\n"
                        precio_usado = p
                    else:
                        stock_insuficiente = True
                        nuevo_inventario += linea
                else:
                    nuevo_inventario += linea

        with open(INVENTARIO_FILE, "w", encoding="utf-8") as archivo:
            archivo.write(nuevo_inventario)

        if not encontrado:
            return "no_encontrado", None

        if stock_insuficiente:
            return "stock_insuficiente", None

        total = registrar_venta_archivo(nombre, cantidad_vendida, precio_usado)
        return "ok", total

    except FileNotFoundError:
        return "no_inventario", None


def registrar_venta_archivo(nombre, cantidad, precio):
    """Guarda la venta en ventas.txt"""
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    total = float(precio) * cantidad

    with open(VENTAS_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(nombre + "/" + str(cantidad) + "/" + str(total) + "/" + fecha + "\n")

    return total


def leer_ventas():
    """Lee ventas.txt y lo devuelve como lista de diccionarios para la página."""
    ventas = []

    try:
        with open(VENTAS_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 4:
                    continue

                producto, cantidad, total, fecha = datos
                ventas.append({
                    "Producto": producto,
                    "Cantidad": int(cantidad),
                    "Total": float(total),
                    "Fecha": fecha,
                })

    except FileNotFoundError:
        pass

    return ventas


def leer_usuarios():
    """Lee usuarios.txt y oculta contraseñas en la vista web."""
    usuarios = []

    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split("/")

                if len(datos) < 3:
                    continue

                nombre, contraseña, rango = datos
                usuarios.append({"Usuario": nombre, "Rango": rango})

    except FileNotFoundError:
        pass

    return usuarios


def reporte_ventas():
    """
    Devuelve datos listos para tablas y gráficos en Streamlit.
    """
    ventas = leer_ventas()
    inventario = leer_inventario()

    if not ventas:
        return None

    total_dinero = sum(venta["Total"] for venta in ventas)
    total_unidades = sum(venta["Cantidad"] for venta in ventas)
    stock_bajo = [producto for producto in inventario if producto["Cantidad"] <= 5]

    return {
        "ventas": ventas,
        "inventario": inventario,
        "total_dinero": total_dinero,
        "total_unidades": total_unidades,
        "stock_bajo": stock_bajo,
    }


# Alias para no romper ninguna llamada previa de la página.
_usuario_jefe = usuario_jefe
_verificar_login = verificar_login
_registrar_usuario = registrar_usuario
_cambiar_contrasena = cambiar_contraseña
_leer_inventario = leer_inventario
_registrar_producto = registrar_producto
_registrar_venta = registrar_venta
_leer_ventas = leer_ventas
_leer_usuarios = leer_usuarios


# ─────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────
usuario_jefe()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = ""
    st.session_state.rango = ""
    st.session_state.intentos = 0


# ─────────────────────────────────────────────
# PANTALLA DE LOGIN
# ─────────────────────────────────────────────
def pantalla_login():
    col_l, col_c, col_r = st.columns([1, 1.4, 1]) #crea tres columnas, la del medio es un poco más ancha que las otras dos, para centrar el contenido de login
    with col_c:
        st.markdown('<div class="osil-title">TIENDA OSIL</div>', unsafe_allow_html=True) #el markdown permite escribir código HTML dentro de Streamlit
        st.markdown('<div class="osil-subtitle">Sistema de gestión · v1.0</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True) #salto de línea para separar el subtítulo "sistema de gestión""

        st.markdown("#### Iniciar sesión") #titulo en negrilla

        usuario = st.text_input("Usuario", placeholder="Ingrese su usuario", key="login_usuario")
        contrasena = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña", key="login_pass")

        if st.session_state.intentos >= 3:
            st.error("Usuario bloqueado. Demasiados intentos fallidos.")
        else:
            if st.button("Entrar →", use_container_width=True): #el use_container_width hace que el botón ocupe todo el ancho disponible, para que se vea más grande y fácil de clicar
                if usuario.strip() and contrasena.strip():
                    rango = verificar_login(usuario.strip().lower(), contrasena.strip())
                    if rango:
                        st.session_state.logged_in = True
                        st.session_state.usuario = usuario.strip().lower()
                        st.session_state.rango = rango
                        st.session_state.intentos = 0
                        st.rerun()
                    else:
                        st.session_state.intentos += 1
                        restantes = 3 - st.session_state.intentos
                        st.error(f"Credenciales incorrectas. Intentos restantes: {restantes}")
                else:
                    st.warning("Por favor complete todos los campos.")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;margin-top:1.5rem;font-family:\'Space Mono\',monospace;'
            'font-size:0.7rem;color:#444;">© Tienda OSIL · Todos los derechos reservados</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="osil-title" style="font-size:1.8rem">TIENDA OSIL</div>', unsafe_allow_html=True)
        st.markdown('<div class="osil-subtitle">Sistema de gestión</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        rango = st.session_state.rango
        badge_class = f"badge-{rango}" #clase CSS para el badge, que cambia de color según el rango del usuario (jefe, gerente o empleado)
        st.markdown(
            f'<span style="font-family:\'Space Mono\',monospace;font-size:0.85rem;color:#aaa;">{st.session_state.usuario}</span>' 
            f'&nbsp;&nbsp;<span class="badge {badge_class}">{rango}</span>', #muestra el nombre del usuario y su rango en la barra lateral, con un badge de color que indica su rango (jefe, gerente o empleado)
            unsafe_allow_html=True,
        )
        st.markdown("---") #línea divisoria para separar la información del usuario de las opciones del menú

        opciones = []
        if rango in ("jefe", "gerente"):
            opciones = ["Dashboard", "Usuarios", "Inventario", "Ventas", "Reportes"]
        else:
            opciones = ["Dashboard", "Inventario", "Ventas", "Reportes"]

        if "pagina" not in st.session_state:
            st.session_state.pagina = "Dashboard" #página que abre siempre al iniciar sesión, que es el dashboard

        for op in opciones:
            active = "background:#428af5;color:#0d0d0d;border-radius:8px;" if st.session_state.pagina == op else "" #estilo para resaltar la opción del menú que está activa (la página que se está viendo actualmente)
            if st.button(op, key=f"nav_{op}", use_container_width=True): 
                st.session_state.pagina = op #actualiza la página actual en el estado de la sesión, para que se muestre el contenido correspondiente a esa página
                st.rerun() #reinicia la aplicación para que se renderice la nueva página seleccionada

        st.markdown("---")
        if st.button("Cerrar sesión", use_container_width=True):
            for k in ["logged_in", "usuario", "rango", "intentos", "pagina"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()


# ─────────────────────────────────────────────
# PÁGINAS
# ─────────────────────────────────────────────

def pagina_dashboard():
    st.markdown('<div class="osil-title" style="font-size:2rem">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="osil-subtitle">Resumen general del sistema</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    inventario = leer_inventario()
    ventas = leer_ventas()

    total_productos = len(inventario)
    total_stock = sum(p["Cantidad"] for p in inventario)
    total_ventas = len(ventas)
    ingreso_total = sum(v["Total"] for v in ventas)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-value">{total_productos}</div><div class="metric-label">Productos</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-value">{total_stock}</div><div class="metric-label">Unidades en stock</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-value">{total_ventas}</div><div class="metric-label">Ventas realizadas</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-box"><div class="metric-value">${ingreso_total:,.0f}</div><div class="metric-label">Ingresos totales</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Stock bajo (≤ 5 unidades)")
        bajo = [p for p in inventario if p["Cantidad"] <= 5]
        if bajo:
            df = pd.DataFrame(bajo)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay productos con stock bajo.")

    with col2:
        st.markdown("#### Últimas 5 ventas")
        if ventas:
            df = pd.DataFrame(ventas[-5:][::-1])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay ventas registradas.")


def pagina_usuarios():
    st.markdown('<div class="osil-title" style="font-size:2rem">Usuarios</div>', unsafe_allow_html=True)
    st.markdown('<div class="osil-subtitle">Gestión de cuentas del sistema</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    button[data-baseweb="tab"] {
        margin-right: 40px; /* separación entre tabs */
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Ver usuarios", "Registrar usuario", "Cambiar contraseña"])

    with tab1:
        usuarios = leer_usuarios()
        if usuarios:
            df = pd.DataFrame(usuarios)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay usuarios.")

    with tab2:
        st.markdown("#### Nuevo usuario")
        col1, col2 = st.columns(2)
        with col1:
            nuevo_nombre = st.text_input("Nombre de usuario", key="reg_nombre")
        with col2:
            nuevo_rango = st.selectbox("Rango", ["empleado", "gerente"], key="reg_rango")
        nueva_pass = st.text_input("Contraseña (mínimo 8 caracteres, sin espacios)", type="password", key="reg_pass")

        if st.button("Registrar usuario"):
            nombre = nuevo_nombre.strip().lower()
            if not nombre:
                st.error("El nombre no puede estar vacío.")
            elif " " in nombre:
                st.error("El nombre no debe contener espacios.")
            elif len(nueva_pass) < 8 or " " in nueva_pass:
                st.error("La contraseña debe tener al menos 8 caracteres y sin espacios.")
            else:
                ok, msg = registrar_usuario(nombre, nueva_pass, nuevo_rango)
                if ok:
                    st.success(f"{msg}")
                else:
                    st.error(f"{msg}")

    with tab3:
        st.markdown("#### Cambiar contraseña")
        col1, col2 = st.columns(2)
        with col1:
            usr_cambio = st.text_input("Usuario", key="cambio_usr")
        with col2:
            pass_nueva = st.text_input("Nueva contraseña", type="password", key="cambio_pass")

        if st.button("Actualizar contraseña"):
            usuario = usr_cambio.strip().lower()
            if not usuario:
                st.error("Ingrese el nombre de usuario.")
            elif len(pass_nueva) < 8 or " " in pass_nueva:
                st.error("La contraseña debe tener al menos 8 caracteres y sin espacios.")
            else:
                ok = cambiar_contraseña(usuario, pass_nueva)
                if ok:
                    st.success("Contraseña actualizada.")
                else:
                    st.error("Usuario no encontrado.")


def pagina_inventario():
    st.markdown('<div class="osil-title" style="font-size:2rem">Inventario</div>', unsafe_allow_html=True)
    st.markdown('<div class="osil-subtitle">Control de productos y stock</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    button[data-baseweb="tab"] {
        margin-right: 40px; /* separación entre tabs */
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Ver inventario", "Registrar producto", "Buscar producto"])

    with tab1:
        inventario = leer_inventario()
        if inventario:
            df = pd.DataFrame(inventario)
            # Resaltar stock bajo
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(inventario)} productos · {sum(p['Cantidad'] for p in inventario)} unidades")
        else:
            st.info("El inventario está vacío.")

    with tab2:
        st.markdown("#### Agregar / actualizar producto")
        col1, col2, col3 = st.columns(3)
        with col1:
            prod_nombre = st.text_input("Nombre del producto", key="inv_nombre", placeholder="Ej: manzana")
        with col2:
            prod_cantidad = st.number_input("Cantidad", min_value=1, step=1, key="inv_cantidad")
        with col3:
            prod_precio = st.number_input("Precio unitario", min_value=0.01, step=0.01, format="%.2f", key="inv_precio")

        if st.button("Guardar producto"):
            nombre = prod_nombre.strip().lower()
            if not nombre:
                st.error("El nombre no puede estar vacío.")
            elif prod_cantidad <= 0:
                st.error("La cantidad debe ser mayor a 0.")
            elif prod_precio <= 0:
                st.error("El precio debe ser mayor a 0.")
            else:
                actualizado = registrar_producto(nombre, int(prod_cantidad), prod_precio)
                if actualizado:
                    st.success(f"Producto '{nombre}' actualizado en inventario.")
                else:
                    st.success(f"Producto '{nombre}' registrado exitosamente.")

    with tab3:
        st.markdown("#### Buscar producto")
        busqueda = st.text_input("Nombre del producto", key="busq_nombre", placeholder="Escriba el nombre...")
        if st.button("Buscar"):
            nombre = busqueda.strip().lower()
            inventario = leer_inventario()
            resultado = next((p for p in inventario if p["Nombre"] == nombre), None)
            if resultado:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Producto", resultado["Nombre"].capitalize())
                c2.metric("Cantidad", resultado["Cantidad"])
                c3.metric("Precio", f"${resultado['Precio']:.2f}")
                c4.metric("Registrado", resultado["Fecha"])
            else:
                st.warning("Producto no encontrado.")


def pagina_ventas():
    st.markdown('<div class="osil-title" style="font-size:2rem">Ventas</div>', unsafe_allow_html=True)
    st.markdown('<div class="osil-subtitle">Registro de transacciones</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    button[data-baseweb="tab"] {
        margin-right: 40px; /* separación entre tabs */
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Registrar venta", "Historial de ventas"])

    with tab1:
        st.markdown("#### Nueva venta")

        inventario = leer_inventario()
        if not inventario:
            st.warning("No hay productos en inventario.")
            return

        productos_disponibles = [p["Nombre"] for p in inventario if p["Cantidad"] > 0]

        col1, col2 = st.columns(2)
        with col1:
            prod_venta = st.selectbox("Producto", productos_disponibles, key="venta_prod")
        with col2:
            prod_info = next((p for p in inventario if p["Nombre"] == prod_venta), None)
            stock_actual = prod_info["Cantidad"] if prod_info else 0
            st.markdown(f"**Stock disponible:** {stock_actual} unidades")
            cantidad_venta = st.number_input("Cantidad a vender", min_value=0, max_value=stock_actual, step=1, key="venta_cantidad")

        if prod_info:
            subtotal = prod_info["Precio"] * cantidad_venta
            st.markdown(
                f'<div class="metric-box" style="max-width:250px;">'
                f'<div class="metric-value">${subtotal:,.2f}</div>'
                f'<div class="metric-label">Total a cobrar</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Confirmar venta", use_container_width=False):
            resultado, total = registrar_venta(prod_venta, int(cantidad_venta))
            if resultado == "ok":
                st.success(f"Venta registrada. Total: ${total:,.2f}")
                st.balloons()
            elif resultado == "stock_insuficiente":
                st.error("Stock insuficiente.")
            elif resultado == "no_encontrado":
                st.error("Producto no encontrado.")
            else:
                st.error("No hay inventario.")

    with tab2:
        ventas = leer_ventas()
        if ventas:
            df = pd.DataFrame(ventas[::-1])
            df["Total"] = df["Total"].apply(lambda x: f"${x:,.2f}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay ventas registradas.")


def pagina_reportes():
    st.markdown('<div class="osil-title" style="font-size:2rem">Reportes</div>', unsafe_allow_html=True)
    st.markdown('<div class="osil-subtitle">Análisis de ventas e inventario</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    ventas = leer_ventas()
    inventario = leer_inventario()

    if not ventas:
        st.info("No hay datos de ventas para mostrar reportes.")
        return

    df_ventas = pd.DataFrame(ventas)

    # Agrupaciones
    ventas_por_producto = df_ventas.groupby("Producto").agg(
        Unidades=("Cantidad", "sum"),
        Ingresos=("Total", "sum"),
    ).reset_index().sort_values("Unidades", ascending=False)

    ventas_por_fecha = df_ventas.groupby("Fecha").agg(
        Total=("Total", "sum")
    ).reset_index().sort_values("Fecha")

    DARK_BG  = "#161616"
    ACCENT   = "#428af5"
    SECONDARY= "#60a5fa"
    TEXT     = "#f0ece0"
    GRID     = "#2a2a2a"
    matplotlib.rcParams.update({
        "figure.facecolor": DARK_BG,
        "axes.facecolor":   DARK_BG,
        "axes.edgecolor":   GRID,
        "axes.labelcolor":  TEXT,
        "xtick.color":      TEXT,
        "ytick.color":      TEXT,
        "text.color":       TEXT,
        "grid.color":       GRID,
        "font.family":      "monospace",
    })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top productos vendidos")
        fig, ax = plt.subplots(figsize=(6, 4))
        top = ventas_por_producto.head(6)
        bars = ax.barh(top["Producto"], top["Unidades"], color=ACCENT, height=0.6, edgecolor="none")
        ax.set_xlabel("Unidades vendidas")
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.3)
        ax.spines[["top", "right", "left"]].set_visible(False)
        for bar in bars:
            ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                    str(int(bar.get_width())), va="center", fontsize=9, color=TEXT)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Participación de ingresos")
        fig, ax = plt.subplots(figsize=(6, 4))
        colors_pie = [ACCENT, SECONDARY, "#4ade80", "#f87171", "#fb923c", "#a78bfa"]
        top6 = ventas_por_producto.head(6)
        wedges, texts, autotexts = ax.pie(
            top6["Ingresos"],
            labels=top6["Producto"],
            autopct="%1.1f%%",
            colors=colors_pie[:len(top6)],
            startangle=140,
            wedgeprops={"edgecolor": DARK_BG, "linewidth": 2},
        )
        for t in texts + autotexts:
            t.set_color(TEXT)
            t.set_fontsize(9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("#### Ingresos por fecha")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.fill_between(ventas_por_fecha["Fecha"], ventas_por_fecha["Total"],
                    alpha=0.3, color=ACCENT)
    ax.plot(ventas_por_fecha["Fecha"], ventas_por_fecha["Total"],
            color=ACCENT, linewidth=2, marker="o", markersize=5)
    ax.set_ylabel("Ingresos ($)")
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Productos con stock bajo (≤ 5)")
        bajo = [p for p in inventario if p["Cantidad"] <= 5]
        if bajo:
            df_bajo = pd.DataFrame(bajo)
            st.dataframe(df_bajo, use_container_width=True, hide_index=True)
        else:
            st.success("Todos los productos tienen stock suficiente.")

    with col4:
        st.markdown("#### Resumen financiero")
        total_ingresos = df_ventas["Total"].sum()
        producto_estrella = ventas_por_producto.iloc[0]["Producto"] if not ventas_por_producto.empty else "—"
        unidades_estrella = ventas_por_producto.iloc[0]["Unidades"] if not ventas_por_producto.empty else 0

        st.markdown(
            f'<div class="metric-box" style="margin-bottom:1rem;">'
            f'<div class="metric-value">${total_ingresos:,.2f}</div>'
            f'<div class="metric-label">Ingresos totales</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-box">'
            f'<div class="metric-value" style="font-size:1.2rem">{producto_estrella.capitalize()}</div>'
            f'<div class="metric-label">Producto más vendido · {unidades_estrella} unidades</div></div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    if not st.session_state.logged_in:
        pantalla_login()
        return

    render_sidebar()

    pagina = st.session_state.get("pagina", "Dashboard")

    if pagina == "Dashboard":
        pagina_dashboard()
    elif pagina == "Usuarios":
        if st.session_state.rango in ("jefe", "gerente"):
            pagina_usuarios()
        else:
            st.error("Acceso denegado.")
    elif pagina == "Inventario":
        pagina_inventario()
    elif pagina == "Ventas":
        pagina_ventas()
    elif pagina == "Reportes":
        pagina_reportes()


main()