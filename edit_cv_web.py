#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from generate_cv import generate_latex, generate_markdown, write_text


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_lines(raw_items: list[str]) -> list[str]:
    values = []
    for item in raw_items:
        stripped = item.strip()
        if stripped:
            values.append(stripped)
    return values


def parse_form(payload: bytes, current_data: dict) -> dict:
    parsed = parse_qs(payload.decode("utf-8"), keep_blank_values=True)

    experience_count = int(parsed.get("experience_count", ["0"])[0] or "0")
    education_count = int(parsed.get("education_count", ["0"])[0] or "0")
    skill_group_count = int(parsed.get("skill_group_count", ["0"])[0] or "0")

    data = {
        "basics": {
            "name": parsed.get("basics.name", [""])[0].strip(),
            "phone": parsed.get("basics.phone", [""])[0].strip(),
            "email": parsed.get("basics.email", [""])[0].strip(),
            "github": parsed.get("basics.github", [""])[0].strip(),
            "linkedin": parsed.get("basics.linkedin", [""])[0].strip(),
        },
      "sections": current_data.get(
        "sections",
        {
          "experience": "EXPERIENCIA",
          "education": "EDUCACION",
          "skills": "COMPETENCIAS TECNICAS",
        },
      ),
        "experience": [],
        "education": [],
        "skill_groups": [],
    }

    for index in range(experience_count):
        company = parsed.get(f"experience.{index}.company", [""])[0].strip()
        period = parsed.get(f"experience.{index}.period", [""])[0].strip()
        role = parsed.get(f"experience.{index}.role", [""])[0].strip()
        schedule = parsed.get(f"experience.{index}.schedule", [""])[0].strip()
        bullets = normalize_lines(parsed.get(f"experience.{index}.bullets", [""]))
        if company or period or role or schedule or bullets:
            data["experience"].append(
                {
                    "company": company,
                    "period": period,
                    "role": role,
                    "schedule": schedule,
                    "bullets": bullets,
                }
            )

    for index in range(education_count):
        institution = parsed.get(f"education.{index}.institution", [""])[0].strip()
        period = parsed.get(f"education.{index}.period", [""])[0].strip()
        degree = parsed.get(f"education.{index}.degree", [""])[0].strip()
        details = normalize_lines(parsed.get(f"education.{index}.details", [""]))
        if institution or period or degree or details:
            data["education"].append(
                {
                    "institution": institution,
                    "period": period,
                    "degree": degree,
                    "details": details,
                }
            )

    for index in range(skill_group_count):
        title = parsed.get(f"skill_groups.{index}.title", [""])[0].strip()
        items = normalize_lines(parsed.get(f"skill_groups.{index}.items", [""]))
        if title or items:
            data["skill_groups"].append({"title": title, "items": items})

    return data


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def input_row(label: str, name: str, value: str, placeholder: str = "") -> str:
    return (
        "<label class=\"field\">"
        f"<span>{escape(label)}</span>"
        f"<input name=\"{escape(name)}\" value=\"{escape(value)}\" placeholder=\"{escape(placeholder)}\">"
        "</label>"
    )


def textarea_row(label: str, name: str, values: list[str], placeholder: str = "") -> str:
    text = "\n".join(values)
    return (
        "<label class=\"field\">"
        f"<span>{escape(label)}</span>"
        f"<textarea name=\"{escape(name)}\" placeholder=\"{escape(placeholder)}\">{escape(text)}</textarea>"
        "</label>"
    )


def render_experience_cards(entries: list[dict]) -> str:
    cards = []
    for index, entry in enumerate(entries):
        cards.append(
            "<article class=\"card repeat-item\" data-kind=\"experience\">"
            "<div class=\"card-actions\"><button type=\"button\" class=\"ghost\" onclick=\"removeItem(this)\">Quitar</button></div>"
            f"{input_row('Empresa', f'experience.{index}.company', entry.get('company', ''))}"
            f"{input_row('Periodo', f'experience.{index}.period', entry.get('period', ''), '2024 -- Actualidad')}"
            f"{input_row('Cargo', f'experience.{index}.role', entry.get('role', ''))}"
            f"{input_row('Jornada', f'experience.{index}.schedule', entry.get('schedule', ''), 'Jornada completa')}"
            f"{textarea_row('Bullets, una linea por item', f'experience.{index}.bullets', entry.get('bullets', []))}"
            "</article>"
        )
    return "".join(cards)


def render_education_cards(entries: list[dict]) -> str:
    cards = []
    for index, entry in enumerate(entries):
        cards.append(
            "<article class=\"card repeat-item\" data-kind=\"education\">"
            "<div class=\"card-actions\"><button type=\"button\" class=\"ghost\" onclick=\"removeItem(this)\">Quitar</button></div>"
            f"{input_row('Institucion', f'education.{index}.institution', entry.get('institution', ''))}"
            f"{input_row('Periodo', f'education.{index}.period', entry.get('period', ''))}"
            f"{input_row('Grado o titulo', f'education.{index}.degree', entry.get('degree', ''))}"
            f"{textarea_row('Detalles, una linea por item', f'education.{index}.details', entry.get('details', []))}"
            "</article>"
        )
    return "".join(cards)


def render_skill_cards(groups: list[dict]) -> str:
    cards = []
    for index, group in enumerate(groups):
        cards.append(
            "<article class=\"card repeat-item\" data-kind=\"skill_groups\">"
            "<div class=\"card-actions\"><button type=\"button\" class=\"ghost\" onclick=\"removeItem(this)\">Quitar</button></div>"
            f"{input_row('Titulo del grupo', f'skill_groups.{index}.title', group.get('title', ''))}"
            f"{textarea_row('Items, una linea por item', f'skill_groups.{index}.items', group.get('items', []))}"
            "</article>"
        )
    return "".join(cards)


def render_page(data: dict, message: str = "") -> str:
    basics = data["basics"]
    notice = f"<p class=\"notice\">{escape(message)}</p>" if message else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Editor de CV</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4efe7;
      --panel: #fffdf9;
      --line: #d9cfc2;
      --text: #1e1d1a;
      --muted: #6f665c;
      --accent: #0f766e;
      --accent-soft: #d8f3ef;
      --danger: #9f1239;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Georgia, "Nimbus Roman", serif; background: linear-gradient(180deg, #f7f2eb 0%, #eee6da 100%); color: var(--text); }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 64px; }}
    h1, h2, h3 {{ margin: 0 0 12px; }}
    p {{ color: var(--muted); }}
    form {{ display: grid; gap: 24px; }}
    .panel {{ background: rgba(255, 253, 249, 0.94); border: 1px solid var(--line); border-radius: 18px; padding: 20px; box-shadow: 0 12px 30px rgba(30, 29, 26, 0.08); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; }}
    .field {{ display: grid; gap: 6px; margin-bottom: 14px; }}
    .field span {{ font-size: 0.92rem; color: var(--muted); }}
    input, textarea {{ width: 100%; border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; font: inherit; background: #fff; color: var(--text); }}
    textarea {{ min-height: 120px; resize: vertical; }}
    .repeat-list {{ display: grid; gap: 16px; }}
    .card {{ border: 1px solid var(--line); border-radius: 16px; padding: 16px; background: #fffefa; }}
    .card-actions {{ display: flex; justify-content: flex-end; margin-bottom: 12px; }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }}
    button {{ border: 0; border-radius: 999px; padding: 11px 16px; font: inherit; cursor: pointer; }}
    .primary {{ background: var(--accent); color: white; }}
    .secondary {{ background: var(--accent-soft); color: var(--accent); }}
    .ghost {{ background: transparent; color: var(--danger); border: 1px solid rgba(159, 18, 57, 0.28); }}
    .notice {{ background: var(--accent-soft); color: var(--accent); border: 1px solid rgba(15, 118, 110, 0.18); padding: 12px 14px; border-radius: 12px; }}
    .help {{ font-size: 0.95rem; color: var(--muted); margin-top: 8px; }}
  </style>
</head>
<body>
  <main>
    <header class="panel">
      <h1>Editor web de CV</h1>
      <p>Modifica <strong>cv.json</strong> desde este formulario. Al guardar, el script actualiza el JSON y regenera <strong>cv.tex</strong> y <strong>cv.md</strong>.</p>
      {notice}
    </header>

    <form method="post" action="/save">
      <section class="panel">
        <h2>Datos basicos</h2>
        <div class="grid">
          {input_row('Nombre completo', 'basics.name', basics.get('name', ''))}
          {input_row('Telefono', 'basics.phone', basics.get('phone', ''))}
          {input_row('Email', 'basics.email', basics.get('email', ''))}
          {input_row('GitHub', 'basics.github', basics.get('github', ''))}
          {input_row('LinkedIn', 'basics.linkedin', basics.get('linkedin', ''))}
        </div>
      </section>

      <section class="panel">
        <div class="actions">
          <h2>Experiencia</h2>
          <button type="button" class="secondary" onclick="addItem('experience')">Agregar experiencia</button>
        </div>
        <p class="help">Cada bullet va en una linea separada.</p>
        <input type="hidden" id="experience_count" name="experience_count" value="{len(data['experience'])}">
        <div id="experience_list" class="repeat-list">{render_experience_cards(data['experience'])}</div>
      </section>

      <section class="panel">
        <div class="actions">
          <h2>Educacion</h2>
          <button type="button" class="secondary" onclick="addItem('education')">Agregar educacion</button>
        </div>
        <p class="help">Usa detalles para cursos, enfoque o actividades relevantes.</p>
        <input type="hidden" id="education_count" name="education_count" value="{len(data['education'])}">
        <div id="education_list" class="repeat-list">{render_education_cards(data['education'])}</div>
      </section>

      <section class="panel">
        <div class="actions">
          <h2>Competencias</h2>
          <button type="button" class="secondary" onclick="addItem('skill_groups')">Agregar grupo</button>
        </div>
        <p class="help">Cada item debe ir en una linea separada. Ejemplos: tecnologias, herramientas, idiomas.</p>
        <input type="hidden" id="skill_group_count" name="skill_group_count" value="{len(data['skill_groups'])}">
        <div id="skill_groups_list" class="repeat-list">{render_skill_cards(data['skill_groups'])}</div>
      </section>

      <section class="panel actions">
        <button class="primary" type="submit">Guardar cambios y regenerar</button>
      </section>
    </form>
  </main>

  <template id="experience_template">
    <article class="card repeat-item" data-kind="experience">
      <div class="card-actions"><button type="button" class="ghost" onclick="removeItem(this)">Quitar</button></div>
      <label class="field"><span>Empresa</span><input data-field="company"></label>
      <label class="field"><span>Periodo</span><input data-field="period" placeholder="2024 -- Actualidad"></label>
      <label class="field"><span>Cargo</span><input data-field="role"></label>
      <label class="field"><span>Jornada</span><input data-field="schedule" placeholder="Jornada completa"></label>
      <label class="field"><span>Bullets, una linea por item</span><textarea data-field="bullets"></textarea></label>
    </article>
  </template>

  <template id="education_template">
    <article class="card repeat-item" data-kind="education">
      <div class="card-actions"><button type="button" class="ghost" onclick="removeItem(this)">Quitar</button></div>
      <label class="field"><span>Institucion</span><input data-field="institution"></label>
      <label class="field"><span>Periodo</span><input data-field="period"></label>
      <label class="field"><span>Grado o titulo</span><input data-field="degree"></label>
      <label class="field"><span>Detalles, una linea por item</span><textarea data-field="details"></textarea></label>
    </article>
  </template>

  <template id="skill_groups_template">
    <article class="card repeat-item" data-kind="skill_groups">
      <div class="card-actions"><button type="button" class="ghost" onclick="removeItem(this)">Quitar</button></div>
      <label class="field"><span>Titulo del grupo</span><input data-field="title"></label>
      <label class="field"><span>Items, una linea por item</span><textarea data-field="items"></textarea></label>
    </article>
  </template>

  <script>
    const collectionConfig = {{
      experience: ['company', 'period', 'role', 'schedule', 'bullets'],
      education: ['institution', 'period', 'degree', 'details'],
      skill_groups: ['title', 'items']
    }};

    function setNames(kind) {{
      const items = document.querySelectorAll(`#${{kind}}_list .repeat-item`);
      items.forEach((item, index) => {{
        item.querySelectorAll('[data-field]').forEach((field) => {{
          field.name = `${{kind}}.${{index}}.${{field.dataset.field}}`;
        }});
      }});
      const countField = document.getElementById(`${{kind === 'skill_groups' ? 'skill_group' : kind}}_count`);
      countField.value = items.length;
    }}

    function addItem(kind) {{
      const template = document.getElementById(`${{kind}}_template`);
      const list = document.getElementById(`${{kind}}_list`);
      const fragment = template.content.cloneNode(true);
      list.appendChild(fragment);
      setNames(kind);
    }}

    function removeItem(button) {{
      const item = button.closest('.repeat-item');
      const kind = item.dataset.kind;
      item.remove();
      setNames(kind);
    }}

    setNames('experience');
    setNames('education');
    setNames('skill_groups');
  </script>
</body>
</html>
"""


class CVEditorHandler(BaseHTTPRequestHandler):
    json_path: Path
    latex_path: Path
    markdown_path: Path

    def do_HEAD(self) -> None:
        query = parse_qs(urlparse(self.path).query)
        message = query.get("message", [""])[0]
        self.respond_html(render_page(load_json(self.json_path), message), include_body=False)

    def do_GET(self) -> None:
        query = parse_qs(urlparse(self.path).query)
        message = query.get("message", [""])[0]
        self.respond_html(render_page(load_json(self.json_path), message))

    def do_POST(self) -> None:
        if self.path != "/save":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length)
        current_data = load_json(self.json_path)
        data = parse_form(payload, current_data)

        write_json(self.json_path, data)
        write_text(self.latex_path, generate_latex(data))
        write_text(self.markdown_path, generate_markdown(data))

        self.send_response(303)
        self.send_header("Location", "/?message=Cambios+guardados+y+archivos+regenerados")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        return

    def respond_html(self, body: str, include_body: bool = True) -> None:
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        if include_body:
            self.wfile.write(encoded)


def main() -> None:
    parser = argparse.ArgumentParser(description="Levanta un editor web para cv.json")
    parser.add_argument("--host", default="127.0.0.1", help="Host donde escuchar")
    parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor web")
    parser.add_argument("--input", default="cv.json", help="Ruta del archivo JSON fuente")
    parser.add_argument("--latex", default="cv.tex", help="Ruta de salida para el archivo LaTeX")
    parser.add_argument("--markdown", default="cv.md", help="Ruta de salida para el archivo Markdown")
    args = parser.parse_args()

    handler = type(
        "ConfiguredCVEditorHandler",
        (CVEditorHandler,),
        {
            "json_path": Path(args.input),
            "latex_path": Path(args.latex),
            "markdown_path": Path(args.markdown),
        },
    )

    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Editor disponible en http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()