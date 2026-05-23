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

/* Badge de rango. Estilo para el badge que muestra el rango del usuario (jefe, gerente o empleado) junto a su nombre en la barra lateral, con colores distintivos para cada rango y un diseño moderno y llamativo para resaltar esa información importante. */
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
.badge-jefe    { background: #cfd916; color: #0d0d0d; }
.badge-gerente { background: #4ade80; color: #0d0d0d; }
.badge-empleado{ background: #60a5fa; color: #0d0d0d; }

/* Métricas personalizadas. Estilo para las cajas de métricas en el dashboard, que muestran información clave como total de productos, unidades en stock, ventas realizadas e ingresos totales, con un diseño moderno y llamativo para destacar esos datos importantes. */
.metric-box {
    background: #1c1c1c;
    border: 1px solid #2c2c2c;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    text-align: center;
}
.metric-value { /*estilo para el valor principal de la métrica, como el número total de productos o el ingreso total, con una fuente grande y llamativa para destacar esa información clave dentro de la caja de la métrica. */
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    color: #428af5;
}
.metric-label { /*estilo para la etiqueta de la métrica, que describe qué representa el valor principal (por ejemplo, "Productos" o "Ingresos totales"), con una fuente más pequeña y un color más suave para complementar el valor principal sin restarle protagonismo. */
    font-size: 0.75rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 2px;
}

/* Inputs. Estilo para los campos de entrada de texto, números y selectbox en toda la aplicación, con un fondo oscuro, bordes suaves y una fuente monoespaciada para dar un aspecto moderno y tecnológico a los formularios de la aplicación. */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #1e1e1e !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: #f0ece0 !important;
    font-family: 'Space Mono', monospace !important;
}

/* Botones. Estilo para los botones en toda la aplicación, con un fondo azul, texto blanco y una transición suave para mejorar la experiencia del usuario. */
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
.stButton > button:hover { /*estilo para el estado hover de los botones, que cambia el fondo a un "amarillo" más claro, eleva ligeramente el botón y agrega una sombra para dar un efecto de profundidad y resaltar la interactividad del botón cuando el usuario pasa el cursor sobre él. */
    background: #ffd966 !important;
    transform: translateY(-1px) !important; /*eleva el botón 1 píxel hacia arriba para dar un efecto de "levantar" al hacer hover.
    box-shadow: 0 4px 16px rgba(245,197,66,0.3) !important;
}

/* Alerts. Estilo para los mensajes de alerta en toda la aplicación, con colores distintivos para cada tipo de alerta (éxito, error, advertencia e información) y un borde izquierdo para resaltar su importancia. */
.stSuccess { background: #0f2a1a !important; border-left: 3px solid #4ade80 !important; }
.stError   { background: #2a0f0f !important; border-left: 3px solid #f87171 !important; }
.stWarning { background: #2a1f0f !important; border-left: 3px solid #fb923c !important; }
.stInfo    { background: #0f1e2a !important; border-left: 3px solid #60a5fa !important; }

/* Dataframe. Estilo para las tablas de datos (dataframes) en toda la aplicación, con un fondo oscuro, bordes suaves y una fuente monoespaciada para mejorar la legibilidad y dar un aspecto moderno a las tablas.
.dataframe { font-family: 'Space Mono', monospace !important; font-size: 0.8rem !important; }
[data-testid="stDataFrameResizable"] {
    border: 1px solid #2c2c2c !important; /*borde que rodea toda la tabla para darle un aspecto más definido y separado del fondo, con un color oscuro para mantener la estética general de la aplicación. */
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Divider. Estilo para los divisores (líneas horizontales) en toda la aplicación, con un color oscuro para integrarse con el diseño general y dar una separación visual suave entre secciones de contenido. */
hr { border-color: #2c2c2c !important; }

/* Tabs. Estilo para las pestañas en toda la aplicación */
.stTabs [data-baseweb="tab-list"] { background: #161616; border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { color: #888 !important; font-family: 'Syne', sans-serif !important; border-radius: 7px !important; }
.stTabs [aria-selected="true"] { background: #428af5 !important; color: #0d0d0d !important; }

/* Scrollbar. Estilo para la barra de desplazamiento (scrollbar) en toda la aplicación. */
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
        return None #Si el archivo de usuarios no existe, no se puede verificar el login, así que se devuelve None para indicar que no se encontró ningún usuario válido.

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

                if nombre == nombre_usuario: #Si el nombre de usuario que se quiere registrar ya existe en el archivo, se marca el estado como True para indicar que ya existe ese usuario, y se sigue leyendo el archivo para mantener el contenido original sin cambios.
                    estado = True

                nuevo_usuario += linea

        if estado:
            return False, "El nombre de usuario ya existe." #Si el estado es True, significa que ya se encontró un usuario con ese nombre, por lo que se devuelve False para indicar que no se pudo registrar el nuevo usuario, junto con un mensaje de error.

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

                if n == usuario and not encontrado: #Si el nombre de usuario coincide con el que se quiere cambiar la contraseña, y aún no se ha encontrado ese usuario en el proceso de lectura del archivo, entonces se actualiza la contraseña en la variable nuevo_texto, manteniendo el mismo formato de nombre/rango pero con la nueva contraseña. Además, se marca encontrado como True para evitar que si hay otro usuario con el mismo nombre (lo cual no debería pasar si el registro de usuarios es correcto) se cambie también su contraseña.
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

    return productos #Si el archivo de inventario no existe, se devuelve una lista vacía, lo que indica que no hay productos registrados en el inventario. Esto permite que la aplicación maneje correctamente la situación de un inventario vacío sin generar errores al intentar leer un archivo inexistente.


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
                        stock_insuficiente = True #Si la cantidad vendida es mayor que la cantidad disponible en el inventario, se marca stock_insuficiente como True para indicar que no se puede completar la venta debido a falta de stock. En este caso, el inventario no se actualiza y se mantiene la misma cantidad para ese producto.
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

        usuario = st.text_input("Usuario", placeholder="Ingrese su usuario", key="login_usuario") #input de texto para el nombre de usuario, con un placeholder que indica al usuario qué debe ingresar, y una clave única para identificar este input en el estado de la sesión (login_usuario)
        contrasena = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña", key="login_pass")

        if st.session_state.intentos >= 3:
            st.error("Usuario bloqueado. Demasiados intentos fallidos.")
        else:
            if st.button("Entrar →", use_container_width=True): #el use_container_width hace que el botón ocupe todo el ancho disponible, para que se vea más grande y fácil de clicar
                if usuario.strip() and contrasena.strip():
                    rango = verificar_login(usuario.strip().lower(), contrasena.strip()) #Se verifica el login con el nombre de usuario y la contraseña ingresados, después de eliminar espacios al principio y al final del nombre de usuario, y convertirlo a minúsculas para evitar problemas de mayúsculas/minúsculas. Si las credenciales son correctas, se devuelve el rango del usuario (jefe, gerente o empleado), que se almacena en la variable rango.
                    if rango:
                        st.session_state.logged_in = True #Si el rango es válido (es decir, si las credenciales son correctas), se marca logged_in como True para indicar que el usuario ha iniciado sesión correctamente, y se guardan el nombre de usuario (en minúsculas y sin espacios al principio o al final) y el rango en el estado de la sesión, para que puedan ser utilizados en otras partes de la aplicación. Luego se llama a st.rerun() para reiniciar la aplicación y mostrar la interfaz principal después del login.
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

        st.markdown("</div>", unsafe_allow_html=True) #cierra el div que se abrió al principio del markdown, para que el estilo de esa sección no afecte a otras partes de la aplicación
        st.markdown(
            '<div style="text-align:center;margin-top:1.5rem;font-family:\'Space Mono\',monospace;'
            'font-size:0.7rem;color:#444;">© Tienda OSIL · Todos los derechos reservados</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar(): #Función para renderizar la barra lateral, que se muestra después de iniciar sesión, y que contiene el nombre del usuario, su rango, las opciones de navegación y el botón de cerrar sesión.
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
            for k in ["logged_in", "usuario", "rango", "intentos", "pagina"]: #al cerrar sesión, se eliminan todas las variables relacionadas con el estado del usuario y la página actual del estado de la sesión, para que al volver a la pantalla de login no quede ningún dato residual del usuario anterior.
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()


# ─────────────────────────────────────────────
# PÁGINAS
# ─────────────────────────────────────────────

def pagina_dashboard():
    st.markdown('<div class="osil-title" style="font-size:2rem">Dashboard</div>', unsafe_allow_html=True) #título principal de la página, con un tamaño de fuente más grande para destacar que es el dashboard
    st.markdown('<div class="osil-subtitle">Resumen general del sistema</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    inventario = leer_inventario()
    ventas = leer_ventas()

    total_productos = len(inventario)
    total_stock = sum(p["Cantidad"] for p in inventario) #Suma la cantidad de cada producto en el inventario para obtener el total de unidades disponibles en stock.
    total_ventas = len(ventas)
    ingreso_total = sum(v["Total"] for v in ventas)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-box"><div class="metric-value">{total_productos}</div><div class="metric-label">Productos</div></div>', unsafe_allow_html=True) #Muestra el total de productos registrados en el inventario, contando cada producto como una unidad, sin importar su cantidad.
    with c2:
        st.markdown(f'<div class="metric-box"><div class="metric-value">{total_stock}</div><div class="metric-label">Unidades en stock</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><div class="metric-value">{total_ventas}</div><div class="metric-label">Ventas realizadas</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-box"><div class="metric-value">${ingreso_total:,.0f}</div><div class="metric-label">Ingresos totales</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True) #salto de línea para separar las métricas del resto del contenido del dashboard

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Stock bajo (≤ 5 unidades)")
        bajo = [p for p in inventario if p["Cantidad"] <= 5]
        if bajo:
            df = pd.DataFrame(bajo) #Crea un DataFrame de pandas a partir de la lista de productos con stock bajo, para mostrarlo en una tabla en Streamlit.
            st.dataframe(df, use_container_width=True, hide_index=True) #Ajusta el ancho de las columnas al contenedor disponible y ocultando la columna de índice que pandas agrega por defecto, para que se vea más limpia y centrada en la información relevante del producto (nombre, cantidad, precio, fecha).
        else:
            st.info("No hay productos con stock bajo.")

    with col2:
        st.markdown("#### Últimas 5 ventas")
        if ventas:
            df = pd.DataFrame(ventas[-5:][::-1]) #Toma las últimas 5 ventas de la lista de ventas (ventas[-5:]) y las invierte ([::-1]) para mostrar la venta más reciente primero en la tabla. Luego crea un DataFrame de pandas con esa información para mostrarla en Streamlit.
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
            df = pd.DataFrame(usuarios) #Crea un DataFrame de pandas a partir de la lista de usuarios leída del archivo, para mostrarla en una tabla en Streamlit.
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
                ok, msg = registrar_usuario(nombre, nueva_pass, nuevo_rango) #Llama a la función registrar_usuario con el nombre de usuario, la contraseña y el rango seleccionados. La función devuelve un estado (ok) que indica si el registro fue exitoso o no, y un mensaje (msg) que contiene información sobre el resultado del registro, como si el usuario ya existe o si se registró correctamente.
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
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(inventario)} productos · {sum(p['Cantidad'] for p in inventario)} unidades") #Muestra un pie de página debajo de la tabla con el total de productos (contando cada producto como una unidad) y el total de unidades disponibles en stock, sumando la cantidad de cada producto en el inventario.
        else:
            st.info("El inventario está vacío.")

    with tab2:
        st.markdown("#### Agregar / actualizar producto")
        col1, col2, col3 = st.columns(3)
        with col1:
            prod_nombre = st.text_input("Nombre del producto", key="inv_nombre", placeholder="Ej: manzana")
        with col2:
            prod_cantidad = st.number_input("Cantidad", min_value=1, step=1, key="inv_cantidad") #Input numérico para la cantidad del producto, con un valor mínimo de 1 y un paso de 1, para asegurar que se ingresen cantidades enteras positivas.
        with col3:
            prod_precio = st.number_input("Precio unitario", min_value=0.01, step=0.01, format="%.2f", key="inv_precio") #Input numérico para el precio unitario del producto, con un valor mínimo de 0.01 y un paso de 0.01, para asegurar que se ingresen precios positivos con dos decimales.

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
        busqueda = st.text_input("Nombre del producto", key="busq_nombre", placeholder="Escriba el nombre del producto a buscar")
        if st.button("Buscar"):
            nombre = busqueda.strip().lower()
            inventario = leer_inventario()
            resultado = next((p for p in inventario if p["Nombre"] == nombre), None) #Busca en la lista de productos del inventario un producto cuyo nombre coincida exactamente con el nombre ingresado en el campo de búsqueda. Si encuentra un producto que coincida, lo devuelve como resultado; si no encuentra ningún producto con ese nombre, devuelve None.
            if resultado:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Producto", resultado["Nombre"].capitalize()) #Muestra el nombre del producto encontrado en una métrica, capitalizando la primera letra para que se vea más presentable.
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

        productos_disponibles = [p["Nombre"] for p in inventario if p["Cantidad"] > 0] #Crea una lista de nombres de productos que tienen una cantidad mayor a 0 en el inventario, para mostrar solo los productos disponibles para la venta en el selectbox.

        col1, col2 = st.columns(2)
        with col1:
            prod_venta = st.selectbox("Producto", productos_disponibles, key="venta_prod")
        with col2:
            prod_info = next((p for p in inventario if p["Nombre"] == prod_venta), None) #Busca en la lista de productos del inventario el producto que coincida con el producto seleccionado en el selectbox. Si encuentra el producto, devuelve su información como un diccionario; si no lo encuentra devuelve None.
            stock_actual = prod_info["Cantidad"] if prod_info else 0 #Si se encontró el producto en el inventario, se obtiene su cantidad actual para mostrarla como referencia al usuario al momento de ingresar la cantidad a vender. Si por alguna razón no se encuentra el producto, se asigna un stock_actual de 0 para evitar errores al intentar mostrar la cantidad disponible.
            st.markdown(f"**Stock disponible:** {stock_actual} unidades")
            cantidad_venta = st.number_input("Cantidad a vender", min_value=0, max_value=stock_actual, step=1, key="venta_cantidad")

        if prod_info:
            subtotal = prod_info["Precio"] * cantidad_venta
            st.markdown( #Es lo que hay dentro del recuadro e3 "Total a cobrar" 
                f'<div class="metric-box" style="max-width:250px;">'
                f'<div class="metric-value">${subtotal:,.2f}</div>'
                f'<div class="metric-label">Total a cobrar</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Confirmar venta", use_container_width=False):
            resultado, total = registrar_venta(prod_venta, int(cantidad_venta)) #Llama a la función registrar_venta con el nombre del producto seleccionado y la cantidad a vender ingresada por el usuario. La función devuelve un estado (resultado) que indica si la venta se registró correctamente o si hubo algún problema (como stock insuficiente, producto no encontrado o inventario vacío), y el total de la venta si se registró correctamente.
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
            df = pd.DataFrame(ventas[::-1]) #Toma la lista de ventas y la invierte para mostrar la venta más reciente primero en la tabla. Luego crea un DataFrame de pandas con esa información para mostrarla en Streamlit.
            df["Total"] = df["Total"].apply(lambda x: f"${x:,.2f}") #Formatea la columna "Total" del DataFrame para mostrar los valores como montos en pesos colombianos con dos decimales y separadores de miles, para que se vea más claro y profesional en la tabla de ventas.
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

    df_ventas = pd.DataFrame(ventas) #Crea un DataFrame de pandas a partir de la lista de ventas leída del archivo, para facilitar el análisis y la generación de gráficos en la página de reportes.

    # Agrupaciones
    ventas_por_producto = df_ventas.groupby("Producto").agg( #Agrupa las ventas por producto, sumando la cantidad de unidades vendidas y el total de ingresos para cada producto, para obtener un resumen de las ventas por producto que se puede mostrar en gráficos y tablas en la página de reportes.
        Unidades=("Cantidad", "sum"), #Suma la cantidad de unidades vendidas para cada producto, para obtener el total de unidades vendidas por producto.
        Ingresos=("Total", "sum"),
    ).reset_index().sort_values("Unidades", ascending=False) #Ordena los productos por la cantidad de unidades vendidas en orden descendente, para mostrar primero los productos más vendidos en los gráficos y tablas de la página de reportes.

    ventas_por_fecha = df_ventas.groupby("Fecha").agg( #Agrupa las ventas por fecha, sumando el total de ingresos para cada fecha, para obtener un resumen de los ingresos diarios que se puede mostrar en un gráfico de líneas en la página de reportes.
        Total=("Total", "sum")
    ).reset_index().sort_values("Fecha") #Ordena las fechas en orden ascendente para mostrar la evolución de los ingresos a lo largo del tiempo de manera cronológica en el gráfico de líneas de la página de reportes.

    DARK_BG  = "#161616" #Color de fondo oscuro para los gráficos, que se utiliza para crear un contraste visual con los colores de las barras, líneas y texto, y para darle un aspecto moderno y elegante a los gráficos en la página de reportes.
    ACCENT   = "#428af5" #Color de acento para los elementos destacados en los gráficos, como las barras de los productos más vendidos o la línea de ingresos por fecha.
    SECONDARY= "#60a5fa" #Color secundario para elementos complementarios en los gráficos, como las barras de productos menos vendidos o las áreas debajo de la línea de ingresos por fecha.
    TEXT     = "#f0ece0"
    GRID     = "#2a2a2a" #Color para las líneas de la cuadrícula en los gráficos, que ayuda a mejorar la legibilidad de los gráficos sin ser demasiado intrusivo, manteniendo la coherencia con el fondo oscuro y los colores de acento.
    matplotlib.rcParams.update({ #Actualiza la configuración de Matplotlib para aplicar los colores y estilos definidos anteriormente a todos los gráficos generados en la página de reportes, asegurando una apariencia consistente y personalizada que se integra bien con el diseño general de la aplicación.
        "figure.facecolor": DARK_BG,
        "axes.facecolor":   DARK_BG, 
        "axes.edgecolor":   GRID,
        "axes.labelcolor":  TEXT,
        "xtick.color":      TEXT,
        "ytick.color":      TEXT,
        "text.color":       TEXT,
        "grid.color":       GRID,
        "font.family":      "monospace", #Fuente de letra monoespaciada para los gráficos, que le da un aspecto más técnico y uniforme a los textos dentro de los gráficos, como las etiquetas de los ejes, los títulos y los valores de las barras o líneas.
    })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top productos vendidos")
        fig, ax = plt.subplots(figsize=(6, 4)) #Crea una figura y un eje para el gráfico de barras horizontales que muestra los productos más vendidos, con un tamaño de 6 pulgadas de ancho por 4 pulgadas de alto, para que se ajuste bien al espacio disponible en la columna del reporte.
        top = ventas_por_producto.head(6) #Toma los primeros 6 productos del DataFrame de ventas por producto, que son los productos más vendidos debido al ordenamiento previo, para mostrar solo los productos más destacados en el gráfico de barras horizontales.
        bars = ax.barh(top["Producto"], top["Unidades"], color=ACCENT, height=0.6, edgecolor="none")
        ax.set_xlabel("Unidades vendidas") #Etiqueta para el eje x del gráfico de barras horizontales.
        ax.invert_yaxis() #Invierte el eje y para que el producto más vendido aparezca en la parte superior del gráfico, siguiendo la convención común de mostrar los valores más altos primero en gráficos de barras horizontales.
        ax.grid(axis="x", alpha=0.3) #Muestra una cuadrícula en el eje x con transparencia de 0.3, que ayuda a mejorar la legibilidad de los valores en el gráfico.
        ax.spines[["top", "right", "left"]].set_visible(False)
        for bar in bars:
            ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                    str(int(bar.get_width())), va="center", fontsize=9, color=TEXT) #Agrega etiquetas de texto al final de cada barra en el gráfico de barras horizontales, mostrando la cantidad de unidades vendidas para cada producto.
        plt.tight_layout() #Ajusta el diseño del gráfico para que los elementos no se solapen y se vean bien distribuidos dentro del espacio asignado, especialmente considerando las etiquetas de texto agregadas al final de las barras.
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Participación de ingresos")
        fig, ax = plt.subplots(figsize=(6, 4))
        colors_pie = [ACCENT, SECONDARY, "#4ade80", "#f87171", "#fb923c", "#a78bfa"]
        top6 = ventas_por_producto.head(6)
        wedges, texts, autotexts = ax.pie(
            top6["Ingresos"],
            labels=top6["Producto"], #Etiquetas para cada porción del gráfico de pastel, que corresponden a los nombres de los productos más vendidos.
            autopct="%1.1f%%", #Formato para mostrar el porcentaje de participación de cada producto en los ingresos totales, con un decimal y el símbolo de porcentaje.
            colors=colors_pie[:len(top6)],
            startangle=140, #Ángulo de inicio para el gráfico de pastel, que determina la posición de la primera porción del pastel. En este caso, se establece en 140 grados para que las porciones se distribuyan de manera equilibrada y visualmente atractiva.
            wedgeprops={"edgecolor": DARK_BG, "linewidth": 2}, #Propiedades para las porciones del gráfico de pastel, que incluyen un borde del mismo color que el fondo oscuro y un grosor de línea de 2, para crear un efecto de separación entre las porciones y mejorar la estética del gráfico.
        )
        for t in texts + autotexts: #Configura el color y el tamaño de las etiquetas de texto en el gráfico de pastel, tanto las etiquetas de los productos como los porcentajes, para que sean legibles y se integren bien con el diseño general del gráfico.
            t.set_color(TEXT)
            t.set_fontsize(9)
        plt.tight_layout() #Ajusta el diseño del gráfico para que los elementos no se solapen y se vean bien distribuidos dentro del espacio asignado.
        st.pyplot(fig)
        plt.close()

    st.markdown("#### Ingresos por fecha")
    fig, ax = plt.subplots(figsize=(10, 3.5)) #Crea una figura y un eje para el gráfico de líneas que muestra la evolución de los ingresos por fecha, con un tamaño de 10 pulgadas de ancho por 3.5 pulgadas de alto, para que se ajuste bien al espacio disponible.
    ax.fill_between(ventas_por_fecha["Fecha"], ventas_por_fecha["Total"],
                    alpha=0.3, color=ACCENT)
    ax.plot(ventas_por_fecha["Fecha"], ventas_por_fecha["Total"],
            color=ACCENT, linewidth=2, marker="o", markersize=5) #Dibuja una línea con marcadores en el gráfico de líneas para mostrar la evolución de los ingresos por fecha, utilizando el color de acento definido anteriormente, con un grosor de línea de 2, y marcadores circulares de tamaño 5 para resaltar cada punto de datos en la línea.
    ax.set_ylabel("Ingresos ($)")
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False) #Oculta los bordes superior y derecho del gráfico de líneas.
    plt.xticks(rotation=30, ha="right") #Rota las etiquetas del eje x 30 grados y las alinea a la derecha para mejorar la legibilidad de las fechas, especialmente si hay muchas fechas o si los nombres de las fechas son largos.
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Productos con stock bajo (≤ 5)")
        bajo = [p for p in inventario if p["Cantidad"] <= 5] #Crea una lista de productos que tienen una cantidad menor o igual a 5 en el inventario.
        if bajo:
            df_bajo = pd.DataFrame(bajo)
            st.dataframe(df_bajo, use_container_width=True, hide_index=True) #Muestra una tabla con los productos que tienen stock bajo.
        else:
            st.success("Todos los productos tienen stock suficiente.")

    with col4:
        st.markdown("#### Resumen financiero")
        total_ingresos = df_ventas["Total"].sum()
        producto_estrella = ventas_por_producto.iloc[0]["Producto"] if not ventas_por_producto.empty else "—" #Obtiene el nombre del producto más vendido (producto estrella)del DataFrame de ventas por producto, tomando la primera fila (iloc[0]) que corresponde al producto con más unidades vendidas debido al ordenamiento previo. Si el DataFrame de ventas por producto está vacío, se asigna un guion ("—") como valor predeterminado para indicar que no hay datos disponibles.
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
    if not st.session_state.logged_in: #Si el usuario no ha iniciado sesión, se muestra la pantalla de login y se detiene la ejecución del resto de la función main, para que no se renderice ninguna otra parte de la aplicación hasta que el usuario inicie sesión correctamente.
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