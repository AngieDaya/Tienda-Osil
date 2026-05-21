# 🏪 Tienda OSIL

Aplicación web de gestión de tienda construida con **Python** y **Streamlit**. Permite administrar usuarios, inventario, ventas y reportes desde una interfaz oscura y moderna.

---

## Funcionalidades

- **Login con roles** — tres niveles de acceso: `jefe`, `gerente` y `empleado`
- **Dashboard** — resumen general con métricas clave
- **Usuarios** — registro, listado y cambio de contraseña (solo jefe/gerente)
- **Inventario** — agregar, actualizar y buscar productos
- **Ventas** — registrar transacciones y consultar el historial
- **Reportes** — gráficas de productos más vendidos, ingresos por fecha y stock bajo

> Los datos se almacenan localmente en archivos de texto plano:  
> `usuarios.txt`, `inventario.txt` y `ventas.txt`

---

## Estructura del proyecto

```
tienda-osil/
├── TIENDA_OSIL.py      # Aplicación principal
├── requirements.txt    # Dependencias del proyecto
├── usuarios.txt        # Generado automáticamente al iniciar
├── inventario.txt      # Generado al registrar productos
└── ventas.txt          # Generado al registrar ventas
```

---

## Instalación y configuración

### 1. Clonar o descargar el proyecto

Coloca el archivo `TIENDA_OSIL.py` y `requirements.txt` en una misma carpeta.

### 2. Crear el entorno virtual

Abre una terminal en la carpeta del proyecto y ejecuta:

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

Sabrás que el entorno está activo cuando veas `(venv)` al inicio de tu terminal.

### 3. Instalar las dependencias

Con el entorno virtual activo, instala todo lo necesario con:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` debe contener al menos:

```
streamlit
pandas
matplotlib
```

---

## Iniciar la aplicación

```bash
streamlit run TIENDA_OSIL.py
```
ó
```bash
streamlit run '.\TIENDA OSIL.py'
```

Streamlit abrirá automáticamente el navegador en `http://localhost:8501`.  
Si no se abre solo, copia esa URL y pégala en tu navegador.

---

## Credenciales iniciales

Al ejecutar la app por primera vez, se crea automáticamente el usuario administrador:

| Usuario | Contraseña | Rango |
|---------|-----------|-------|
| `jefe`  | `jefe`    | jefe  |


---

## Detener la aplicación

Presiona `Ctrl + C` en la terminal para detener el servidor de Streamlit.

Para desactivar el entorno virtual:

```bash
deactivate
```
