# AGENTS.md

## Proposito del proyecto

Este repositorio sirve para mantener un CV a partir de una fuente de datos editable en JSON.

La fuente de verdad es `cv.json`.

Los archivos generados son:

- `cv.tex`: version en LaTeX del CV.
- `cv.md`: version en Markdown plano del CV.

El script encargado de generar ambos archivos es `generate_cv.py`.

## Objetivo para la IA

Cuando un usuario converse con la IA sobre su CV, la IA debe:

1. Entender qué parte del CV quiere modificar el usuario.
2. Traducir esa solicitud a cambios concretos en `cv.json`.
3. Mantener la estructura del JSON valida y consistente.
4. Regenerar `cv.tex` y `cv.md` ejecutando `python3 generate_cv.py`.
5. Confirmar qué cambió y, si es posible, validar que no haya errores.

## Regla principal

Siempre editar `cv.json` primero.

No usar `cv.tex` ni `cv.md` como fuente de verdad. Esos archivos deben tratarse como salidas generadas. Solo deberian editarse manualmente si el usuario pide cambiar la plantilla o el formato de salida.

## Estructura esperada de `cv.json`

### `basics`

Informacion principal de contacto.

Campos:

- `name`
- `phone`
- `email`
- `github`
- `linkedin`

### `sections`

Titulos visibles de las secciones del CV en LaTeX.

Campos:

- `experience`
- `education`
- `skills`

### `experience`

Lista de experiencias laborales.

Cada item debe tener:

- `company`
- `period`
- `role`
- `schedule`
- `bullets`: lista de frases breves

### `education`

Lista de estudios o formacion.

Cada item debe tener:

- `institution`
- `period`
- `degree`
- `details`: lista de frases

### `skill_groups`

Lista de grupos de competencias.

Cada item debe tener:

- `title`
- `items`: lista de strings

## Como interpretar solicitudes del usuario

Mapeo sugerido:

- Si el usuario quiere cambiar nombre, telefono, correo o enlaces: editar `basics`.
- Si quiere renombrar secciones: editar `sections`.
- Si quiere agregar, quitar o reordenar trabajos: editar `experience`.
- Si quiere agregar cursos o estudios: editar `education`.
- Si quiere cambiar tecnologias, herramientas o idiomas: editar `skill_groups`.

## Criterios de edicion

- Mantener el JSON valido.
- No eliminar campos requeridos sin reemplazarlos.
- Conservar el estilo de redaccion del usuario cuando sea posible.
- Preferir frases claras, concretas y orientadas a CV.
- No inventar experiencia, estudios o habilidades que el usuario no haya indicado.

## Cuando pedir aclaracion

La IA debe pedir aclaracion solo si falta informacion esencial, por ejemplo:

- falta el nombre de una empresa o cargo
- no hay fechas para una experiencia nueva
- no queda claro en qué seccion debe ir un contenido

Si la intencion del usuario es clara, la IA debe hacer el cambio sin pedir confirmaciones innecesarias.

## Flujo recomendado de trabajo

1. Leer `cv.json`.
2. Identificar la seccion afectada.
3. Editar solo los campos necesarios en `cv.json`.
4. Ejecutar `python3 generate_cv.py`.
5. Verificar que `cv.tex` y `cv.md` no tengan errores obvios.
6. Informar al usuario qué se actualizo.

## Alcance

Este documento esta pensado para asistentes de IA que trabajen dentro del repositorio y ayuden al usuario a mantener su CV conversando en lenguaje natural.
