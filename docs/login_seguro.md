# Autenticación segura en la aplicación de recetas

Este documento describe la implementación del nuevo sistema de autenticación segura para la aplicación Streamlit y los pasos necesarios para gestionarlo correctamente.

## 1. Resumen de la solución

- Las credenciales ya no están codificadas en el código fuente.
- Los nombres de usuario se almacenan cifrados con `Fernet` y se indexan mediante un hash SHA-256 para evitar duplicados.
- Las contraseñas se almacenan utilizando PBKDF2-HMAC con SHA-256, 200 000 iteraciones y una sal aleatoria por usuario.
- Las comprobaciones de acceso se realizan contra la tabla `usuario` en la base de datos `recetas.db`.
- El módulo `auth.py` ofrece utilidades reutilizables para crear cuentas y validar credenciales.

## 2. Creación y actualización de usuarios

### 2.1 Desde la interfaz web

- En la pantalla de inicio de sesión encontrarás el botón **"Registrar nuevo usuario"**.
- Al pulsarlo se despliega un formulario independiente en el que debes indicar el nombre de usuario, la contraseña y su confirmación.
- La contraseña se valida de forma local; si las entradas coinciden y no hay errores, se invoca a `auth.create_user` para almacenar el hash y la sal.
- Tras un registro exitoso, la interfaz vuelve automáticamente al formulario de inicio de sesión para que puedas autenticarte con las nuevas credenciales.

### 2.2 Desde la línea de comandos

1. Asegúrate de tener un entorno virtual activo (opcional pero recomendado).
2. Ejecuta el siguiente comando para crear un usuario inicial:

   ```bash
   cd proyecto_restaurant
   python -m auth crear-usuario <USUARIO> <CONTRASEÑA>
   ```

   Reemplaza `<USUARIO>` y `<CONTRASEÑA>` por los valores deseados. El comando generará automáticamente una sal aleatoria y guardará el hash en la base de datos.

3. Si necesitas cambiar la contraseña de un usuario existente, reutiliza el mismo comando añadiendo la bandera `--overwrite`:

   ```bash
   python -m auth crear-usuario <USUARIO> <NUEVA_CONTRASEÑA> --overwrite
   ```

   El sistema validará que el nombre de usuario no esté vacío y confirmará por consola el resultado de la operación.

## 3. Flujo de autenticación en la interfaz

- Al abrir la aplicación, se muestra un formulario de inicio de sesión protegido (`app_restaurante.py`).
- En cualquier momento se puede alternar al formulario de registro para crear una cuenta nueva sin abandonar la pantalla.
- Tras enviar las credenciales, se verifica el hash almacenado mediante `auth.verify_user`, que devuelve el nombre de usuario descifrado cuando las credenciales son válidas.
- Si la verificación es exitosa, se almacena en la sesión (`st.session_state['auth_user']`) el nombre de usuario recuperado de forma segura.
- Desde la barra lateral es posible cerrar la sesión de forma segura.

## 4. Inicialización de la base de datos

El script `script_crear_db.py` sigue siendo responsable de crear las tablas principales de recetas y ahora también garantiza que la tabla `usuario` exista mediante `auth.initialize_user_table()`. Si detecta un esquema antiguo, lo migra automáticamente cifrando los nombres de usuario existentes. Puedes ejecutar el script tantas veces como sea necesario; las tablas se crean o actualizan según corresponda.

## 5. Buenas prácticas adicionales

- Usa contraseñas robustas y evita compartirlas por canales inseguros.
- Renueva periódicamente las contraseñas utilizando el comando con `--overwrite`.
- Considera almacenar las credenciales sensibles (como contraseñas temporales) en gestores de contraseñas.
- Si despliegas la aplicación públicamente, utiliza HTTPS para proteger las credenciales en tránsito.

Con estos pasos, la aplicación dispone de un inicio de sesión consistente con buenas prácticas de seguridad y fácilmente extensible para futuras mejoras.
