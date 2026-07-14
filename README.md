# CV Generator

Este proyecto contiene un script de Python para generar un CV en formato LaTeX y Markdown a partir de un archivo JSON editable.

## Archivos principales

- `cv.json`: fuente de datos editable del CV.
- `generate_cv.py`: script que convierte el JSON en archivos de salida.
- `cv.tex`: CV generado en LaTeX.
- `cv.md`: CV generado en Markdown plano.

## Como usarlo

1. Edita `cv.json` con tu informacion.
2. Ejecuta el script:

```bash
python3 generate_cv.py
```

1. El script regenerara:

- `cv.tex`
- `cv.md`

## Editor web

Tambien puedes editar `cv.json` desde un formulario web local.

1. Ejecuta:

```bash
python3 edit_cv_web.py
```

1. Abre en tu navegador:

```text
http://127.0.0.1:8000
```

1. Modifica los campos del formulario.
1. Guarda los cambios.

Al guardar, el editor actualiza `cv.json` y regenera automaticamente `cv.tex` y `cv.md`.

## Estructura de `cv.json`

El archivo `cv.json` esta dividido en bloques que representan las secciones del CV.

### `basics`

Contiene la informacion principal de contacto que aparece en el encabezado.

Campos:

- `name`: nombre completo.
- `phone`: telefono de contacto.
- `email`: correo electronico.
- `github`: usuario o URL visible de GitHub.
- `linkedin`: perfil o URL visible de LinkedIn.

Ejemplo:

```json
"basics": {
  "name": "Oscar Andres Vargas Zazzali",
  "phone": "+(56) 9 9335 8631",
  "email": "ovargaszazzali@gmail.com",
  "github": "github.com/OscarVargas97",
  "linkedin": "linkedin.com/in/oscarvargasz/"
}
```

### `sections`

Permite definir los nombres visibles de las secciones principales del CV generado en LaTeX.

Campos:

- `experience`: titulo de la seccion de experiencia.
- `education`: titulo de la seccion de educacion.
- `skills`: titulo de la seccion de competencias.

Ejemplo:

```json
"sections": {
  "experience": "EXPERIENCIA",
  "education": "EDUCACION",
  "skills": "COMPETENCIAS TECNICAS"
}
```

### `experience`

Es una lista de trabajos o experiencias laborales. Cada elemento del arreglo representa una experiencia.

Campos por item:

- `company`: nombre de la empresa.
- `period`: rango de fechas.
- `role`: cargo.
- `schedule`: tipo de jornada.
- `bullets`: lista de responsabilidades, logros o tareas.

Ejemplo:

```json
{
  "company": "RFLEX.IO",
  "period": "2024 -- Actualidad",
  "role": "Ingeniero de Software",
  "schedule": "Jornada completa",
  "bullets": [
    "Refactorizacion de codigo legado.",
    "Automatizacion de procesos manuales.",
    "Colaboracion con Producto y buenas practicas."
  ]
}
```

### `education`

Es una lista de estudios formales. Cada elemento representa una institucion o programa academico.

Campos por item:

- `institution`: nombre de la institucion.
- `period`: rango de fechas.
- `degree`: titulo o grado.
- `details`: lista de detalles adicionales, cursos o actividades relacionadas.

Ejemplo:

```json
{
  "institution": "Universidad Mayor, Santiago, Chile",
  "period": "2015 -- 2022",
  "degree": "Ingenieria Civil en Computacion e Informatica",
  "details": [
    "Formacion profesional en computacion.",
    "Curso realizado: Learning How to Learn.",
    "Curso realizado: Architecting with Google Compute Engine."
  ]
}
```

### `skill_groups`

Es una lista de grupos de competencias. Cada grupo tiene un titulo y una lista de elementos.

Campos por item:

- `title`: nombre del grupo.
- `items`: lista de tecnologias, herramientas o idiomas.

Ejemplo:

```json
{
  "title": "Tecnologias",
  "items": ["Docker", "Python", "PHP", "JavaScript"]
}
```

## Recomendaciones de edicion

- Mantén la misma estructura de llaves y arreglos.
- Usa comillas dobles validas en todo el JSON.
- Si agregas una experiencia o estudio nuevo, copia un bloque existente y modifica sus valores.
- `bullets`, `details` e `items` siempre deben ser listas.
- Si cambias los nombres de las secciones en `sections`, eso afectara el titulo visible del LaTeX.

## Flujo recomendado

1. Actualiza `cv.json`.
2. Ejecuta `python3 generate_cv.py`.
3. Revisa `cv.tex` si quieres generar PDF.
4. Revisa `cv.md` si quieres una version mas facil de procesar por LLMs o filtros automáticos.

## Objetivo

La salida en LaTeX permite generar un PDF con formato humano presentable. La salida en Markdown sirve como respaldo legible por sistemas automatizados, LLMs o filtros previos basados en texto.
