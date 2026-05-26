INICIO DEL PROGRAMA

DEFINIR archivo_usuarios = "usuarios.txt"
DEFINIR archivo_inventario = "inventario.txt"
DEFINIR archivo_ventas = "ventas.txt"


--------------------------------------------------
FUNCIÓN usuario_jefe()
--------------------------------------------------
    DEFINIR nuevo_usuario como texto vacío
    DEFINIR existe como FALSO

    INTENTAR abrir archivo_usuarios en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene nombre, contraseña y rango
                CONTINUAR con la siguiente línea

            OBTENER nombre, contraseña y rango

            SI nombre es igual a "jefe"
                existe = VERDADERO

            AGREGAR línea a nuevo_usuario

        FIN PARA

        SI existe es FALSO
            AGREGAR "jefe/jefe/jefe" a nuevo_usuario

        ABRIR archivo_usuarios en modo escritura
        ESCRIBIR nuevo_usuario

    SI archivo_usuarios no existe
        CREAR archivo_usuarios
        ESCRIBIR "jefe/jefe/jefe"

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN verificar_login(usuario, contraseña)
--------------------------------------------------
    INTENTAR abrir archivo_usuarios en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 3 datos necesarios
                CONTINUAR

            OBTENER nombre, clave y rango

            SI nombre es igual a usuario Y clave es igual a contraseña
                RETORNAR rango

        FIN PARA

    SI archivo_usuarios no existe
        RETORNAR NULO

    RETORNAR NULO

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN registrar_usuario(nombre_usuario, contraseña_usuario, rango_usuario)
--------------------------------------------------
    DEFINIR usuario_existe como FALSO
    DEFINIR nuevo_texto como texto vacío

    INTENTAR abrir archivo_usuarios en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 3 datos necesarios
                CONTINUAR

            OBTENER nombre, contraseña y rango

            SI nombre es igual a nombre_usuario
                usuario_existe = VERDADERO

            AGREGAR línea a nuevo_texto

        FIN PARA

        SI usuario_existe es VERDADERO
            RETORNAR FALSO, "El nombre de usuario ya existe"

        AGREGAR nuevo usuario a nuevo_texto

        ABRIR archivo_usuarios en modo escritura
        ESCRIBIR nuevo_texto

        RETORNAR VERDADERO, "Usuario registrado exitosamente"

    SI archivo_usuarios no existe
        CREAR archivo_usuarios
        ESCRIBIR nuevo usuario
        RETORNAR VERDADERO, "Archivo creado y usuario registrado"

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN cambiar_contraseña(usuario, nueva_contraseña)
--------------------------------------------------
    DEFINIR nuevo_texto como texto vacío
    DEFINIR encontrado como FALSO

    INTENTAR abrir archivo_usuarios en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 3 datos necesarios
                CONTINUAR

            OBTENER nombre, contraseña y rango

            SI nombre es igual a usuario Y encontrado es FALSO
                AGREGAR nombre + nueva_contraseña + rango a nuevo_texto
                encontrado = VERDADERO
            SI NO
                AGREGAR línea original a nuevo_texto

        FIN PARA

        ABRIR archivo_usuarios en modo escritura
        ESCRIBIR nuevo_texto

        RETORNAR encontrado

    SI archivo_usuarios no existe
        RETORNAR FALSO

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN leer_inventario()
--------------------------------------------------
    CREAR lista productos vacía

    INTENTAR abrir archivo_inventario en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene nombre, cantidad, precio y fecha
                CONTINUAR

            OBTENER nombre, cantidad, precio y fecha

            CREAR producto con:
                Nombre
                Cantidad convertida a entero
                Precio convertido a decimal
                Fecha

            AGREGAR producto a la lista productos

        FIN PARA

    SI archivo_inventario no existe
        NO HACER NADA

    RETORNAR productos

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN buscar_producto(nombre)
--------------------------------------------------
    INTENTAR abrir archivo_inventario en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 4 datos necesarios
                CONTINUAR

            OBTENER nombre_producto, cantidad, precio y fecha

            SI nombre_producto es igual a nombre
                RETORNAR datos del producto

        FIN PARA

    SI archivo_inventario no existe
        RETORNAR NULO

    RETORNAR NULO

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN registrar_producto(nombre, cantidad, precio)
--------------------------------------------------
    OBTENER fecha actual
    DEFINIR nuevo_texto como texto vacío
    DEFINIR existe como FALSO

    INTENTAR abrir archivo_inventario en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 4 datos necesarios
                CONTINUAR

            OBTENER nombre_producto, cantidad_actual, precio_actual y fecha

            SI nombre_producto es igual a nombre
                nueva_cantidad = cantidad_actual + cantidad
                AGREGAR producto actualizado a nuevo_texto
                existe = VERDADERO
            SI NO
                AGREGAR línea original a nuevo_texto

        FIN PARA

    SI archivo_inventario no existe
        CONTINUAR

    SI existe es FALSO
        AGREGAR nuevo producto a nuevo_texto

    ABRIR archivo_inventario en modo escritura
    ESCRIBIR nuevo_texto

    RETORNAR existe

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN registrar_venta(nombre, cantidad_vendida)
--------------------------------------------------
    DEFINIR nuevo_inventario como texto vacío
    DEFINIR encontrado como FALSO
    DEFINIR stock_insuficiente como FALSO
    DEFINIR precio_usado como NULO

    INTENTAR abrir archivo_inventario en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 4 datos necesarios
                CONTINUAR

            OBTENER nombre_producto, cantidad_actual, precio y fecha

            SI nombre_producto es igual a nombre
                encontrado = VERDADERO

                SI cantidad_vendida es menor o igual a cantidad_actual
                    nueva_cantidad = cantidad_actual - cantidad_vendida
                    AGREGAR producto con nueva cantidad a nuevo_inventario
                    precio_usado = precio
                SI NO
                    stock_insuficiente = VERDADERO
                    AGREGAR línea original a nuevo_inventario

            SI NO
                AGREGAR línea original a nuevo_inventario

        FIN PARA

        ABRIR archivo_inventario en modo escritura
        ESCRIBIR nuevo_inventario

        SI encontrado es FALSO
            RETORNAR "no_encontrado", NULO

        SI stock_insuficiente es VERDADERO
            RETORNAR "stock_insuficiente", NULO

        total = registrar_venta_archivo(nombre, cantidad_vendida, precio_usado)

        RETORNAR "ok", total

    SI archivo_inventario no existe
        RETORNAR "no_inventario", NULO

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN registrar_venta_archivo(nombre, cantidad, precio)
--------------------------------------------------
    OBTENER fecha actual
    total = precio * cantidad

    ABRIR archivo_ventas en modo agregar
    ESCRIBIR nombre, cantidad, total y fecha

    RETORNAR total

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN leer_ventas()
--------------------------------------------------
    CREAR lista ventas vacía

    INTENTAR abrir archivo_ventas en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 4 datos necesarios
                CONTINUAR

            OBTENER producto, cantidad, total y fecha

            CREAR venta con:
                Producto
                Cantidad convertida a entero
                Total convertido a decimal
                Fecha

            AGREGAR venta a la lista ventas

        FIN PARA

    SI archivo_ventas no existe
        NO HACER NADA

    RETORNAR ventas

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN leer_usuarios()
--------------------------------------------------
    CREAR lista usuarios vacía

    INTENTAR abrir archivo_usuarios en modo lectura

        PARA cada línea del archivo
            SEPARAR línea por "/"

            SI la línea no tiene los 3 datos necesarios
                CONTINUAR

            OBTENER nombre, contraseña y rango

            CREAR usuario con:
                Usuario = nombre
                Rango = rango

            AGREGAR usuario a la lista usuarios

        FIN PARA

    SI archivo_usuarios no existe
        NO HACER NADA

    RETORNAR usuarios

FIN FUNCIÓN


--------------------------------------------------
FUNCIÓN reporte_ventas()
--------------------------------------------------
    ventas = leer_ventas()
    inventario = leer_inventario()

    SI ventas está vacío
        RETORNAR NULO

    total_dinero = SUMA de todos los totales de ventas
    total_unidades = SUMA de todas las cantidades vendidas

    stock_bajo = productos del inventario con cantidad menor o igual a 5

    CREAR reporte con:
        ventas
        inventario
        total_dinero
        total_unidades
        stock_bajo

    RETORNAR reporte

FIN FUNCIÓN


--------------------------------------------------
EJECUCIÓN INICIAL
--------------------------------------------------
LLAMAR usuario_jefe()

FIN DEL PROGRAMA
