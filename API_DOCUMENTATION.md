# 📚 Documentación AlecTours

# REQUISITOS FUNCIONALES

# RF-001 — Registro de usuario

<!--
  ¿Qué? Requisito funcional que define el registro de nuevos usuarios en el sistema.
  ¿Para qué? Documentar formalmente la funcionalidad de creación de cuentas.
  ¿Impacto? Sin este requisito, no habría forma estandarizada de incorporar usuarios al sistema.
-->

---

## Identificación de RF-001 Registro de usuario

| Campo         | Valor               |
| ------------- | ------------------- |
| **ID**        | RF-001              |
| **Nombre**    | Registro de usuario |
| **Módulo**    |                     |
| **Prioridad** | Alta                |
| **Estado**    | Implementado        |
| **Fecha**     | Marzo 2026          |

---

## Descripción de RF-001 Registro de usuario

El sistema debe permitir que un usuario nuevo cree una cuenta proporcionando su nombre completo, correo electrónico, numero de telefono y contraseña. Tras el registro, el sistema envía un correo de verificación a la dirección de email proporcionada. El usuario debe hacer clic en el enlace del correo para activar su cuenta antes de poder iniciar sesión.

---

## Entradas de RF 001 Registro de usuario

| Campo             | Tipo          | Obligatorio | Validaciones                                                                 |
| ------------------| ------------- | ----------- | ---------------------------------------------------------------------------- |
| `Nombre completo` | Texto         | Sí          | Mínimo 2 caracteres, máximo 255                                              |
| `email`           | Texto (email) | Sí          | Formato de email válido, máximo 255 caracteres, debe ser único en el sistema |
| `celular`         |  Texto        | Sí          | Numero de telefono no mayor a 11 digitos                                     |
| `password`        | Texto         | Sí          | Mínimo 8 caracteres, al menos 1 mayúscula, 1 minúscula y 1 número            |

---

## Proceso de RF 001

1. El usuario ingresa nombre completo, correo electrónico y contraseña en el formulario de registro.
2. El frontend valida los campos antes de enviar la solicitud al backend.
3. El backend valida los datos con Pydantic (formato, longitudes, fortaleza de contraseña).
4. El backend verifica que el correo no esté registrado previamente.
5. La contraseña se hashea con bcrypt antes de almacenarse.
6. Se crea el registro del usuario en la tabla `users` con `is_email_verified = false`.
7. Se genera un token UUID único de verificación de email con expiración de 24 horas y se almacena en la tabla `email_verification_tokens`.
8. Se envía un correo electrónico al usuario con el enlace de verificación: `{FRONTEND_URL}/verify-email?token={token}`.
9. La respuesta retorna los datos del usuario recién creado (sin contraseña, con `is_email_verified: false`).
10. El usuario hace clic en el enlace del correo → el frontend envía el token al endpoint `POST /verify-email`.
11. El backend valida el token (existencia, expiración, uso previo), marca `is_email_verified = true` y el token como usado.

---

## Salidas de RF 001

| Escenario           | Código HTTP | Respuesta                                                                                                                      |                                                                          
| ------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------|
| Registro exitoso    | 201         | Datos del usuario creado (`id`, `email`, `full_name`,`numero de celular` `is_active`, `is_email_verified: false`, `created_at`)|                                                                                  |                                    
| Email ya registrado | 400         | Mensaje de error: "Email ya registrado"                                                                                        |
| Datos inválidos     | 422         | Detalle de los errores de validación                                                                                           |

---

## Endpoints asociados de RF 001

| Método | Ruta                        | Auth requerida | Descripción                                  |
| ------ | --------------------------- | -------------- | -------------------------------------------- |
| POST   | `/api/v1/auth/register`     | No             | Crea la cuenta y envía email de verificación |
| POST   | `/api/v1/auth/verify-email` | No             | Activa la cuenta con el token del email      |

---

## Reglas de negocio de RF 001

- RN-001: El correo electrónico debe ser único en todo el sistema.
- RN-002: La contraseña nunca se almacena en texto plano; siempre se hashea con bcrypt.
- RN-003: La contraseña debe cumplir los requisitos mínimos de fortaleza (8+ caracteres, mayúscula, minúscula, número).
- RN-004: El campo `is_active` se establece como `true` por defecto al crear la cuenta.
- RN-005: El campo `is_email_verified` se establece como `false` por defecto — el usuario no puede iniciar sesión hasta verificar su correo.
- RN-006: El token de verificación de email expira en 24 horas y solo puede usarse una vez.
- RN-007: Si el envío del correo falla (error en Resend API), el usuario igual queda registrado en la BD. En modo desarrollo (sin API key), el enlace se imprime en la consola del servidor.

---

# RF-002 — Creación de Preferencias en Perfil del Cliente
<!--
  ¿Qué? Requisito funcional que permite conocer la preferencias de viajes del clientes.
  ¿Para qué? Generar propuesta de viajes coforme a sus preferencias.
  ¿Impacto? El usuario revisirá en su interfaz planes y paquetes turisticos de su preferencia
-->
---

## Identificación de RF -002 Creación de Preferencias en Perfil del Cliente 

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RF-002                                                 |
| **Nombre**        |Creación de Preferencias en Perfil del Cliente          |
| **Módulo**        | -                                                      |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |
| **Fecha**         | mayo 2026                                              |

---

## Descripción de RF -002 

El sistema debe permitir que el cliente complete un cuestionario inicial para definir su perfil selecionando preferencias de viaje, incluyendo estilos, destinos y actividades de intereses, presupuesto y restricciones, el cual será utilizado para personalizar automáticamente su experiencia por medio de paquetes turisticos recomendados.

---

## Entradas de RF -002 

| Campos                                                              | Tipo                 | Obligatorio | Validaciones                                         |
| --------------------------------------------------------------------| ---------------------| ----------- | ------------------------------- ---------------------|
| `¿Qué te apasiona? Selecciona tus favoritos para conocer Colombia.` | Boton de opción      | No          | Permitir selección múltiple.                         |
| `Con quién vas a vivir esta aventura?`                              | Boton de opción      | No          | Permitir una única selección.                        |
|`Define tu presupuesto aproximado`                                   | Boton de opción      | No          | Debe seleccionar una única categoría de presupuesto. |                    
| `Tu clima ideal es...`                                              | Boton de opción      | No          | Permitir una única selección.                        |
| `¿Cuál es tu transporte preferido?`                                 | Boton de opción      | No          | Permitir una única selección.                        |

---

## Proceso de RF -002 

1. El usuario una vez registrado crea la cuenta.
2. El frontend muestra un formulario con la pregunta de ¿Qué te apasiona? Selecciona tus favoritos para conocer Colombia con campos de selección.
3. El frontend continua con el formulario seleccione o no las prefernecias
4. El backend registra las opciones selecionadas por el cliente

---

## Salidas de RF -002 

| Escenario                    | Código HTTP | Respuesta                                                          |
| ---------------------------- | ----------- | ------------------------------------------------------------------ |
| Selección exitosa            | 200         | Bienvenida al sistema en login                                     |


---

## Endpoint asociado a RF -002 

| Método | Ruta                     | Auth requerida |
| ------ | ------------------------ | -------------- |
| POST   | `/api/v1/auth/___  `     | Si             |

---

## Reglas de negocio de RF -002 

- RN-001: Solo los usuarios autenticados y con una cuenta activa pueden registrar o actualizar sus preferencias de viaje.
- RN-002: El cuestionario de preferencias debe mostrarse al usuario durante su primer ingreso al sistema después del registro.
- RN-003: El sistema debe almacenar únicamente las opciones seleccionadas por el usuario.
- RN-004: Si el usuario no registra preferencias, el sistema mostrará recomendaciones generales de destinos y paquetes turísticos.
- RN-005: El sistema debe conservar el historial de fecha de creación y última actualización de las preferencias.

---

# RF-003 — Inicio de sesión (Login)

<!--
  ¿Qué? Requisito funcional que define el inicio de sesión de usuarios existentes.
  ¿Para qué? Documentar formalmente cómo un usuario se autentica en el sistema.
  ¿Impacto? Sin login, los usuarios no podrían acceder a las funcionalidades protegidas.
-->

---

## Identificación de RF-003

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RF-003                                                 |
| **Nombre**        | Inicio de sesión (Login)                               |
| **Módulo**        | Autenticación                                          |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |
| **Fecha**         | Abril 2026                                           |

---

## Descripción

El sistema debe permitir que un usuario registrado inicie sesión proporcionando su correo electrónico y contraseña. Si las credenciales son válidas, se generan dos tokens JWT: un access token (corta duración) y un refresh token (larga duración).

---

## Entradas de RF-003

| Campo      | Tipo         | Obligatorio | Validaciones                    |
| ---------- | ------------ | ----------- | ------------------------------- |
| `email`    | Texto (email)| Sí          | Formato de email válido         |
| `password` | Texto        | Sí          | No vacío                        |

---

## Proceso de RF-003

1. El usuario ingresa correo y contraseña en el formulario de login.
2. El frontend envía las credenciales al backend.
3. El backend busca al usuario por correo electrónico en la base de datos.
4. Si el usuario no existe o la cuenta está inactiva, se retorna error genérico.
5. Se verifica la contraseña ingresada contra el hash almacenado (bcrypt).
6. Si la contraseña no coincide, se retorna error genérico (mismo mensaje que usuario inexistente, por seguridad).
7. Se generan un access token (15 minutos) y un refresh token (7 días) firmados con JWT (HS256).
8. El frontend almacena los tokens y redirige al dashboard.

---

## Salidas de RF-003 

| Escenario                    | Código HTTP | Respuesta                                                          |
| ---------------------------- | ----------- | ------------------------------------------------------------------ |
| Login exitoso                | 200         | `{ access_token, refresh_token, token_type: "bearer" }`           |
| Credenciales inválidas       | 401         | Mensaje genérico: "Incorrect email or password"                    |
| Cuenta inactiva              | 401         | Mensaje genérico: "Incorrect email or password"                    |
| Datos inválidos              | 422         | Detalle de los errores de validación                               |

---

## Endpoint asociado de RF-003

| Método | Ruta                     | Auth requerida |
| ------ | ------------------------ | -------------- |
| POST   | `/api/v1/auth/login`     | No             |

---

## Reglas de negocio de RF-003

- RN-001: Los mensajes de error de autenticación deben ser genéricos — no revelar si el email existe o si la contraseña es incorrecta (prevención de enumeración de usuarios).
- RN-002: El access token expira a los 15 minutos.
- RN-003: El refresh token expira a los 7 días.
- RN-004: Los tokens se firman con algoritmo HS256 usando una clave secreta almacenada en variable de entorno.
- RN-005: Solo pueden iniciar sesión usuarios con `is_active = true`.

---
# RF-004 — Catálogo de Vuelos

<!--
  ¿Qué? Requisito funcional que permite al agente de viajes buscar y seleccionar vuelos disponibles de diferentes proveedores.
  ¿Para qué? Facilitar la construcción de itinerarios personalizados y optimizar el proceso de planificación de viajes para los clientes.
  ¿Impacto? El agente podrá incorporar opciones de vuelo actualizadas y acordes a los requerimientos del cliente, mejorando la precisión de las propuestas de viaje y la experiencia de reserva.
-->

---

## Identificación de RF -004 Catálogo de Vuelos

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RF-004                                                 |
| **Nombre**        | Catálogo de Vuelos                                     |
| **Módulo**        | -                                                      |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |
| **Fecha**         | Abril 2026                                             |

---

## Descripción de RF-004 Catálogo de Vuelos

El sistema debe permitir al agente de viajes consultar, filtrar y seleccionar vuelos disponibles provenientes de uno o varios proveedores integrados, con el fin de incorporarlos a los itinerarios y paquetes turísticos ofrecidos a los clientes. La consulta deberá facilitar la búsqueda mediante criterios como origen, destino, fechas de viaje, aerolínea, escalas, horarios y rango de precios, mostrando únicamente las opciones disponibles al momento de la búsqueda.

---

## Entradas de RF-004 Catálogo de Vuelos

| Campos               | Tipo                     | Obligatorio | Validaciones                                                                            |
| ---------------------| -------------------------| ----------- | --------------------------------------------------------------------------------------- |
| `Origen`             | Lista desplegable - text |  Sí         |  Debe corresponder a una ciudad o aeropuerto válido.                                    |
| `Destino`            | Lista desplegable - text |  Sí         |  Debe corresponder a una ciudad o aeropuerto válido y ser diferente al origen.          |
| `Fecha de salida`    | Fecha                    |  Sí         |  No puede ser anterior a la fecha actual
| `Fecha de regreso`   | Fecha                    |  No         |  Debe ser igual o posterior a la fecha de salida.
| `Tipo de viaje`      | Botón de opción          |  Si         |  Valores permitidos: Solo ida, Ida y vuelta
| `Número de pasajeros`| Numérico                 |  Si         |  Debe ser mayor a cero
|`Aerolínea`           | Lista desplegable        |  No         |  Debe corresponder a una aerolínea disponible en los proveedores integrados.
|`Precio mínimo`       | Numérico (moneda)        |  No         |  Debe ser mayor o igual a cero.
|`Precio máximo`       | Numérico (moneda)        |  No         |  Debe ser mayor o igual al precio mínimo.
| `Proveedor de vuelos`| Lista despegable         |  No         | Debe existir en la lista de proveedores configurados.
  

---

## Proceso de RF -004 Catálogo de Vuelos

1. El agente de viajes accede al módulo de búsqueda de vuelos.
2. El frontend muestra el formulario de búsqueda con los criterios disponibles (origen, destino, fechas, pasajeros, clase, entre otros).
3. El agente ingresa los criterios de búsqueda requeridos.
4. El frontend envía la solicitud al backend.
5. El backend valida los datos ingresados.
6. El backend consulta los proveedores de vuelos integrados.
7. El backend consolida y filtra los resultados obtenidos según los criterios seleccionados.
8. El frontend muestra la lista de vuelos disponibles al agente.
9. El agente aplica filtros adicionales si lo considera necesario.
10. El agente selecciona un vuelo y una tarifa disponible.
11. El backend valida que el vuelo continúe disponible.
12. El sistema asocia el vuelo seleccionado al itinerario o paquete turístico correspondiente.
13. El sistema confirma la incorporación exitosa del vuelo al itinerario.

---

## Salidas de RF-004 Catálogo de Vuelos

| Escenario                                      | Código HTTP | Respuesta                                                                                             |
| ---------------------------- ------------------| ----------- | ------------------------------------------------------------------------------------------------------|
| Consulta de vuelos exitosa                     | 200         | Lista de vuelos disponibles obtenida correctamente                                                    |
| Vuelo seleccionado e incorporado al itinerario | 200         | Vuelo agregado al itinerario exitosamente                                                             |
| No se encontraron vuelos disponibles           | 404         | No existen vuelos que coincidan con los criterios de búsqueda                                         |
| Datos de búsqueda inválidos                    | 400         | Error en los parámetros de consulta                                                                   |
| Vuelo no disponible                            | 409         | El vuelo seleccionado ya no se encuentra disponible                                                   |
| Error de conexión con proveedores              | 503         | Mesnaje de "No fue posible consultar los proveedores de vuelos intente nuevamente más tarde"          |
| Error interno del sistema                      | 500         | Mensaje "Error al procesar la solicitud intente nuevamente más tarde"                                 |

---

## Endpoint asociado a RF-004 Catálogo de Vuelos 

| Método | Ruta                     | Auth requerida |
| ------ | ------------------------ | -------------- |
| GET    | `/api/v1/auth/___  `     | Si             |

---

## Reglas de negocio de RF -004 Catálogo de Vuelos

- RN-001: SSolo los agentes de viajes autenticados y con permisos vigentes pueden consultar y seleccionar vuelos.
- RN-002: La búsqueda de vuelos requiere como mínimo origen, destino y fecha de salida.
- RN-003: El origen y el destino no pueden ser iguales.
- RN-004: La fecha de salida no puede ser anterior a la fecha actual.
- RN-005: Para viajes de ida y vuelta, la fecha de regreso debe ser igual o posterior a la fecha de salida.
- RN-007: Solo se mostrarán vuelos con disponibilidad vigente al momento de la consulta.
- RN-008: Los resultados de búsqueda deben incluir información de horarios, duración, escalas, tarifa y disponibilidad.
- RN-009: El agente podrá aplicar filtros adicionales sobre los resultados obtenidos sin realizar una nueva consulta al proveedor, cuando la información ya esté disponible.
- RN-010: Un vuelo solo podrá asociarse a un itinerario si mantiene disponibilidad al momento de la selección.
- RN-011: El sistema debe validar nuevamente la disponibilidad y tarifa del vuelo antes de incorporarlo al itinerario.
- RN-012: Los precios mostrados deben corresponder a la moneda configurada para la operación o proveedor consultado.
- RN-013: El sistema debe registrar la fecha, hora y usuario responsable de la selección del vuelo.
- RN-015: El sistema debe registrar la fecha, hora y usuario responsable de la selección del vuelo.
- RN-016: Los vuelos seleccionados deben ser compatibles con las fechas del paquete turístico asociado.
  
---

# RF-005 — Catálogo de Alojamiento (Hoteles)
<!--
  ¿Qué? Requisito funcional que permite al agente de viajes buscar y seleccionar opciones de alojamiento disponibles.
  ¿Para qué? acilitar la construcción de itinerarios personalizados mediante la incorporación de hoteles acordes a las preferencias y necesidades del cliente.
  ¿Impacto? El agente podrá ofrecer alternativas de hospedaje actualizadas, mejorando la calidad de las propuestas de viaje y la experiencia del cliente.
-->
---

## Identificación de RF-005 Gestión de Alojamiento (Hoteles)

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RF-005                                                 |
| **Nombre**        | Gestión de Alojamiento (Hoteles)                      |
| **Módulo**        | Gestión de Productos Turísticos                        |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |
| **Fecha**         | Abril 2026                                             |

---

## Descripción de RF-005 Gestión de Alojamiento (Hoteles)

El sistema debe permitir que un agente de viajes consulte, filtre y seleccione opciones de alojamiento disponibles para un cliente. La búsqueda debe considerar criterios como destino, fechas de estancia, número de huéspedes, categoría del hotel y presupuesto estimado. El sistema mostrará únicamente alojamientos disponibles que cumplan con los parámetros definidos.
---

## Entradas de RF-005 Gestión de Alojamiento (Hoteles)

| Campos                 | Tipo                     | Obligatorio | Validaciones                                |
| -----------------------| -------------------------| ----------- | --------------------------------------------|
| `Destino`              | Lista desplegable - text |  Sí         |  Destino válido y reconocido por el sistema |
| `Fecha de ingreso`     | Fecha                    |  Sí         |  Fecha igual o posterior a la fecha actual  |
| `Fecha de salida`      | Fecha                    |  No         |  Debe ser posterior a la fecha de ingreso   |
| `Número de personas`   | Numérico                 |  Si         |  Debe ser mayor a cero                      |
|`Número de habitaciones`| Numérico                 |  No         |  Debe ser mayor a cero                      |
|`Categoria de Hotel `   | Numérico (moneda)        |  No         |  Valor entre 1 y 5 estrellas.               |
|`presupuesto máximo`    | Numérico (moneda)        |  No         |  Mayor a 0.                                 |
      
---
## Proceso de RF -005 Gestión de Alojamiento (Hoteles)

1. El agente ingresa los criterios de búsqueda del alojamiento.
2. El sistema valida la información proporcionada.
3. El sistema consulta los proveedores de alojamiento integrados o la base de datos correspondiente.
4. Se obtienen las opciones de hoteles disponibles para las fechas y destino indicados.
5. El sistema aplica filtros adicionales según categoría, capacidad y presupuesto.
6. Se ordenan los resultados según disponibilidad, precio o criterio seleccionado.
7. El sistema presenta al agente la lista de hoteles disponibles.
8. El agente selecciona una opción para incorporarla al itinerario o propuesta de viaje.

---
## Salidas de RF-004 Gestión de Alojamiento (Hoteles)

| Escenario                  | Código HTTP | Respuesta                                                |
| -------------------------- | ----------- | -------------------------------------------------------- |
| Búsqueda exitosa           | 200         | Lista de hoteles disponibles con información relevante   |
| No existen resultados      | 200         | Lista vacía y mensaje informativo                        |
| Fechas inválidas           | 422         | Detalle de errores de validación                         |
| Destino inválido           | 422         | Detalle de errores de validación                         |
| Error de proveedor externo | 503         | Mensaje indicando indisponibilidad temporal del servicio |

---

## Endpoint asociado a RF-005 Gestión de Alojamiento (Hoteles) 

| Método | Ruta                    | Auth requerida |
| ------ | ----------------------- | -------------- |
| GET    | `/api/v1/hotels/hoteles` | Sí             |

---
## Reglas de negocio de RF -004 Gestión de Vuelos

RN-001: Solo los usuarios con rol de Agente de Viajes pueden acceder al catálogo de alojamientos.
RN-002: La fecha de salida debe ser posterior a la fecha de entrada.
RN-003: El sistema solo mostrará hoteles con disponibilidad confirmada para las fechas consultadas.
RN-004: Los resultados deben incluir información básica del alojamiento: nombre, categoría, ubicación, precio y disponibilidad.
RN-005: El sistema debe permitir aplicar filtros por categoría, capacidad y presupuesto.
RN-006: La selección de un hotel no implica una reserva automática.
RN-007: Los precios mostrados deben corresponder a la disponibilidad vigente al momento de la consulta.

---


# RF-006 — Catálogo de Tours y Actividades

<!-- ¿Qué? Requisito funcional que permite al agente de viajes buscar y seleccionar tours, actividades y experiencias disponibles para los clientes. 
¿Para qué? Facilitar la creación de itinerarios personalizados incorporando actividades acordes a los intereses, preferencias y perfil del cliente. 
¿Impacto? El agente podrá complementar las propuestas de viaje con experiencias relevantes, mejorando la satisfacción del cliente y el valor del servicio ofrecido. 
-->
---
## Identificación de RF-006 Catálogo de Tours y Actividades

| Campo         | Valor                           |
| ------------- | ------------------------------- |
| **ID**        | RF-006                          |
| **Nombre**    | Catálogo de Tours y Actividades |
| **Módulo**    | Gestión de Productos Turísticos |
| **Prioridad** | Alta                            |
| **Estado**    | Implementado                    |
| **Fecha**     | Abril 2026                      |

---
## Descripción de RF-006 Catálogo de Tours y Actividades

El sistema debe permitir que un agente de viajes consulte, filtre y seleccione tours, excursiones, actividades recreativas y experiencias turísticas disponibles para un cliente. La búsqueda deberá considerar factores como destino, fechas, categoría de actividad, rango de precio, duración y perfil del viajero. El sistema mostrará únicamente actividades disponibles que cumplan con los criterios establecidos.

---
## Entradas de RF-006 Catálogo de Tours y Actividades

| Campo               | Tipo           | Obligatorio | Validaciones                                       |
| ------------------- | -------------- | ----------- | -------------------------------------------------- |
| `destination`       | Texto          | Sí          | Destino válido y reconocido por el sistema         |
| `activity_date`     | Fecha          | Sí          | Fecha igual o posterior a la fecha actual          |
| `activity_category` | Texto          | No          | Categoría válida registrada en el sistema          |
| `traveler_profile`  | Texto          | No          | Perfil válido (familiar, aventura, cultural, etc.) |
| `max_budget`        | Número decimal | No          | Mayor a 0                                          |
| `duration_hours`    | Número entero  | No          | Mayor a 0                                          |
| `participants`      | Número entero  | No          | Mayor a 0                                          |

---
## Proceso de RF-006 Catálogo de Tours y Actividades

1. El agente ingresa los criterios de búsqueda de actividades.
2. El sistema valida los parámetros proporcionados.
3. El sistema consulta las actividades disponibles en la base de datos o proveedores integrados.
4. Se recuperan las actividades que coinciden con el destino y la fecha seleccionados.
5. El sistema aplica filtros adicionales según categoría, perfil del viajero, duración y presupuesto.
6. Se ordenan los resultados según relevancia, disponibilidad o criterio seleccionado.
7. El sistema muestra al agente la lista de actividades disponibles junto con sus detalles principales.
8. El agente selecciona una o varias actividades para incorporarlas al itinerario o propuesta de viaje.
   
---
## Salidas de RF-006 Catálogo de Tours y Actividades

| Escenario                   | Código HTTP | Respuesta                                                  |
| --------------------------- | ----------- | ---------------------------------------------------------- |
| Búsqueda exitosa            | 200         | Lista de actividades disponibles con información relevante |
| No existen resultados       | 200         | Lista vacía y mensaje informativo                          |
| Datos de búsqueda inválidos | 422         | Detalle de errores de validación                           |
| Destino inválido            | 422         | Detalle de errores de validación                           |
| Error de proveedor externo  | 503         | Mensaje indicando indisponibilidad temporal del servicio   |

---
## Endpoint asociado de RF-006 Catálogo de Tours y Actividades

| Método | Ruta                        | Auth requerida |
| ------ | --------------------------- | -------------- |
| GET    | `/api/v1/activities/___  ` | Sí             |

---
## Reglas de negocio de RF-006 Catálogo de Tours y Actividades

- RN-001: Solo los usuarios con rol de Agente de Viajes pueden acceder al catálogo de tours y actividades.
- RN-002: El sistema debe mostrar únicamente actividades disponibles para la fecha seleccionada.
- RN-003: Los resultados deben incluir información básica como nombre, descripción, ubicación, duración, precio y disponibilidad.
- RN-004: El sistema debe permitir filtrar actividades por categoría, perfil del viajero, duración y presupuesto.
- RN-005: Una actividad seleccionada puede incorporarse al itinerario sin generar una reserva automática.
- RN-006: Las actividades pueden pertenecer a categorías como aventura, cultural, gastronómica, naturaleza, entretenimiento o bienestar.
- RN-007: Los precios y disponibilidad deben reflejar la información vigente proporcionada por los proveedores al momento de la consulta.
- RN-008: El sistema debe permitir seleccionar múltiples actividades para un mismo itinerario.
---

# RF-007 — Catálogo de Transportes y Traslados Terrestres

<!-- ¿Qué? Requisito funcional que permite al agente de viajes buscar y seleccionar servicios de transporte terrestre disponibles. 
¿Para qué? Facilitar la planificación integral de los viajes mediante la incorporación de opciones de movilidad acordes al itinerario y necesidades del cliente.
¿Impacto? El agente podrá complementar las propuestas de viaje con soluciones de transporte adecuadas, optimizando la experiencia y logística del cliente durante su desplazamiento.
-->
---
## Identificación de RF-007 — Catálogo de Transportes y Traslados Terrestres

| Campo         | Valor                                          |
| ------------- | ---------------------------------------------- |
| **ID**        | RF-007                                         |
| **Nombre**    | Catálogo de Transportes y Traslados Terrestres |
| **Módulo**    | Gestión de Productos Turísticos                |
| **Prioridad** | Alta                                           |
| **Estado**    | Implementado                                   |
| **Fecha**     | Abril 2026                                     |

---
## Descripción de RF-007 — Catálogo de Transportes y Traslados Terrestres

El sistema debe permitir que un agente de viajes consulte, filtre y seleccione servicios de transporte terrestre disponibles para un cliente. Entre los servicios contemplados se incluyen traslados privados, traslados compartidos, alquiler de vehículos y transporte ferroviario. La búsqueda deberá considerar origen, destino, fechas, horarios, capacidad requerida y presupuesto estimado.
---

## Entradas de RF-007 — Catálogo de Transportes y Traslados Terrestres

| Campo                | Tipo           | Obligatorio | Validaciones                              |
| ---------------------| -------------- | ----------- | ----------------------------------------- |
| `origen`             | Texto          | Sí          | Ubicación válida registrada en el sistema |
| `destino`            | Texto          | Sí          | Ubicación válida registrada en el sistema |
| `Fecha de viaje`     | Fecha          | Sí          | Fecha igual o posterior a la fecha actual |
| `Tipo de trasnporte` | Texto          | No          | Tipo válido (traslado, alquiler, tren)    |
| `Pasajeros`          | Número entero  | Sí          | Debe ser mayor a 0                        |
| `¨Horas de salida`   | Hora           | No          | Formato de hora válido                    |
| `Presupuesto maximo` | Número decimal | No          | Debe ser mayor a 0                        |

---

## Proceso de RF-007 — Catálogo de Transportes y Traslados Terrestres

1. El agente ingresa los criterios de búsqueda del servicio de transporte.
2. El sistema valida la información proporcionada.
3. El sistema consulta los proveedores de transporte integrados o la base de datos correspondiente.
4. Se obtienen los servicios disponibles para el origen, destino y fecha especificados.
5. El sistema aplica filtros según tipo de transporte, capacidad y presupuesto.
6. Se ordenan los resultados de acuerdo con disponibilidad, precio o criterio seleccionado.
7. El sistema presenta al agente las opciones disponibles junto con sus detalles principales.
8. El agente selecciona uno o varios servicios para incorporarlos al itinerario o propuesta de viaje.

---

## Salidas de RF-007 — Catálogo de Transportes y Traslados Terrestres

| Escenario                   | Código HTTP | Respuesta                                                |
| --------------------------- | ----------- | -------------------------------------------------------- |
| Búsqueda exitosa            | 200         | Lista de servicios de transporte disponibles             |
| No existen resultados       | 200         | Lista vacía y mensaje informativo                        |
| Datos de búsqueda inválidos | 422         | Detalle de errores de validación                         |
| Origen o destino inválido   | 422         | Detalle de errores de validación                         |
| Error de proveedor externo  | 503         | Mensaje indicando indisponibilidad temporal del servicio |

---

## Endpoint asociado de RF-007 - Catálogo de Transportes y Traslados Terrestres

| Método | Ruta                        | Auth requerida |
| ------ | --------------------------- | -------------- |
| GET    | `/api/v1/transports/___ `   | Sí             |

--- 

## Reglas de negocio de RF-007 - Catálogo de Transportes y Traslados Terrestres

- RN-001: Solo los usuarios con rol de Agente de Viajes pueden acceder al catálogo de transportes y traslados terrestres.
- RN-002: El sistema debe mostrar únicamente servicios disponibles para la fecha y ruta consultadas.
- RN-003: Los resultados deben incluir información básica como proveedor, tipo de servicio, horarios, capacidad, precio y disponibilidad.
- RN-004: El sistema debe permitir filtrar resultados por tipo de transporte, capacidad y presupuesto.
- RN-005: Los tipos de transporte soportados incluyen traslados privados, traslados compartidos, alquiler de vehículos y servicios ferroviarios.
- RN-006: La selección de un servicio no implica la confirmación automática de una reserva.
- RN-007: Los precios y disponibilidad deben corresponder a la información vigente proporcionada por los proveedores al momento de la consulta.
- RN-008: El sistema debe permitir seleccionar múltiples servicios de transporte para un mismo itinerario cuando sea necesario.
- RN-009: El origen y el destino no pueden ser iguales para una misma consulta.

---

# RF-008 — Construcción de Itinerarios Personalizados

<!--
¿Qué? Requisito funcional que permite al agente de viajes construir itinerarios día por día combinando distintos servicios turísticos. 
¿Para qué? Facilitar la planificación integral y personalizada de viajes adaptados a las necesidades, preferencias y restricciones del cliente. 
¿Impacto? Permite estructurar propuestas de viaje completas, coherentes y editables, mejorando la eficiencia del agente y la experiencia del cliente.
-->
---


# Identificación de RF-008 - Construcción de Itinerarios Personalizados

| Campo         | Valor                                      |
| ------------- | ------------------------------------------ |
| **ID**        | RF-008                                     |
| **Nombre**    | Construcción de Itinerarios Personalizados |
| **Módulo**    |                                            |
| **Prioridad** | Alta                                       |
| **Estado**    | Implementado                               |
| **Fecha**     | Abril 2026                                 |

---

# Descripción de RF-008 - Construcción de Itinerarios Personalizados

El sistema debe permitir que un agente de viajes cree, edite y gestione itinerarios personalizados organizados por días. Cada itinerario podrá incluir diferentes servicios como vuelos, alojamientos, transportes, tours y actividades. El sistema debe permitir la construcción flexible del itinerario, ajustando el orden, duración y combinación de servicios según las preferencias del cliente.

---
# Entradas de RF-008 - Construcción de Itinerarios Personalizados

| Campo          | Tipo           | Obligatorio | Validaciones                        |
| -------------- | -------------- | ----------- | ----------------------------------- |
| `client_id`    | Texto          | Sí          | Identificador válido del cliente    |
| `trip_name`    | Texto          | Sí          | No vacío, máximo 100 caracteres     |
| `start_date`   | Fecha          | Sí          | Igual o posterior a la fecha actual |
| `end_date`     | Fecha          | Sí          | Debe ser posterior a `start_date`   |
| `destinations` | Lista de texto | Sí          | Al menos un destino válido          |
| `budget`       | Número decimal | No          | Mayor a 0                           |


---

# Proceso de RF-008 - Construcción de Itinerarios Personalizados

1. El agente crea un nuevo itinerario para un cliente.
2. El sistema valida los datos generales del viaje.
3. El sistema inicializa la estructura del itinerario por días según el rango de fechas.
4. El agente añade servicios al itinerario (vuelos, hoteles, transportes, actividades y tours).
5. El sistema valida la compatibilidad básica entre fechas y servicios seleccionados.
6. El agente organiza los elementos del itinerario día por día.
7. El sistema guarda los cambios en tiempo real o bajo confirmación del usuario.
8. El sistema permite previsualizar el itinerario completo antes de su finalización.

---

# Salidas de RF-008 - Construcción de Itinerarios Personalizados

| Escenario                      | Código HTTP | Respuesta                                         |
| ------------------------------ | ----------- | ------------------------------------------------- |
| Itinerario creado exitosamente | 201         | Itinerario generado con estructura diaria         |
| Itinerario actualizado         | 200         | Confirmación de actualización del itinerario      |
| Datos inválidos                | 422         | Detalle de errores de validación                  |
| Cliente no encontrado          | 404         | Mensaje indicando cliente inexistente             |
| Conflicto de fechas            | 409         | Mensaje de incompatibilidad en el rango de fechas |

---
# Endpoint asociado de RF-008 - Construcción de Itinerarios Personalizados

| Método | Ruta                       | Auth requerida |
| ------ | -------------------------- | -------------- |
| POST   | `/api/v1/itineraries`      | Sí             |
| PUT    | `/api/v1/itineraries/{id}` | Sí             |

---

# Reglas de negocio de RF-008 Construcción de Itinerarios Personalizados

- RN-001: Solo usuarios con rol de Agente de Viajes pueden crear o modificar itinerarios.
- RN-002: Un itinerario debe estar asociado a un cliente válido y activo.
- RN-003: Las fechas del itinerario deben ser coherentes entre sí y con los servicios agregados.
- RN-004: Un itinerario se estructura obligatoriamente por días dentro del rango definido.
- RN-005: El sistema debe permitir agregar múltiples servicios por día sin restricciones funcionales.
- RN-006: Los cambios en el itinerario deben poder guardarse progresivamente.
- RN-007: El presupuesto del itinerario debe poder ser estimado y actualizado dinámicamente.
- RN-008: No se permite publicar o finalizar un itinerario con inconsistencias de fechas o servicios no disponibles.
- RN-009: El sistema debe permitir previsualizar el itinerario completo antes de su confirmación final.

---

## RF-009 — Gestión de Disponibilidad y Tarifas de Proveedores
<!--
¿Qué? Requisito funcional que permite la integración con proveedores externos para obtener disponibilidad y tarifas en tiempo real. 
¿Para qué? Garantizar que los agentes de viajes trabajen con información actualizada y puedan comparar opciones de forma automática. 
¿Impacto? Mejora la precisión de precios y disponibilidad, reduce errores de reserva y optimiza la toma de decisiones en la planificación de viajes.
-->
---

# Identificación de RF-009 - Gestión de Disponibilidad y Tarifas de Proveedores

| Campo         | Valor                                              |
| ------------- | -------------------------------------------------- |
| **ID**        | RF-009                                             |
| **Nombre**    | Gestión de Disponibilidad y Tarifas de Proveedores |
| **Módulo**    | Integraciones y Motor de Tarifas                   |
| **Prioridad** | Alta                                               |
| **Estado**    | Implementado                                       |
| **Fecha**     | Abril 2026                                         |

---
# Descripción - Gestión de Disponibilidad y Tarifas de Proveedores

El sistema debe integrarse con proveedores externos de servicios turísticos (vuelos, hoteles, transporte y actividades) para consultar en tiempo real la disponibilidad y tarifas actualizadas. Además, debe permitir consolidar y comparar automáticamente las opciones obtenidas de distintos proveedores, presentando al agente la mejor alternativa según criterios como precio, disponibilidad, condiciones y calidad del servicio.

---

# Entradas de RF-009 - Gestión de Disponibilidad y Tarifas de Proveedores

| Campo          | Tipo          | Obligatorio | Validaciones                                         |
| -------------- | ------------- | ----------- | ---------------------------------------------------- |
| `service_type` | Texto         | Sí          | Valores válidos: vuelo, hotel, transporte, actividad |
| `origin`       | Texto         | No          | Requerido para vuelos y transportes                  |
| `destination`  | Texto         | Sí          | Destino válido registrado                            |
| `start_date`   | Fecha         | Sí          | Igual o posterior a la fecha actual                  |
| `end_date`     | Fecha         | No          | Debe ser posterior a `start_date` cuando aplique     |
| `passengers`   | Número entero | Sí          | Mayor a 0                                            |
| `filters`      | Objeto JSON   | No          | Debe cumplir esquema definido por el sistema         |

---

# Proceso de RF-009 - Gestión de Disponibilidad y Tarifas de Proveedores

1. El sistema recibe una solicitud de consulta de disponibilidad o tarifas.
2. Valida los parámetros de entrada según el tipo de servicio.
3. Se envía la solicitud a uno o múltiples proveedores externos integrados.
4. El sistema recibe respuestas con disponibilidad y precios en tiempo real.
5. Se normalizan los datos provenientes de distintos proveedores.
6. El sistema realiza una comparación automática de opciones según criterios predefinidos.
7. Se ordenan los resultados por mejor relación calidad-precio, disponibilidad o filtros del agente.
8. El sistema retorna las opciones consolidadas al módulo correspondiente para su visualización o uso en itinerarios.

---

# Salidas de RF-009 - Gestión de Disponibilidad y Tarifas de Proveedores

| Escenario                  | Código HTTP | Respuesta                                                  |
| -------------------------- | ----------- | ---------------------------------------------------------- |
| Consulta exitosa           | 200         | Lista consolidada de opciones con tarifas y disponibilidad |
| Sin disponibilidad         | 200         | Lista vacía con mensaje informativo                        |
| Error de proveedor externo | 503         | Respuesta parcial o error indicando falla de integración   |
| Parámetros inválidos       | 422         | Detalle de errores de validación                           |
| Timeout en proveedores     | 504         | Mensaje de tiempo de espera agotado                        |

---

# Endpoint asociado de RF-009 - Gestión de Disponibilidad y Tarifas de Proveedores

| Método | Ruta                       | Auth requerida |
| ------ | -------------------------- | -------------- |
| POST   | `/api/v1/providers/`       | Sí             |

---
# Reglas de negocio de RF-009

- RN-001: El sistema debe consultar múltiples proveedores cuando estén disponibles para el mismo servicio.
- RN-002: La información de tarifas y disponibilidad debe ser en tiempo real o con la menor latencia posible.
- RN-003: En caso de discrepancias entre proveedores, se debe priorizar la información más reciente.
- RN-004: El sistema debe normalizar los datos recibidos para mantener un formato consistente.
- RN-005: La comparación de opciones debe considerar al menos precio, disponibilidad y condiciones del servicio.
- RN-006: El sistema debe manejar fallos parciales sin afectar la respuesta global cuando sea posible.
- RN-007: Las consultas deben poder ser utilizadas por otros módulos como itinerarios, vuelos, hoteles y actividades.

---

## RF-010 — Generación Automática de Cotización
<!-- 
¿Qué? Requisito funcional que permite la generación automática de cotizaciones a partir de un itinerario completo. 
¿Para qué? Agilizar el proceso de venta de viajes mediante la creación de propuestas detalladas sin intervención manual del agente.
¿Impacto? Reduce tiempos operativos, estandariza las cotizaciones y mejora la experiencia del cliente al recibir propuestas rápidas y claras.
-->
---

# Identificación de RF-010 - Generación Automática de Cotización

| Campo         | Valor                               |
| ------------- | ----------------------------------- |
| **ID**        | RF-010                              |
| **Nombre**    | Generación Automática de Cotización |
| **Módulo**    | Cotizaciones y Ventas               |
| **Prioridad** | Alta                                |
| **Estado**    | Implementado                        |
| **Fecha**     | Abril 2026                          |

---

# Descripción de RF-010 - Generación Automática de Cotización

El sistema debe generar automáticamente una cotización detallada, estructurada y visualmente clara una vez que el agente finaliza un itinerario. La cotización debe consolidar todos los servicios incluidos (vuelos, hoteles, transporte, actividades y tours), mostrando costos desglosados, totales, impuestos aplicables y condiciones del viaje, sin requerir intervención manual.

---

# Entradas de RF-010  - Generación Automática de Cotización

| Campo          | Tipo           | Obligatorio | Validaciones                                  |
| -------------- | -------------- | ----------- | --------------------------------------------- |
| `itinerary_id` | Texto          | Sí          | Identificador válido de itinerario finalizado |
| `client_id`    | Texto          | Sí          | Cliente asociado existente y activo           |
| `currency`     | Texto          | No          | Código de moneda válido (ISO 4217)            |
| `apply_taxes`  | Booleano       | No          | Valor verdadero o falso                       |
| `discounts`    | Número decimal | No          | Mayor o igual a 0                             |

---

# Proceso de RF-010 - Generación Automática de Cotización

1. El sistema detecta que un itinerario ha sido finalizado o marcado como listo para cotización.
2. Valida que el itinerario contenga todos los servicios obligatorios.
3. Recupera la información completa del itinerario (vuelos, hoteles, transporte, actividades y tours).
4. Obtiene precios actualizados de cada servicio desde el motor de tarifas.
5. Calcula subtotales, impuestos, descuentos y total final.
6. Genera una estructura de cotización detallada y estandarizada.
7. Formatea la cotización en un formato visual claro (PDF o vista digital).
8. Almacena la cotización generada y la asocia al cliente y al itinerario.
9. Notifica al agente y/o sistema que la cotización está disponible.

---
# Salidas de RF-010 - Generación Automática de Cotización

| Escenario                        | Código HTTP | Respuesta                                            |
| -------------------------------- | ----------- | ---------------------------------------------------- |
| Cotización generada exitosamente | 201         | Cotización creada con detalle completo               |
| Itinerario incompleto            | 422         | Mensaje indicando servicios faltantes                |
| Itinerario no encontrado         | 404         | Mensaje de recurso inexistente                       |
| Error en cálculo de tarifas      | 502         | Mensaje de error en generación de cotización         |
| Error de proveedores externos    | 503         | Cotización no generada por indisponibilidad de datos |

---

# Endpoint asociado de RF-010 - Generación Automática de Cotización

| Método | Ruta                      | Auth requerida |
| ------ | ------------------------- | -------------- |
| POST   | `/api/v1/quotes/`         | Sí             |

---

## Reglas de negocio de RF-010

- RN-001: Solo itinerarios marcados como completos pueden generar cotizaciones.
- RN-002: La cotización debe incluir todos los servicios del itinerario sin omisiones.
- RN-003: Los precios utilizados deben ser obtenidos en tiempo real o la última actualización válida.
- RN-004: La cotización debe incluir desglose detallado de costos (subtotales, impuestos y total final).
- RN-005: El sistema debe permitir aplicar descuentos antes de la generación final.
- RN-006: La moneda de la cotización debe ser consistente en todo el documento.
- RN-007: La cotización generada debe quedar almacenada para futuras consultas o modificaciones.
- RN-008: El sistema debe notificar automáticamente la disponibilidad de la cotización al agente o sistema externo.
- RN-009: No se permite generar cotizaciones si existen servicios del itinerario sin disponibilidad confirmada.

---

## RF-011 - Visualización y Gestión de Cotización

<!-- 
¿Qué? Requisito funcional que permite al cliente visualizar, descargar y gestionar una cotización generada.
¿Para qué? Habilitar la interacción del cliente con la propuesta de viaje, permitiendo su revisión, aceptación o rechazo.
¿Impacto? Mejora la experiencia del cliente y agiliza el ciclo de venta al permitir decisiones directas desde el portal de autoservicio.
-->

---

# Identificación de RF-011 - Visualización y Gestión de Cotización

| Campo         | Valor                                 |
| ------------- | ------------------------------------- |
| **ID**        | RF-011                                |
| **Nombre**    | Visualización y Gestión de Cotización |
| **Módulo**    | Cotizaciones y Portal del Cliente     |
| **Prioridad** | Alta                                  |
| **Estado**    | Implementado                          |
| **Fecha**     | Abril 2026                            |

--- 

# Descripción - Visualización y Gestión de Cotización

El sistema debe permitir que un cliente registrado pueda visualizar una cotización generada a partir de un itinerario, revisar su contenido detallado, descargarla en formato PDF, enviar comentarios al agente de viajes y tomar una decisión final de aceptación o rechazo desde su portal de autoservicio.

---

# Entradas de RF-011 - Visualización y Gestión de Cotización 

| Campo             | Tipo  | Obligatorio | Validaciones                                 |
| ----------------- | ----- | ----------- | -------------------------------------------- |
| `quote_id`        | Texto | Sí          | Identificador válido de cotización existente |
| `client_id`       | Texto | Sí          | Debe corresponder al cliente autenticado     |
| `comments`        | Texto | No          | Máximo 1000 caracteres                       |
| `decision`        | Texto | No          | Valores: `accepted`, `rejected`, `pending`   |
| `download_format` | Texto | No          | Valor permitido: `pdf`                       |

---
# Proceso de RF-011 - Visualización y Gestión de Cotización

1. El cliente accede a su portal de autoservicio autenticado.
2. El sistema recupera las cotizaciones asociadas al cliente.
3. El cliente selecciona una cotización específica para visualizarla.
4. El sistema muestra el detalle completo de la cotización (servicios, precios, impuestos y total).
5. El cliente puede descargar la cotización en formato PDF.
6. El cliente puede agregar comentarios o solicitudes de modificación.
7. El cliente puede aceptar o rechazar la cotización.
8. El sistema registra la decisión y notifica al agente de viajes.
10. Si es aceptada, el sistema actualiza el estado de la cotización a “aprobada”.
    
---
# Salidas de RF-011 - Visualización y Gestión de Cotización

| Escenario                          | Código HTTP | Respuesta                          |
| ---------------------------------- | ----------- | ---------------------------------- |
| Cotización consultada exitosamente | 200         | Detalle completo de la cotización  |
| PDF generado                       | 200         | Archivo descargable en formato PDF |
| Cotización aceptada                | 200         | Confirmación de aprobación         |
| Cotización rechazada               | 200         | Confirmación de rechazo            |
| Cotización no encontrada           | 404         | Mensaje de recurso inexistente     |
| Acceso no autorizado               | 403         | Mensaje de acceso denegado         |

---

# Endpoint asociado de RF-011 - Visualización y Gestión de Cotización

| Método | Ruta                                 | Auth requerida |
| ------ | ------------------------------------ | -------------- |
| GET    | `/api/v1/quotes/{quote_id}`          | Sí             |
| POST   | `/api/v1/quotes/{quote_id}/decision` | Sí             |
| GET    | `/api/v1/quotes/{quote_id}/download` | Sí             |

---

# Reglas de negocio de RF-011 - Visualización y Gestión de Cotización

- RN-001: Solo el cliente propietario de la cotización puede acceder a ella.
- RN-002: La cotización solo puede ser aceptada o rechazada por el cliente autenticado.
- RN-003: Una cotización aceptada no puede volver a estado “pendiente”.
- RN-004: El cliente puede agregar comentarios en cualquier estado previo a la decisión final.
- RN-005: La cotización debe conservar su versión original para auditoría.
- RN-006: La descarga en PDF debe reflejar exactamente la versión vigente de la cotización.
- RN-007: El sistema debe notificar automáticamente al agente cuando el cliente toma una decisión.
- RN-008: El acceso a cotizaciones debe requerir autenticación válida y sesión activa.

--- 

## RF-012 - Flujo de Reserva y Pago
<!-- 
¿Qué? 
Requisito funcional que permite procesar reservas de servicios y gestionar pagos de clientes. 
¿Para qué? Completar el ciclo de venta de un viaje asegurando la confirmación de servicios y la transacción económica. 
¿Impacto? Permite la conversión de cotizaciones en reservas reales, garantizando seguridad en pagos, integración con proveedores y soporte multimoneda. 
-->
---

# Identificación de RF-012 - Flujo de Reserva y Pago

| Campo         | Valor                   |
| ------------- | ----------------------- |
| **ID**        | RF-012                  |
| **Nombre**    | Flujo de Reserva y Pago |
| **Módulo**    | Reservas                |
| **Prioridad** | Alta                    |
| **Estado**    | Implementado            |
| **Fecha**     | Abril 2026              |

---

# Descripción de RF-012 - Flujo de Reserva y Pago

El sistema debe permitir la conversión de una cotización aprobada en una reserva confirmada, gestionando la disponibilidad con los proveedores y procesando el pago del cliente de forma segura. El flujo debe soportar múltiples servicios turísticos (vuelos, hoteles, transporte y actividades), múltiples métodos de pago y múltiples divisas, garantizando consistencia entre la reserva y la transacción económica.

---

# Entradas de RF-012 - Flujo de Reserva y Pago


| Campo            | Tipo           | Obligatorio | Validaciones                                       |
| ---------------- | -------------- | ----------- | -------------------------------------------------- |
| `quote_id`       | Texto          | Sí          | Debe existir y estar en estado “aprobada”          |
| `client_id`      | Texto          | Sí          | Cliente válido y autenticado                       |
| `payment_method` | Texto          | Sí          | Valores válidos: tarjeta, transferencia, wallet    |
| `currency`       | Texto          | Sí          | Código de moneda válido (ISO 4217)                 |
| `amount`         | Número decimal | Sí          | Mayor a 0                                          |
| `installments`   | Número entero  | No          | Mayor o igual a 1                                  |
| `billing_info`   | Objeto JSON    | Sí          | Debe cumplir esquema de facturación definido       |
| `services`       | Lista          | Sí          | Debe contener servicios confirmados del itinerario |

---

# Proceso de RF-012 - Flujo de Reserva y Pago

1. El cliente o agente inicia el proceso de reserva a partir de una cotización aprobada.
2. El sistema valida que la cotización esté vigente y en estado “aprobada”.
3. Se verifican nuevamente la disponibilidad de todos los servicios con los proveedores.
4. Si algún servicio no está disponible, el sistema notifica el conflicto y detiene el proceso o propone alternativas.
5. Se calcula el monto final a pagar según moneda, impuestos y posibles cargos adicionales.
6. El sistema envía la solicitud de pago al gateway de pagos seguro.
7. Se procesa la transacción según el método de pago seleccionado.
8. Si el pago es exitoso, el sistema confirma las reservas con los proveedores.
9. Se generan los códigos de reserva (PNR u otros identificadores).
10. El sistema almacena la reserva final y actualiza el estado de la cotización a “confirmada”.
11. Se notifica al cliente, agente y sistema interno sobre la confirmación.

---

# Salidas de RF-012 -  Flujo de Reserva y Pago

| Escenario                       | Código HTTP | Respuesta                                  |
| ------------------------------- | ----------- | ------------------------------------------ |
| Reserva confirmada exitosamente | 201         | Reserva creada con códigos de confirmación |
| Pago exitoso, reserva pendiente | 202         | Pago procesado, reserva en confirmación    |
| Fallo en pago                   | 402         | Transacción rechazada                      |
| Servicio no disponible          | 409         | Conflicto de disponibilidad                |
| Cotización inválida             | 404         | Cotización no encontrada o expirada        |
| Error de proveedor              | 503         | Fallo en confirmación con proveedores      |

---

# Endpoint asociado de RF-012 - Flujo de Reserva y Pago

| Método | Ruta                       | Auth requerida |
| ------ | -------------------------- | -------------- |
| POST   | `/api/v1/bookings/confirm` | Sí             |
| POST   | `/api/v1/payments/process` | Sí             |

---
 
# Reglas de negocio de RF-012 - Flujo de Reserva y Pago

- RN-001: Solo cotizaciones en estado “aprobada” pueden convertirse en reservas.
- RN-002: El sistema debe revalidar disponibilidad en tiempo real antes de confirmar la reserva.
- RN-003: El pago debe procesarse antes de confirmar definitivamente la reserva.
- RN-004: El sistema debe soportar múltiples métodos de pago y múltiples divisas.
- RN-005: No se permite confirmar reservas con servicios no disponibles.
- RN-006: Cada servicio confirmado debe generar su identificador de reserva (PNR o equivalente).
- RN-007: El proceso de reserva debe ser transaccional; si falla el pago o la confirmación, debe revertirse.
- RN-008: Todas las transacciones deben registrarse para auditoría y trazabilidad.

---
# REQUISITOS NO FUNCIONALES
---
# RNF-001 — Seguridad

<!--
  ¿Qué? Requisito no funcional que define los estándares de seguridad del sistema.
  ¿Para qué? Garantizar que los datos sensibles estén protegidos contra ataques comunes.
  ¿Impacto? Un fallo de seguridad podría exponer contraseñas, tokens y datos personales.
-->
---
## Identificación de RNF-001 — Seguridad

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-001                                                |
| **Nombre**        | Seguridad                                              |
| **Categoría**     | Seguridad de la información                            |
| **Prioridad**     | Crítica                                                |
| **Estado**        | Implementado                                           |

---

## Requisitos de RNF-001 — Seguridad

### RNF-001.1 — Hashing de contraseñas
Las contraseñas de los usuarios deben almacenarse mediante hashing con el algoritmo **bcrypt**. Nunca se almacenan en texto plano ni se incluyen en respuestas de la API.

### RNF-001.2 — Tokens JWT
La autenticación debe basarse en tokens JWT (JSON Web Tokens) firmados con algoritmo **HS256**:
- **Access token**: duración de 15 minutos.
- **Refresh token**: duración de 7 días.
- La clave secreta debe tener mínimo 32 caracteres y almacenarse en variable de entorno.

### RNF-001.3 — Prevención de enumeración de usuarios
Los mensajes de error en endpoints de autenticación deben ser genéricos:
- En login: "Incorrect email or password" (sin distinguir si el email existe).
- En forgot-password: siempre retornar el mismo mensaje, sin revelar si el email está registrado.

### RNF-001.4 — Validación de entradas
Todas las entradas del usuario deben validarse tanto en el frontend como en el backend:
- Frontend: validación con lógica React antes de enviar.
- Backend: validación con Pydantic (schemas tipados y restrictivos).

### RNF-001.5 — Protección contra inyección SQL
El sistema debe usar SQLAlchemy ORM para todas las consultas a la base de datos. No se permite SQL crudo sin parametrizar.

### RNF-001.6 — CORS (Cross-Origin Resource Sharing)
- En desarrollo: permitir únicamente `http://localhost:5173`.
- En producción: configurar orígenes específicos; nunca usar `allow_origins=["*"]`.

### RNF-001.7 — Variables de entorno
Toda información sensible (claves secretas, credenciales de BD, configuraciones SMTP) debe almacenarse en archivos `.env` no versionados. Se debe proveer un `.env.example` como plantilla.

### RNF-001.8 — Fortaleza de contraseñas
Las contraseñas deben cumplir requisitos mínimos:
- Mínimo 8 caracteres.
- Al menos 1 letra mayúscula.
- Al menos 1 letra minúscula.
- Al menos 1 número.
  
---

# RNF-002 — Rendimiento
<!--
  ¿Qué? Requisito no funcional que define las expectativas de rendimiento del sistema.
  ¿Para qué? Garantizar una experiencia fluida para el usuario con tiempos de respuesta aceptables.
  ¿Impacto? Un sistema lento afecta la UX y puede causar abandono por parte de los usuarios.
-->
---

## Identificación RNF-002 — Rendimiento

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-002                                                |
| **Nombre**        | Rendimiento                                            |
| **Categoría**     | Rendimiento                                            |
| **Prioridad**     | Alta                                                   |
| **Estado**        | Implementado                                           |

---

## Requisitos 

### RNF-002.1 — Tiempo de respuesta de la API
Los endpoints de la API deben responder en menos de **500 milisegundos** en condiciones normales de carga (excluyendo latencia de red).

### RNF-002.2 — Framework asíncrono
El backend debe utilizar un framework asíncrono (FastAPI + Uvicorn) para manejar múltiples solicitudes concurrentes de forma eficiente sin bloquear el event loop.

### RNF-002.3 — Connection pooling
Las conexiones a la base de datos deben gestionarse mediante un pool de conexiones configurado en SQLAlchemy, evitando la creación/destrucción de conexiones por cada solicitud.

### RNF-002.4 — Build optimizado del frontend
El frontend debe compilarse a un bundle optimizado de producción mediante Vite, aplicando:
- Tree-shaking (eliminación de código no utilizado).
- Minificación de JavaScript y CSS.
- Code splitting para carga eficiente.

### RNF-002.5 — Carga del frontend
La aplicación frontend debe cargar completamente (First Contentful Paint) en menos de **3 segundos** en una conexión de banda ancha estándar.

-------------------------

# RNF-003 — Capacidad de Usuarios Concurrentes

<!-- 
¿Qué? Requisito no funcional que define la capacidad del sistema para soportar usuarios simultáneos. 
¿Para qué? Garantizar que el sistema mantenga estabilidad y rendimiento bajo carga concurrente. 
¿Impacto? Una baja capacidad de concurrencia puede provocar caídas, lentitud o indisponibilidad del servicio.
-->

## Identificación RNF-003 — Capacidad de Usuarios Concurrentes

| Campo         | Valor                              |
| ------------- | ---------------------------------- |
| **ID**        | RNF-003                            |
| **Nombre**    | Capacidad de Usuarios Concurrentes |
| **Categoría** | Escalabilidad / Rendimiento        |
| **Prioridad** | Alta                               |
| **Estado**    | Propuesto                          |

---

## Requisitos RNF-003 — Capacidad de Usuarios Concurrentes

### RNF-003.1 — Soporte de usuarios concurrentes
El sistema debe soportar al menos 500 usuarios concurrentes simultáneos (entre clientes y agentes) sin degradación significativa del servicio.

### RNF-003.2 — Mantenimiento de rendimiento bajo carga
Bajo condiciones de concurrencia objetivo, el sistema debe mantener tiempos de respuesta consistentes, con un p95 menor a 800ms en los endpoints principales.

### RNF-003.3 — Escalabilidad horizontal
El backend debe permitir escalabilidad horizontal, soportando el aumento de usuarios mediante la adición de nuevas instancias sin necesidad de rediseño de la arquitectura.

### RNF-003.4 — Balanceo de carga
El sistema debe operar detrás de un balanceador de carga que distribuya las solicitudes de manera uniforme entre instancias activas.

### RNF-003.5 — Pruebas de carga y estrés
El sistema debe ser validado mediante pruebas de carga y estrés que simulen al menos el 120% de la carga concurrente objetivo, verificando estabilidad y ausencia de caídas.

### RNF-003.6 — Gestión de conexiones
El sistema debe gestionar eficientemente las conexiones concurrentes (HTTP/WebSocket si aplica), evitando bloqueos, fugas de conexiones o saturación del pool.
---

# RNF-004 — Autenticación y Control de Acceso

<!-- 
¿Qué? Requisito no funcional que define los mecanismos de autenticación y autorización del sistema.
¿Para qué? Garantizar que solo usuarios autenticados y autorizados accedan a los recursos correspondientes. 
¿Impacto? La ausencia de control de acceso puede provocar vulnerabilidades, fuga de información o acceso indebido. 
-->
---

## Identificación RNF-004 — Autenticación y Control de Acceso

| Campo         | Valor                             |
| ------------- | --------------------------------- |
| **ID**        | RNF-004                           |
| **Nombre**    | Autenticación y Control de Acceso |
| **Categoría** | Seguridad / Autenticación         |
| **Prioridad** | Alta                              |
| **Estado**    | Propuesto                         |
---

## Requisitos RNF-004 — Autenticación y Control de Acceso

### RNF-004.1 — Autenticación segura
El sistema debe implementar un mecanismo de autenticación seguro basado en tokens (por ejemplo, JWT), garantizando la verificación de identidad en cada solicitud protegida.

### RNF-004.2 — Control de acceso basado en roles (RBAC)
El sistema debe implementar control de acceso basado en roles, diferenciando al menos entre clientes y agentes, con permisos específicos para cada tipo de usuario.

### RNF-004.3 — Protección de rutas y recursos
Todas las rutas, endpoints o recursos sensibles deben estar protegidos y accesibles únicamente para usuarios autenticados con los permisos adecuados.

### RNF-004.4 — Expiración y renovación de sesiones
Los tokens de autenticación deben tener un tiempo de expiración definido y permitir mecanismos seguros de renovación (refresh token o equivalente).

### RNF-004.5 — Protección contra accesos no autorizados
El sistema debe rechazar cualquier intento de acceso a recursos sin autenticación o con permisos insuficientes, registrando estos eventos para auditoría.

### RNF-004.6 — Gestión segura de credenciales
Las credenciales de usuario deben almacenarse de forma segura utilizando hashing fuerte (por ejemplo, bcrypt o Argon2), evitando almacenamiento en texto plano.

### RNF-004.7 — Auditoría de accesos
El sistema debe registrar eventos de inicio de sesión, intentos fallidos y cambios de permisos para fines de auditoría y trazabilidad.
---

# RNF-005 — Auditoría y Trazabilidad de Seguridad
<!-- 
¿Qué? Requisito no funcional que define el registro y monitoreo de eventos del sistema. 
¿Para qué? Permitir auditoría, detección de amenazas y análisis forense ante incidentes.
¿Impacto? Sin trazabilidad, no es posible detectar, investigar ni responder adecuadamente a incidentes de seguridad. 
-->
---

## Identificación RNF-005 — Auditoría y Trazabilidad de Seguridad 

| Campo         | Valor                                 |
| ------------- | ------------------------------------- |
| **ID**        | RNF-005                               |
| **Nombre**    | Auditoría y Trazabilidad de Seguridad |
| **Categoría** | Seguridad / Observabilidad            |
| **Prioridad** | Alta                                  |
| **Estado**    | Pendiente                             |
---

## Requisitos de RNF-005 — Auditoría y Trazabilidad de Seguridad 

### RNF-005.1 — Registro de eventos de seguridad
El sistema debe registrar todos los eventos relevantes de seguridad, incluyendo autenticaciones, intentos fallidos de acceso, cambios de credenciales y elevación de privilegios.

### RNF-005.2 — Registro de actividades operativas
El sistema debe registrar las principales acciones operativas realizadas por los usuarios (clientes y agentes), como creación, modificación y eliminación de datos críticos.

### RNF-005.3 — Trazabilidad de acciones por usuario
Cada evento registrado debe incluir un identificador único de usuario, fecha y hora, tipo de acción y recurso afectado, garantizando trazabilidad completa.

###RNF-005.4 — Inmutabilidad de logs
Los registros de auditoría deben ser inmutables o protegidos contra modificaciones o eliminaciones no autorizadas.

### RNF-005.5 — Centralización de logs
El sistema debe centralizar los logs en un mecanismo de almacenamiento seguro (base de datos de logs o sistema externo de logging), facilitando su consulta y análisis.

### RNF-005.6 — Retención de información
Los logs de auditoría deben conservarse durante un período mínimo definido (por ejemplo, 90 días o según política de seguridad), sin pérdida de información.

### RNF-005.7 — Soporte para detección de anomalías
El sistema debe permitir que los registros sean utilizados por herramientas de monitoreo o análisis para detectar patrones anómalos o posibles amenazas.

---
# RNF-006 — Latencia de API Backend
<!-- 
¿Qué? Requisito no funcional que define los tiempos de respuesta del backend. 
¿Para qué? Garantizar una experiencia fluida del usuario y eficiencia en integraciones con proveedores externos. 
¿Impacto? Una alta latencia degrada la UX, afecta integraciones y puede generar fallos en procesos críticos.
-->
---

## Identificación de RNF-006 — Latencia de API Backend

| Campo         | Valor                   |
| ------------- | ----------------------- |
| **ID**        | RNF-006                 |
| **Nombre**    | Latencia de API Backend |
| **Categoría** | Rendimiento             |
| **Prioridad** | Alta                    |
| **Estado**    | Propuesto               |
---

## Requisitos de RNF-006 — Latencia de API Backend

### RNF-006.1 — Tiempo de respuesta general
Las APIs del backend deben responder en un tiempo promedio inferior a 300 ms bajo condiciones normales de operación, excluyendo latencia de red y de servicios externos.

### RNF-006.2 — Percentiles de latencia
El sistema debe garantizar que al menos el 95% de las solicitudes (p95) se resuelvan en menos de 600 ms.

### RNF-006.3 — Integraciones con proveedores externos
Las integraciones con servicios de terceros deben manejarse de forma eficiente, evitando que bloqueen el flujo principal del sistema mediante técnicas como llamadas asíncronas, colas o timeouts controlados.

### RNF-006.4 — Manejo de timeouts
Las llamadas a APIs externas deben contar con timeouts configurados (máximo recomendado de 2 a 5 segundos, según proveedor) para evitar degradación del rendimiento general.

### RNF-006.5 — Degradación controlada
En caso de alta carga o fallos en servicios externos, el sistema debe implementar mecanismos de fallback o degradación controlada para mantener la disponibilidad del servicio.

### RNF-006.6 — Optimización de consultas
Las operaciones de backend deben optimizar el acceso a base de datos e integraciones, evitando consultas redundantes o innecesarias que incrementen la latencia.
---

# RNF-007 — Compatibilidad y Portabilidad
<!--
  ¿Qué? Requisito no funcional que define los navegadores y entornos soportados.
  ¿Para qué? Garantizar que el sistema funcione correctamente en los entornos objetivo.
  ¿Impacto? Si no se define compatibilidad, podrían surgir errores inesperados en ciertos navegadores.
-->
---
 
## Identificación RNF-007 — Compatibilidad y Portabilidad 

| Campo             | Valor                                                  |
| ----------------- | ------------------------------------------------------ |
| **ID**            | RNF-007                                                |
| **Nombre**        | Compatibilidad y Portabilidad                          |
| **Categoría**     | Compatibilidad                                         |
| **Prioridad**     | Media                                                  |
| **Estado**        | Implementado                                           |
---

## Requisitos

### RNF-006.1 — Navegadores soportados
La aplicación frontend debe funcionar correctamente en las últimas dos versiones estables de:
- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Safari

### RNF-006.2 — Resoluciones de pantalla
La interfaz debe ser funcional desde **320px** de ancho (móviles pequeños) hasta **2560px** (monitores ultrawide).

### RNF-006.3 — Sistema operativo del servidor
El backend debe ejecutarse correctamente en sistemas Linux (entorno de desarrollo y producción).

### RNF-006.4 — Containerización
La base de datos debe ejecutarse en contenedores Docker para garantizar reproducibilidad del entorno de desarrollo.

### RNF-006.5 — Versiones mínimas de runtime
- **Python**: 3.12+
- **Node.js**: 20 LTS+
- **PostgreSQL**: 17+ 
---
















































# 📚 Documentación API AlecTours

**Base URL:** `http://localhost:8000`

---

## 🔐 AUTENTICACIÓN (Auth)

### 1️⃣ Registro de Usuario
- **Método:** `POST`
- **URL:** `/auth/register`
- **Status:** 201 Created

**Request Body:**
```json
{
  "username": "juan_perez",
  "correo_electronico": "juan@example.com",
  "password": "Password123!"
}
```

**Response:**
```json
{
  "message": "Usuario registrado exitosamente. Revisa tu correo para verificar tu cuenta.",
  "user_id": 1,
  "email": "juan@example.com",
  "verification_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Notas:**
- Se envía email de verificación automáticamente
- El usuario NO puede iniciar sesión hasta verificar el email
- Username debe tener 3-50 caracteres

---

### 2️⃣ Verificar Email
- **Método:** `POST`
- **URL:** `/auth/verify-email`
- **Status:** 200 OK

**Query Parameters:**
```
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "message": "Email verificado exitosamente",
  "user_id": 1
}
```

---

### 3️⃣ Iniciar Sesión
- **Método:** `POST`
- **URL:** `/auth/login`
- **Status:** 200 OK

**Request Body:**
```json
{
  "username": "juan_perez",
  "password": "Password123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1
}
```

**Errores Comunes:**
- `401`: Credenciales inválidas
- `403`: Email no verificado

---

## 👥 CLIENTES

### 1️⃣ Crear Cliente
- **Método:** `POST`
- **URL:** `/api/clientes`
- **Status:** 201 Created

**Request Body:**
```json
{
  "nombre": "Carlos García",
  "cedula": "1234567890",
  "telefono": "+57 3001234567",
  "correo": "carlos.garcia@example.com",
  "direccion": "Calle 5 #10-20, Bogotá"
}
```

**Response:**
```json
{
  "id": 1,
  "nombre": "Carlos García",
  "cedula": "1234567890",
  "telefono": "+57 3001234567",
  "correo": "carlos.garcia@example.com",
  "direccion": "Calle 5 #10-20, Bogotá",
  "fecha_creacion": "2026-06-05T21:20:00"
}
```

---

### 2️⃣ Obtener Todos los Clientes
- **Método:** `GET`
- **URL:** `/api/clientes`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Carlos García",
    "cedula": "1234567890",
    "telefono": "+57 3001234567",
    "correo": "carlos.garcia@example.com",
    "direccion": "Calle 5 #10-20, Bogotá"
  }
]
```

---

### 3️⃣ Obtener Cliente por ID
- **Método:** `GET`
- **URL:** `/api/clientes/{cliente_id}`
- **Status:** 200 OK

**Example:**
```
GET /api/clientes/1
```

---

### 4️⃣ Actualizar Cliente
- **Método:** `PUT`
- **URL:** `/api/clientes/{cliente_id}`
- **Status:** 200 OK

**Request Body:**
```json
{
  "nombre": "Carlos García Actualizado",
  "telefono": "+57 3009876543"
}
```

---

### 5️⃣ Eliminar Cliente
- **Método:** `DELETE`
- **URL:** `/api/clientes/{cliente_id}`
- **Status:** 200 OK

**Response:**
```json
{
  "message": "Cliente eliminado exitosamente"
}
```

---

## 👨‍💼 EMPLEADOS

### 1️⃣ Crear Empleado
- **Método:** `POST`
- **URL:** `/api/empleados`
- **Status:** 201 Created

**Request Body:**
```json
{
  "nombre": "Ana Rodríguez",
  "cedula": "9876543210",
  "cargo": "Gerente de Reservas",
  "correo_electronico": "ana.rodriguez@alectours.com",
  "telefono": "+57 3002468135",
  "salario": 3500000,
  "activo": true
}
```

---

### 2️⃣ Obtener Todos los Empleados
- **Método:** `GET`
- **URL:** `/api/empleados`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 3️⃣ Obtener Empleados Activos
- **Método:** `GET`
- **URL:** `/api/empleados/activos/lista`
- **Status:** 200 OK

---

### 4️⃣ Obtener Empleado por ID
- **Método:** `GET`
- **URL:** `/api/empleados/{empleado_id}`
- **Status:** 200 OK

---

### 5️⃣ Actualizar Empleado
- **Método:** `PUT`
- **URL:** `/api/empleados/{empleado_id}`
- **Status:** 200 OK

**Request Body:**
```json
{
  "cargo": "Gerente General",
  "salario": 4000000
}
```

---

### 6️⃣ Eliminar Empleado
- **Método:** `DELETE`
- **URL:** `/api/empleados/{empleado_id}`
- **Status:** 200 OK

---

## 🏨 HOTELES

### 1️⃣ Crear Hotel
- **Método:** `POST`
- **URL:** `/api/hoteles/`
- **Status:** 201 Created

**Request Body:**
```json
{
  "nombre": "Hotel Resort Paradise",
  "ciudad": "Cartagena",
  "ubicacion": "Avenida Costanera, Cartagena",
  "clasificacion": 5,
  "total_habitaciones": 150,
  "descripcion": "Hermoso resort frente al mar con piscinas y spa"
}
```

**Response:**
```json
{
  "id": 1,
  "nombre": "Hotel Resort Paradise",
  "ciudad": "Cartagena",
  "ubicacion": "Avenida Costanera, Cartagena",
  "clasificacion": 5,
  "total_habitaciones": 150,
  "descripcion": "Hermoso resort frente al mar con piscinas y spa"
}
```

---

### 2️⃣ Obtener Todos los Hoteles
- **Método:** `GET`
- **URL:** `/api/hoteles/`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 3️⃣ Obtener Hotel con Detalles Completos
- **Método:** `GET`
- **URL:** `/api/hoteles/{hotel_id}`
- **Status:** 200 OK

**Response:**
```json
{
  "id": 1,
  "nombre": "Hotel Resort Paradise",
  "ciudad": "Cartagena",
  "ubicacion": "Avenida Costanera, Cartagena",
  "clasificacion": 5,
  "total_habitaciones": 150,
  "descripcion": "Hermoso resort frente al mar",
  "habitaciones": [
    {
      "id": 1,
      "numero_habitacion": "101",
      "tipo": "Suite",
      "capacidad": 2,
      "precio_noche": 250000,
      "disponible": true
    }
  ],
  "caracteristicas": [
    {
      "nombre": "Piscina",
      "disponible": true
    }
  ]
}
```

---

### 4️⃣ Actualizar Hotel
- **Método:** `PUT`
- **URL:** `/api/hoteles/{hotel_id}`
- **Status:** 200 OK

**Request Body:**
```json
{
  "descripcion": "Resort 5 estrellas actualizado",
  "clasificacion": 5
}
```

---

### 5️⃣ Eliminar Hotel
- **Método:** `DELETE`
- **URL:** `/api/hoteles/{hotel_id}`
- **Status:** 200 OK

---

## 🛏️ HABITACIONES

### 1️⃣ Crear Habitación
- **Método:** `POST`
- **URL:** `/api/hoteles/{hotel_id}/habitaciones`
- **Status:** 201 Created

**Request Body:**
```json
{
  "numero_habitacion": "202",
  "tipo": "Suite Deluxe",
  "capacidad": 3,
  "precio_noche": 350000,
  "disponible": true,
  "descripcion": "Suite con vista al mar"
}
```

---

### 2️⃣ Obtener Habitaciones de un Hotel
- **Método:** `GET`
- **URL:** `/api/hoteles/{hotel_id}/habitaciones`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 3️⃣ Obtener Habitaciones Disponibles
- **Método:** `GET`
- **URL:** `/api/hoteles/{hotel_id}/habitaciones/disponibles`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 4️⃣ Obtener Habitación por ID
- **Método:** `GET`
- **URL:** `/api/hoteles/habitaciones/{habitacion_id}`
- **Status:** 200 OK

---

### 5️⃣ Actualizar Habitación
- **Método:** `PUT`
- **URL:** `/api/hoteles/habitaciones/{habitacion_id}`
- **Status:** 200 OK

**Request Body:**
```json
{
  "precio_noche": 400000,
  "disponible": false
}
```

---

### 6️⃣ Eliminar Habitación
- **Método:** `DELETE`
- **URL:** `/api/hoteles/habitaciones/{habitacion_id}`
- **Status:** 200 OK

---

## ✨ CARACTERÍSTICAS DE HOTELES

### 1️⃣ Obtener Todas las Características
- **Método:** `GET`
- **URL:** `/api/hoteles/caracteristicas/`
- **Status:** 200 OK

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Piscina"
  },
  {
    "id": 2,
    "nombre": "Spa"
  }
]
```

---

### 2️⃣ Crear Característica
- **Método:** `POST`
- **URL:** `/api/hoteles/caracteristicas/`
- **Status:** 201 Created

**Request Body:**
```json
{
  "nombre": "WiFi Gratis"
}
```

---

### 3️⃣ Añadir Característica a Hotel
- **Método:** `POST`
- **URL:** `/api/hoteles/{hotel_id}/caracteristicas/{caracteristica_id}`
- **Status:** 200 OK

**Query Parameters:**
```
disponible=true
```

---

### 4️⃣ Eliminar Característica de Hotel
- **Método:** `DELETE`
- **URL:** `/api/hoteles/{hotel_id}/caracteristicas/{caracteristica_id}`
- **Status:** 200 OK

---

## 📦 PAQUETES TURÍSTICOS

### 1️⃣ Crear Paquete
- **Método:** `POST`
- **URL:** `/api/paquetes`
- **Status:** 201 Created

**Request Body:**
```json
{
  "nombre": "Escapada Caribeña 3 Noches",
  "descripcion": "Disfruta de playas paradisíacas en Cartagena",
  "precio": 1500000,
  "duracion_dias": 3,
  "destino": "Cartagena",
  "incluye": "Hotel 5 estrellas, desayuno diario, tour ciudad"
}
```

---

### 2️⃣ Obtener Todos los Paquetes
- **Método:** `GET`
- **URL:** `/api/paquetes`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 3️⃣ Obtener Paquete por ID
- **Método:** `GET`
- **URL:** `/api/paquetes/{paquete_id}`
- **Status:** 200 OK

---

### 4️⃣ Actualizar Paquete
- **Método:** `PUT`
- **URL:** `/api/paquetes/{paquete_id}`
- **Status:** 200 OK

**Request Body:**
```json
{
  "precio": 1600000,
  "descripcion": "Escapada mejorada con tours incluidos"
}
```

---

### 5️⃣ Eliminar Paquete
- **Método:** `DELETE`
- **URL:** `/api/paquetes/{paquete_id}`
- **Status:** 200 OK

---

## 🎟️ RESERVAS

### 1️⃣ Crear Reserva
- **Método:** `POST`
- **URL:** `/api/reservas`
- **Status:** 201 Created

**Request Body:**
```json
{
  "id_cliente": 1,
  "id_paquete": 1,
  "fecha_inicio": "2026-07-15",
  "fecha_fin": "2026-07-18",
  "numero_personas": 2,
  "estado": "pendiente"
}
```

**Response:**
```json
{
  "id": 1,
  "id_cliente": 1,
  "id_paquete": 1,
  "fecha_inicio": "2026-07-15",
  "fecha_fin": "2026-07-18",
  "numero_personas": 2,
  "estado": "pendiente",
  "fecha_creacion": "2026-06-05T21:20:00"
}
```

---

### 2️⃣ Obtener Todas las Reservas
- **Método:** `GET`
- **URL:** `/api/reservas`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 3️⃣ Obtener Reservas de un Cliente
- **Método:** `GET`
- **URL:** `/api/reservas/cliente/{cliente_id}`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 4️⃣ Obtener Reservas por Estado
- **Método:** `GET`
- **URL:** `/api/reservas/estado/{estado}`
- **Status:** 200 OK

**Estados válidos:**
- `pendiente`
- `confirmada`
- `cancelada`
- `finalizada`

**Query Parameters:**
```
skip=0
limit=10
```

---

### 5️⃣ Obtener Detalles Completos de Reserva
- **Método:** `GET`
- **URL:** `/api/reservas/{reserva_id}`
- **Status:** 200 OK

**Response:**
```json
{
  "id": 1,
  "id_cliente": 1,
  "id_paquete": 1,
  "fecha_inicio": "2026-07-15",
  "fecha_fin": "2026-07-18",
  "numero_personas": 2,
  "estado": "pendiente",
  "paquete": {
    "id": 1,
    "nombre": "Escapada Caribeña 3 Noches",
    "precio": 1500000
  },
  "pagos": [
    {
      "id": 1,
      "monto": 500000,
      "estado": "pagado"
    }
  ]
}
```

---

### 6️⃣ Actualizar Reserva
- **Método:** `PUT`
- **URL:** `/api/reservas/{reserva_id}`
- **Status:** 200 OK

**Request Body:**
```json
{
  "estado": "confirmada",
  "numero_personas": 3
}
```

---

### 7️⃣ Eliminar Reserva
- **Método:** `DELETE`
- **URL:** `/api/reservas/{reserva_id}`
- **Status:** 200 OK

---

## 💳 MÉTODOS DE PAGO

### 1️⃣ Obtener Métodos de Pago
- **Método:** `GET`
- **URL:** `/api/metodos-pago`
- **Status:** 200 OK

**Response:**
```json
[
  {
    "id": 1,
    "nombre": "Tarjeta de Crédito"
  },
  {
    "id": 2,
    "nombre": "Transferencia Bancaria"
  },
  {
    "id": 3,
    "nombre": "PayPal"
  }
]
```

---

### 2️⃣ Crear Método de Pago
- **Método:** `POST`
- **URL:** `/api/metodos-pago`
- **Status:** 201 Created

**Request Body:**
```json
{
  "nombre": "Criptomonedas"
}
```

---

## 💰 PAGOS

### 1️⃣ Crear Pago
- **Método:** `POST`
- **URL:** `/api/pagos`
- **Status:** 201 Created

**Request Body:**
```json
{
  "id_reserva": 1,
  "monto": 500000,
  "id_metodo_pago": 1,
  "estado": "pagado",
  "fecha_pago": "2026-06-05"
}
```

**Response:**
```json
{
  "id": 1,
  "id_reserva": 1,
  "monto": 500000,
  "id_metodo_pago": 1,
  "estado": "pagado",
  "fecha_pago": "2026-06-05",
  "fecha_creacion": "2026-06-05T21:20:00"
}
```

---

### 2️⃣ Obtener Todos los Pagos
- **Método:** `GET`
- **URL:** `/api/pagos`
- **Status:** 200 OK

**Query Parameters:**
```
skip=0
limit=10
```

---

### 3️⃣ Obtener Pagos de una Reserva
- **Método:** `GET`
- **URL:** `/api/pagos/reserva/{reserva_id}`
- **Status:** 200 OK

---

### 4️⃣ Obtener Pagos por Estado
- **Método:** `GET`
- **URL:** `/api/pagos/estado/{estado}`
- **Status:** 200 OK

**Estados válidos:**
- `pendiente`
- `pagado`
- `rechazado`

---

### 5️⃣ Obtener Pago por ID
- **Método:** `GET`
- **URL:** `/api/pagos/{pago_id}`
- **Status:** 200 OK

---

### 6️⃣ Actualizar Pago
- **Método:** `PUT`
- **URL:** `/api/pagos/{pago_id}`
- **Status:** 200 OK

**Request Body:**
```json
{
  "estado": "pagado",
  "monto": 550000
}
```

---

### 7️⃣ Eliminar Pago
- **Método:** `DELETE`
- **URL:** `/api/pagos/{pago_id}`
- **Status:** 200 OK

---

## ⚠️ CÓDIGOS DE ERROR COMUNES

| Código | Significado |
|--------|------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado exitosamente |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - Credenciales inválidas |
| 403 | Forbidden - Acceso denegado (ej: email no verificado) |
| 404 | Not Found - Recurso no encontrado |
| 409 | Conflict - Conflicto (ej: dependencias, ya existe) |
| 500 | Server Error - Error interno del servidor |

---

## 📝 NOTAS IMPORTANTES

1. **Base URL:** Todos los endpoints comienzan con `http://localhost:8000`
2. **Content-Type:** Usa `application/json` en todos los requests POST/PUT
3. **Validación de Email:** Los usuarios deben verificar su email después de registrarse
4. **Estados válidos:**
   - Reservas: `pendiente`, `confirmada`, `cancelada`, `finalizada`
   - Pagos: `pendiente`, `pagado`, `rechazado`
5. **Paginación:** Usa `skip` y `limit` en los GET (máximo 100 por página)
6. **Formato de Fechas:** `YYYY-MM-DD`

---

## 🚀 FLUJO TÍPICO DE UNA RESERVA

1. **Registrar cliente** → POST `/api/clientes`
2. **Ver hoteles disponibles** → GET `/api/hoteles/`
3. **Ver habitaciones del hotel** → GET `/api/hoteles/{hotel_id}/habitaciones/disponibles`
4. **Crear paquete** → POST `/api/paquetes`
5. **Crear reserva** → POST `/api/reservas`
6. **Crear pago** → POST `/api/pagos`
7. **Confirmar reserva** → PUT `/api/reservas/{reserva_id}` (estado: confirmada)

---

**Última actualización:** 2026-06-05
