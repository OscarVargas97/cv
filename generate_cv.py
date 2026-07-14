#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


LATEX_TEMPLATE = r'''%-------------------------
% Resume in Latex
% Author : Harshibar
% Based off of: https://github.com/jakeryang/resume
% License : MIT
%------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
% only for pdflatex
% \input{glyphtounicode}

% fontawesome
\usepackage{fontawesome5}

% fixed width
\usepackage[scale=0.90,lf]{FiraMono}

% light-grey
\definecolor{light-grey}{gray}{0.83}
\definecolor{dark-grey}{gray}{0.3}
\definecolor{text-grey}{gray}{.08}

\DeclareRobustCommand{\ebseries}{\fontseries{eb}\selectfont}
\DeclareTextFontCommand{\texteb}{\ebseries}

% custom underilne
\usepackage{contour}
\usepackage[normalem]{ulem}
\renewcommand{\ULdepth}{1.8pt}
\contourlength{0.8pt}
\newcommand{\myuline}[1]{%
  \uline{\phantom{#1}}%
  \llap{\contour{white}{#1}}%
}


% custom font: helvetica-style
\usepackage{tgheros}
\renewcommand*\familydefault{\sfdefault}
%% Only if the base font of the document is to be sans serif
\usepackage[T1]{fontenc}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{0in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting - serif
% \titleformat{\section}{
%   \vspace{2pt} \scshape \raggedright\large % header section
% }{}{0em}{}[\color{black} \titlerule \vspace{-5pt}]

% TODO EBSERIES
% sans serif sections
\titleformat {\section}{
    \bfseries \vspace{2pt} \raggedright \large % header section
}{}{0em}{}[\color{light-grey} {\titlerule[2pt]} \vspace{-4pt}]

% only for pdflatex
% Ensure that generate pdf is machine readable/ATS parsable
% \pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-1pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & {\color{dark-grey}\small #2}\vspace{1pt}\\ % top row of resume entry
      \textit{#3} & {\color{dark-grey} \small #4}\\ % second row of resume entry
    \end{tabular*}\vspace{-4pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
      #1 & {\color{dark-grey}} \\
    \end{tabular*}\vspace{-4pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

% CHANGED default leftmargin  0.15 in
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{0pt}}

\color{text-grey}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\begin{document}

%----------HEADING----------
\begin{center}
        <<TEXTBF>>{\Huge <<NAME>>} \\ \vspace{5pt}
        \small \faPhone* \texttt{<<PHONE>>} \hspace{1pt} $|$
        \hspace{1pt} \faEnvelope \hspace{2pt} \texttt{<<EMAIL>>} \hspace{1pt} $|$
        \hspace{1pt} \faGithub \hspace{2pt} \texttt{<<GITHUB>>} \hspace{1pt} $|$
        \hspace{1pt} \faLinkedin \hspace{2pt}\texttt{<<LINKEDIN>>}
        \\ \vspace{-3pt}
\end{center}

%-----------EXPERIENCE-----------
\section{<<EXPERIENCE_TITLE>>}
  \resumeSubHeadingListStart

<<EXPERIENCE_ENTRIES>>
  \resumeSubHeadingListEnd

%-----------EDUCATION-----------
\section {<<EDUCATION_TITLE>>}
  \resumeSubHeadingListStart
<<EDUCATION_ENTRIES>>
  \resumeSubHeadingListEnd

%
%-----------PROGRAMMING SKILLS-----------
\section{<<SKILLS_TITLE>>}
 \begin{itemize}[leftmargin=0in, label={}]
    \small{\item{
<<SKILLS_BLOCK>>
    }}
 \end{itemize}
%-------------------------------------------
\end{document}
'''


LATEX_CHAR_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "á": r"\'a",
    "é": r"\'e",
    "í": r"\'i",
    "ó": r"\'o",
    "ú": r"\'u",
    "Á": r"\'A",
    "É": r"\'E",
    "Í": r"\'I",
    "Ó": r"\'O",
    "Ú": r"\'U",
    "ñ": r"\~n",
    "Ñ": r"\~N",
    "ü": r'\"u',
    "Ü": r'\"U'
}


def latex_escape(value: str) -> str:
    return "".join(LATEX_CHAR_MAP.get(char, char) for char in value)


def render_experience(entries: list[dict]) -> str:
    blocks = []
    for entry in entries:
        bullets = "\n".join(
            f"        \\resumeItem{{{latex_escape(item)}}}" for item in entry["bullets"]
        )
        block = (
            "    \\resumeSubheading\n"
            f"      {{{latex_escape(entry['company'])}}}{{{latex_escape(entry['period'])}}}\n"
            f"      {{{latex_escape(entry['role'])}}}{{{latex_escape(entry['schedule'])}}}\n"
            "      \\resumeItemListStart\n"
            f"{bullets}\n"
            "      \\resumeItemListEnd"
        )
        blocks.append(block)
    return "\n    \\vspace{-4pt}\n".join(blocks)


def render_education(entries: list[dict]) -> str:
    blocks = []
    for entry in entries:
        details = "\n".join(
            f"    \\resumeItem {{{latex_escape(item)}}}" for item in entry["details"]
        )
        block = (
            "    \\resumeSubheading\n"
            f"      {{{latex_escape(entry['institution'])}}}{{{latex_escape(entry['period'])}}}\n"
            f"      {{{latex_escape(entry['degree'])}}}{{}}\n"
            "      \\resumeItemListStart\n"
            f"{details}\n"
            "      \\resumeItemListEnd"
        )
        blocks.append(block)
    return "\n    \\vspace{-16pt}\n".join(blocks)


def flatten_items(raw_items: list[str]) -> list[str]:
    """Split multiline strings into individual items."""
    result = []
    for item in raw_items:
        for line in item.splitlines():
            stripped = line.strip()
            if stripped:
                result.append(stripped)
    return result


def render_skills(groups: list[dict]) -> str:
    lines = []
    last_index = len(groups) - 1
    for index, group in enumerate(groups):
        suffix = r"\vspace{2pt} \\" if index != last_index else ""
        flat = flatten_items(group["items"])
        items = ", ".join(latex_escape(item) for item in flat)
        lines.append(f"    \\textbf{{{latex_escape(group['title'])}}} {{: {items}}}{suffix}")
    return "\n".join(lines)


def generate_latex(data: dict) -> str:
    basics = data["basics"]
    sections = data["sections"]
    replacements = {
        "<<TEXTBF>>": r"\textbf",
        "<<NAME>>": latex_escape(basics["name"]),
        "<<PHONE>>": latex_escape(basics["phone"]),
        "<<EMAIL>>": latex_escape(basics["email"]),
        "<<GITHUB>>": latex_escape(basics["github"]),
        "<<LINKEDIN>>": latex_escape(basics["linkedin"]),
        "<<EXPERIENCE_TITLE>>": latex_escape(sections["experience"]),
        "<<EDUCATION_TITLE>>": latex_escape(sections["education"]),
        "<<SKILLS_TITLE>>": latex_escape(sections["skills"]),
        "<<EXPERIENCE_ENTRIES>>": render_experience(data["experience"]),
        "<<EDUCATION_ENTRIES>>": render_education(data["education"]),
        "<<SKILLS_BLOCK>>": render_skills(data["skill_groups"]),
    }
    output = LATEX_TEMPLATE
    for placeholder, value in replacements.items():
        output = output.replace(placeholder, value)
    return output


def generate_markdown(data: dict) -> str:
    basics = data["basics"]

    def normalize_schedule(value: str) -> str:
        return value.replace("Jornada ", "", 1).capitalize()

    lines = [
        f"# {basics['name']}",
        "",
        "## Contacto",
        "",
        f"- Telefono: {basics['phone']}",
        f"- Email: <mailto:{basics['email']}>",
        f"- GitHub: <https://{basics['github']}>",
        f"- LinkedIn: <https://{basics['linkedin']}>",
        "",
        "## Experiencia",
        "",
    ]

    for entry in data["experience"]:
        lines.extend([
            f"### {entry['company']}",
            "",
            f"- Periodo: {entry['period'].replace('--', '-').strip()}",
            f"- Cargo: {entry['role']}",
            f"- Jornada: {normalize_schedule(entry['schedule'])}",
        ])
        lines.extend(f"- {item}" for item in entry["bullets"])
        lines.append("")

    lines.extend([
        "## Educacion",
        "",
    ])

    for entry in data["education"]:
        lines.extend([
            f"### {entry['institution']}",
            "",
            f"- Periodo: {entry['period'].replace('--', '-').strip()}",
            f"- Grado: {entry['degree']}",
        ])
        lines.extend(f"- {item}" for item in entry["details"])
        lines.append("")

    lines.extend([
        "## Competencias Tecnicas",
        "",
    ])

    for group in data["skill_groups"]:
        lines.extend([
            f"### {group['title']}",
            "",
        ])
        lines.extend(f"- {item}" for item in flatten_items(group["items"]))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def load_data(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera cv.tex y cv.md a partir de cv.json")
    parser.add_argument("--input", default="cv.json", help="Ruta del archivo JSON fuente")
    parser.add_argument("--latex", default="cv.tex", help="Ruta de salida para el archivo LaTeX")
    parser.add_argument("--markdown", default="cv.md", help="Ruta de salida para el archivo Markdown")
    args = parser.parse_args()

    data = load_data(Path(args.input))
    write_text(Path(args.latex), generate_latex(data))
    write_text(Path(args.markdown), generate_markdown(data))


if __name__ == "__main__":
    main()