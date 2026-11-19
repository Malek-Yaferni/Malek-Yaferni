"""Generate the GitHub profile sheet and link buttons.


GitHub strips README CSS, so the brown / ivory system lives in SVG.

Run: python generate.py

"""



from __future__ import annotations


import math

from pathlib import Path


W = 1040

FONT = "Segoe UI, Helvetica, Arial, sans-serif"


ESPRESSO = "#241A16"

MOCHA = "#49352A"

CHOCOLATE = "#795C46"

GOLD = "#C5A77D"

CARAMEL = "#B8875A"

IVORY = "#F3EBDD"

CREAM = "#FAF6EF"

BEIGE = "#D8C6AC"


OUT = Path(__file__).resolve().parent / "assets"

issues: list[str] = []


def esc(value: str) -> str:

    return (

        value.replace("&", "&amp;")

        .replace("<", "&lt;")

        .replace(">", "&gt;")

    )


def est_width(text: str, size: float, weight: int, spacing: float) -> float:

    factor = 0.56 if weight >= 650 else 0.52

    return len(text) * size * factor + max(len(text) - 1, 0) * spacing


class Page:

    def __init__(self) -> None:

        self.els: list[str] = []

        self.y = 0.0


    def add(self, element: str) -> None:

        self.els.append(element)


    def rect(

        self,

        x: float,

        y: float,

        w: float,

        h: float,

        rx: float,

        fill: str,

        stroke: str | None = None,

        sw: float = 1,

        opacity: float = 1,

    ) -> None:

        stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""

        opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""

        self.add(

            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '

            f'rx="{rx:.1f}" fill="{fill}"{stroke_attr}{opacity_attr}/>'

        )


    def line(

        self,

        x1: float,

        y1: float,

        x2: float,

        y2: float,

        stroke: str,

        sw: float = 1,

        opacity: float = 1,

        dash: str | None = None,

    ) -> None:

        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""

        opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""

        self.add(

            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '

            f'stroke="{stroke}" stroke-width="{sw}"{dash_attr}{opacity_attr}/>'

        )


    def circle(

        self,

        cx: float,

        cy: float,

        r: float,

        fill: str = "none",

        stroke: str | None = None,

        sw: float = 1,

        opacity: float = 1,

        dash: str | None = None,

    ) -> None:

        stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""

        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""

        opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""

        self.add(

            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"'

            f'{stroke_attr}{dash_attr}{opacity_attr}/>'

        )


    def text(

        self,

        x: float,

        y: float,

        value: str,

        size: float,

        fill: str,

        weight: int = 500,

        anchor: str = "start",

        spacing: float = 0,

        opacity: float = 1,

        max_right: float = W - 28,

        min_left: float = 28,

    ) -> None:

        width = est_width(value, size, weight, spacing)

        if anchor == "middle":

            left, right = x - width / 2, x + width / 2

        elif anchor == "end":

            left, right = x - width, x

        else:

            left, right = x, x + width

        if left < min_left - 1 or right > max_right + 1:

            issues.append(

                f'overflow "{value}" y={y:.0f} span={left:.0f}..{right:.0f}'

            )

        spacing_attr = f' letter-spacing="{spacing}"' if spacing else ""

        opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""

        self.add(

            f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-family="{FONT}" '

            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"'

            f'{spacing_attr}{opacity_attr}>{esc(value)}</text>'

        )


    def header(self, number: str, title: str, dek: str) -> None:

        y = self.y

        self.rect(36, y, 2, 48, 0, CARAMEL)

        self.text(54, y + 16, number, 14, CHOCOLATE, 700, spacing=3.2)

        self.text(54, y + 52, title, 36, ESPRESSO, 700)

        title_w = est_width(title, 36, 700, 0)

        rule_x = 54 + title_w + 22

        if rule_x < 1000:

            self.line(rule_x, y + 44, 1004, y + 44, BEIGE, 1)

        self.text(54, y + 80, dek, 16, MOCHA)

        self.y = y + 112


    def finish(self) -> str:

        height = math.ceil(self.y)

        body = "\n".join(self.els)

        return (

            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '

            f'viewBox="0 0 {W} {height}" fill="none" role="img">\n'

            f"<title>Malek Yaferni — Industrial Computer Engineering, AI and Data Science</title>\n"

            f"{body}\n</svg>\n"

        )


def corner(page: Page, x: float, y: float, corner_name: str, color: str = GOLD) -> None:

    arm = 16

    if corner_name == "tl":

        page.line(x, y, x + arm, y, color, 1)

        page.line(x, y, x, y + arm, color, 1)

    elif corner_name == "tr":

        page.line(x - arm, y, x, y, color, 1)

        page.line(x, y, x, y + arm, color, 1)

    elif corner_name == "bl":

        page.line(x, y, x + arm, y, color, 1)

        page.line(x, y - arm, x, y, color, 1)

    else:

        page.line(x - arm, y, x, y, color, 1)

        page.line(x, y - arm, x, y, color, 1)


def hero(page: Page) -> None:

    x, y, w, h = 28, 24, 984, 468

    page.rect(x, y, w, h, 30, ESPRESSO)

    page.rect(x + 10, y + 10, w - 20, h - 20, 22, "none", CHOCOLATE, 1, 0.55)


    for cx in range(760, 980, 20):

        for cy in range(70, 450, 20):

            page.circle(cx, cy, 0.8, GOLD, opacity=0.28)


    corner(page, x + 26, y + 26, "tl")

    corner(page, x + w - 26, y + 26, "tr")

    corner(page, x + 26, y + h - 26, "bl")

    corner(page, x + w - 26, y + h - 26, "br")


    page.text(64, 92, "INDUSTRIAL COMPUTER ENGINEERING", 13, GOLD, 700, spacing=2.6)

    page.text(64, 168, "Malek Yaferni", 64, IVORY, 700)

    page.line(64, 196, 214, 196, GOLD, 1.25)

    page.text(64, 238, "Energy Systems Supervision", 22, GOLD, 600)

    page.text(64, 274, "Artificial Intelligence   ·   Data Science", 16, IVORY, 500)

    page.text(

        64,

        328,

        "Building intelligent solutions, one project at a time.",

        16,

        BEIGE,

    )


    facts = [("ENET'Com, Sfax", 64), ("Final year", 250), ("Open to PFE", 390)]

    for label, fx in facts:

        page.circle(fx, 392, 3, CARAMEL)

        page.text(fx + 14, 397, label, 15, IVORY, 600)


    cx, cy = 824, 258

    nodes = [

        ("Agents", -90),

        ("RAG", -30),

        ("Vision", 30),

        ("Data", 90),

        ("Infra", 150),

        ("AgriMent", 210),

    ]

    orbit = 124

    page.circle(cx, cy, orbit, "none", GOLD, 1, 0.45)

    page.circle(cx, cy, 78, "none", GOLD, 1, 0.28)

    page.circle(cx, cy, 52, ESPRESSO, GOLD, 1.25)

    page.circle(cx, cy, 58, "none", GOLD, 1, 0.7, dash="1.5 4")


    points = []

    for label, deg in nodes:

        rad = math.radians(deg)

        points.append((cx + orbit * math.cos(rad), cy + orbit * math.sin(rad), label, deg))


    for index, (px, py, _label, _deg) in enumerate(points):

        nxt = points[(index + 1) % len(points)]

        page.line(px, py, nxt[0], nxt[1], GOLD, 1, 0.4)

        page.line(cx, cy, px, py, GOLD, 1, 0.75)


    page.text(cx, cy + 6, "MY", 18, IVORY, 700, anchor="middle", spacing=2)


    for px, py, label, deg in points:

        page.circle(px, py, 4.5, GOLD)

        lx = cx + 162 * math.cos(math.radians(deg))

        ly = cy + 162 * math.sin(math.radians(deg)) + 4

        deg_n = deg % 360

        if deg_n < 45 or deg_n > 315:

            anchor = "start"

        elif 135 < deg_n < 225:

            anchor = "end"

        else:

            anchor = "middle"

        page.text(lx, ly, label, 13, IVORY, 600, anchor=anchor, spacing=0.4)


    page.y = y + h + 56


def about(page: Page) -> None:

    page.header(

        "01",

        "About",

        "Final-year engineering, aimed at systems people can actually use.",

    )

    y = page.y

    left_w, right_w, gap, h = 600, 350, 18, 458

    page.rect(36, y, left_w, h, 20, CREAM, BEIGE, 1)

    page.rect(36 + left_w + gap, y, right_w, h, 20, ESPRESSO)


    page.text(64, y + 40, "PROFILE", 13, CHOCOLATE, 700, spacing=2.8)

    page.text(64, y + 78, "Hello, I'm Malek", 28, ESPRESSO, 700)

    lines = [

        (y + 122, "Final-year Industrial Computer Engineering student"),

        (y + 148, "at ENET'Com, Sfax, specializing in Energy Systems"),

        (y + 174, "Supervision."),

        (y + 216, "I turn operational problems into intelligent systems:"),

        (y + 242, "agents, retrieval, computer vision, and the data"),

        (y + 268, "pipelines underneath them."),

    ]

    for ly, line in lines:

        page.text(64, ly, line, 16, MOCHA)


    page.text(64, y + 312, "FOCUS", 13, CHOCOLATE, 700, spacing=2.8)

    focus = [

        (64, "Generative AI and LLMs"),

        (64, "AI agents and multi-agent systems"),

        (64, "Machine learning and deep learning"),

        (330, "Retrieval-augmented generation"),

        (330, "Computer vision"),

        (330, "Data engineering and analysis"),

    ]

    for index, (fx, label) in enumerate(focus):

        col = index if index < 3 else index - 3

        fy = y + 346 + col * 30

        page.rect(fx, fy - 10, 6, 6, 1, CARAMEL)

        page.text(fx + 16, fy, label, 15, ESPRESSO, 600)


    rx = 36 + left_w + gap

    page.text(rx + 28, y + 40, "APPROACH", 13, GOLD, 700, spacing=2.8)

    page.text(rx + 28, y + 78, "How I build", 28, IVORY, 700)

    steps = [

        ("01", "Frame the decision", "The operational question comes first."),

        ("02", "Compose the system", "Specialized agents, one orchestration."),

        ("03", "Ground the answer", "Retrieval, evidence, and a human check."),

        ("04", "Measure", "Precision, correlation, and mAP."),

    ]

    for index, (num, title, detail) in enumerate(steps):

        sy = y + 124 + index * 70

        page.text(rx + 28, sy, num, 13, GOLD, 700, spacing=1.2)

        page.text(rx + 68, sy, title, 16, IVORY, 700)

        page.text(rx + 68, sy + 24, detail, 14, BEIGE)

    page.line(rx + 28, y + h - 58, rx + right_w - 28, y + h - 58, CHOCOLATE, 1)

    page.text(rx + 28, y + h - 30, "Open to a graduation internship", 14, GOLD, 600)


    strip_y = y + h + 16

    page.rect(36, strip_y, 968, 58, 16, CREAM, BEIGE, 1)

    meta = [

        (64, "ENET'Com"),

        (230, "Sfax, Tunisia"),

        (430, "Final year"),

        (600, "AI and software"),

        (800, "PFE"),

    ]

    for mx, label in meta:

        page.circle(mx, strip_y + 29, 3, CARAMEL)

        page.text(mx + 12, strip_y + 34, label, 14, ESPRESSO, 600)

    page.y = strip_y + 58 + 52


def stack(page: Page) -> None:

    page.header(

        "02",

        "Technical Stack",

        "Tools I use to design, train, orchestrate, and ship.",

    )

    groups = [

        (

            "Languages",

            "Programming",

            [("Python", "Java"), ("C", "JavaScript"), ("C++", "SQL")],

        ),

        (

            "Machine intelligence",

            "AI, learning, vision",

            [("TensorFlow", "OpenCV"), ("PyTorch", "YOLOv9"), ("Keras", ""), ("Scikit-learn", "")],

        ),

        (

            "Generative and agentic",

            "Orchestration and retrieval",

            [("LangChain", "Groq"), ("LangGraph", "Mistral"), ("ChromaDB", "MCP"), ("Qdrant", "n8n")],

        ),

        (

            "Systems",

            "Backend, data, tools",

            [("FastAPI", "MongoDB"), ("Streamlit", "Git"), ("PostgreSQL", "Linux"), ("MySQL", "GitHub")],

        ),

    ]

    y = page.y

    card_w, card_h, gap = 475, 272, 18

    for index, (title, eyebrow, rows) in enumerate(groups):

        col = index % 2

        row = index // 2

        x = 36 + col * (card_w + gap)

        cy = y + row * (card_h + gap)

        page.rect(x, cy, card_w, card_h, 18, CREAM, BEIGE, 1)

        page.text(x + 28, cy + 36, eyebrow.upper(), 12, CHOCOLATE, 700, spacing=2.2)

        page.text(x + 28, cy + 70, title, 24, ESPRESSO, 700)

        page.line(x + 28, cy + 88, x + card_w - 28, cy + 88, BEIGE, 1)

        for r_index, (left, right) in enumerate(rows):

            ry = cy + 122 + r_index * 32

            page.rect(x + 28, ry - 9, 5, 5, 1, CARAMEL)

            page.text(x + 44, ry, left, 16, MOCHA, 600)

            if right:

                page.rect(x + 250, ry - 9, 5, 5, 1, CARAMEL)

                page.text(x + 266, ry, right, 16, MOCHA, 600)

    page.y = y + 2 * card_h + gap + 52


def project_card(

    page: Page,

    x: float,

    y: float,

    w: float,

    h: float,

    number: str,

    category: str,

    title: str,

    subtitle: str,

    body: tuple[str, str],

    metric: str,

    stack_line: str,

) -> None:

    page.rect(x, y, w, h, 18, CREAM, BEIGE, 1)

    page.rect(x + 24, y + 28, 2, 16, 0, CARAMEL)

    page.text(x + 36, y + 41, number, 13, CHOCOLATE, 700, spacing=1.4)

    page.text(x + 78, y + 41, category, 12, CHOCOLATE, 700, spacing=1.8)

    page.text(x + 24, y + 82, title, 24, ESPRESSO, 700)

    page.text(x + 24, y + 112, subtitle, 15, MOCHA)

    page.text(x + 24, y + 156, body[0], 15, MOCHA)

    page.text(x + 24, y + 178, body[1], 15, MOCHA)

    if metric:

        page.text(x + 24, y + 220, metric, 14, CHOCOLATE, 700)

    page.line(x + 24, y + h - 58, x + w - 24, y + h - 58, BEIGE, 1)

    page.text(x + 24, y + h - 30, stack_line, 13, MOCHA, 600)


def projects(page: Page) -> None:

    page.header(

        "03",

        "Featured Projects",

        "Selected systems across agents, vision, retrieval, and infrastructure.",

    )

    cards = [

        (

            "01",

            "GENERATIVE AI",

            "AgriMent",

            "Agricultural decision-support",

            (

                "Six decoupled agents, orchestrated with LangGraph.",

                "Hybrid RAG, with a human in the loop.",

            ),

            "0.941 context precision   ·   0.98 Pearson",

            "LangGraph  ·  FastAPI  ·  Mistral  ·  ChromaDB  ·  Qdrant",

        ),

        (

            "02",

            "DEEP LEARNING",

            "Facial Emotion Recognition",

            "Architecture comparison",

            (

                "ResNet50 and VGG16 under transfer learning.",

                "Training, evaluation, and a Streamlit interface.",

            ),

            "Compared models, then served the prediction.",

            "Python  ·  TensorFlow  ·  Keras  ·  Streamlit",

        ),

        (

            "03",

            "COMPUTER VISION",

            "PPE Detection",

            "Safety equipment, in real time",

            (

                "Custom dataset of 23,000+ images.",

                "YOLOv9 detection with GPU inference.",

            ),

            "87% mAP",

            "Python  ·  YOLOv9  ·  PyTorch  ·  Streamlit",

        ),

        (

            "04",

            "RETRIEVAL",

            "AI Job Matching",

            "CV profiles to relevant roles",

            (

                "PDF extraction into LLM-structured profiles.",

                "Semantic retrieval and personal recommendations.",

            ),

            "",

            "FastAPI  ·  ChromaDB  ·  Llama 3.3  ·  Groq  ·  PyMuPDF",

        ),

        (

            "05",

            "SECURITY",

            "Cybersecurity AI Analyst",

            "Network threat investigation",

            (

                "CIC-IDS2017 with Isolation Forest anomalies.",

                "MCP tools, tool calling, evidence-based reports.",

            ),

            "",

            "Python  ·  Pandas  ·  Isolation Forest  ·  MCP  ·  RAG",

        ),
        
        (
            "06",
            "INFORMATION RETRIEVAL",
            "Scientific Literature Search",
            "Semantic search over 5,183 scientific abstracts",
            (
                "Compared dense, BM25, and hybrid RRF retrieval.",
                "Benchmarked MiniLM, BGE-small, and E5-small.",
            ),
            "BGE-small: nDCG@10 0.746 vs BM25 0.647 (+15%)",
            "Python  ·  Sentence Transformers  ·  FAISS  ·  BM25  ·  Streamlit",
        ),


        (

            "07",

            "INFRASTRUCTURE",

            "Tunisia Telecom",

            "Highly available directory services",

            (

                "Active Directory for enterprise operations.",

                "DNS, Group Policy, Hyper-V, and PowerShell.",

            ),

            "",

            "Windows Server  ·  Active Directory  ·  Hyper-V",

        ),
        

    ]

    y = page.y

    card_w, card_h, gap = 475, 300, 18

    for index, card in enumerate(cards):

        col = index % 2

        row = index // 2

        x = 36 + col * (card_w + gap)

        cy = y + row * (card_h + gap)

        project_card(page, x, cy, card_w, card_h, *card)

    rows = math.ceil(len(cards) / 2)
    page.y = y + rows * card_h + (rows - 1) * gap + 52


def experience(page: Page) -> None:

    page.header(

        "04",

        "Experience",

        "Engineering internships, from intelligent systems to infrastructure.",

    )

    y = page.y

    card_w, card_h, gap = 475, 248, 18

    roles = [

        (

            "ENGINEERING INTERNSHIP",

            "Talan Tunisie Consulting",

            "July 2026  —  August 2026",

            (

                "Contributed to AgriMent during SummerCamp 2026.",

                "Multi-agent and RAG workflows, in a mixed team.",

            ),

            "Second place   ·   10 teams   ·   120+ participants",

        ),

        (

            "ENGINEERING INTERNSHIP",

            "Tunisia Telecom",

            "July 2025  —  August 2025",

            (

                "Highly available Active Directory infrastructure.",

                "DNS, Group Policy, Hyper-V, and PowerShell.",

            ),

            "Enterprise directory, virtualization, automation",

        ),

    ]

    for index, (eyebrow, title, date, body, foot) in enumerate(roles):

        x = 36 + index * (card_w + gap)

        page.rect(x, y, card_w, card_h, 18, CREAM, BEIGE, 1)

        page.rect(x, y, 4, card_h, 2, CARAMEL)

        page.text(x + 28, y + 40, eyebrow, 12, CHOCOLATE, 700, spacing=2)

        page.text(x + 28, y + 78, title, 22, ESPRESSO, 700)

        page.text(x + 28, y + 108, date, 14, CHOCOLATE, 600)

        page.text(x + 28, y + 150, body[0], 15, MOCHA)

        page.text(x + 28, y + 174, body[1], 15, MOCHA)

        page.text(x + 28, y + 214, foot, 14, ESPRESSO, 700)

    page.y = y + card_h + 52


def education(page: Page) -> None:

    page.header(

        "05",

        "Education",

        "Study, certifications, and the student communities I help run.",

    )

    y = page.y

    card_w, gap, h = 310, 19, 292

    blocks = [

        (

            "STUDY",

            "ENET'Com",

            [

                "Sfax, Tunisia",

                "Industrial Computer Engineering",

                "Energy Systems Supervision",

                "Final year",

            ],

        ),

        (

            "CERTIFICATIONS",

            "Oracle",

            [

                "Agentic AI Foundations",

                "October 2026",

                "OCI 2025 AI Foundations",

                "Associate  ·  October 2025",

            ],

        ),

        (

            "LEADERSHIP",

            "IEEE",

            [

                "CASS ENET'Com  ·  Webmaster",

                "January 2025 — January 2026",

                "Tunisia Section  ·  TSYP 12",

                "Organizing committee  ·  Dec 2024",

            ],

        ),

    ]

    for index, (eyebrow, title, lines) in enumerate(blocks):

        x = 36 + index * (card_w + gap)

        page.rect(x, y, card_w, h, 18, CREAM, BEIGE, 1)

        page.text(x + 24, y + 40, eyebrow, 12, CHOCOLATE, 700, spacing=2)

        page.text(x + 24, y + 78, title, 26, ESPRESSO, 700)

        page.line(x + 24, y + 98, x + card_w - 24, y + 98, BEIGE, 1)

        for line_index, line in enumerate(lines):

            page.text(x + 24, y + 136 + line_index * 32, line, 15, MOCHA, 600)

    page.y = y + h + 52


def contact(page: Page) -> None:

    page.header(

        "06",

        "Contact",

        "A final-year internship, a collaboration, or a technical conversation.",

    )

    y = page.y

    page.rect(28, y, 984, 210, 28, ESPRESSO)

    corner(page, 54, y + 28, "tl")

    corner(page, 986, y + 28, "tr")

    corner(page, 54, y + 182, "bl")

    corner(page, 986, y + 182, "br")

    page.text(64, y + 64, "LET'S CONNECT", 13, GOLD, 700, spacing=2.8)

    page.text(64, y + 108, "Intelligent systems, built with care.", 28, IVORY, 700)

    page.text(

        64,

        y + 148,

        "malekyaferni@gmail.com",

        16,

        GOLD,

        600,

    )

    page.text(64, y + 176, "Sfax, Tunisia", 14, BEIGE)


    cx, cy = 900, y + 108

    page.circle(cx, cy, 46, "none", GOLD, 1, 0.45)

    page.circle(cx, cy, 28, ESPRESSO, GOLD, 1.15)

    page.text(cx, cy + 5, "MY", 14, IVORY, 700, anchor="middle", spacing=1.5)

    for deg in (-90, -30, 30, 90, 150, 210):

        rad = math.radians(deg)

        page.circle(cx + 46 * math.cos(rad), cy + 46 * math.sin(rad), 3, GOLD)

        page.line(

            cx,

            cy,

            cx + 46 * math.cos(rad),

            cy + 46 * math.sin(rad),

            GOLD,

            1,

            0.6,

        )

    page.y = y + 210 + 36


def button(label: str, width: int, filled: bool) -> str:

    height = 48

    fill = ESPRESSO if filled else CREAM

    text_fill = IVORY if filled else ESPRESSO

    stroke = GOLD if filled else BEIGE

    dot = GOLD if filled else CARAMEL

    label_w = est_width(label, 14, 700, 1.1)

    content = 10 + 16 + label_w

    # redraw width from content so the label stays centered as a group

    width = max(width, int(content + 36))

    text_x = (width + 16) / 2

    svg = [

        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '

        f'viewBox="0 0 {width} {height}" role="img">',

        f"<title>{esc(label)}</title>",

        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="24" '

        f'fill="{fill}" stroke="{stroke}"/>',

        f'<circle cx="22" cy="24" r="3" fill="{dot}"/>',

        f'<text x="{text_x:.1f}" y="29" fill="{text_fill}" font-family="{FONT}" '

        f'font-size="14" font-weight="700" text-anchor="middle" letter-spacing="1.1">'

        f"{esc(label)}</text>",

        "</svg>",

    ]

    return "\n".join(svg) + "\n", width


def main() -> None:

    page = Page()

    page.rect(0, 0, W, 4000, 0, IVORY)

    hero(page)

    about(page)

    stack(page)

    projects(page)

    experience(page)

    education(page)

    contact(page)

    height = math.ceil(page.y)

# repaint background to the true height by replacing the placeholder later

    svg = page.finish()

    svg = svg.replace(f'width="{W}" height="{height}"', f'width="{W}" height="{height}"', 1)

# The placeholder rect used a fixed height. Patch it to the real page height.

    svg = svg.replace(

        f'<rect x="0.0" y="0.0" width="{W}.0" height="4000.0" rx="0.0" fill="{IVORY}"/>',

        f'<rect x="0" y="0" width="{W}" height="{height}" fill="{IVORY}"/>',

        1,

    )


    OUT.mkdir(exist_ok=True)

    (OUT / "profile.svg").write_text(svg, encoding="utf-8")


    buttons = {

        "btn-email.svg": ("Email", 148, True),

        "btn-linkedin.svg": ("LinkedIn", 168, True),

        "btn-github.svg": ("GitHub", 156, True),

        "repo-emotion.svg": ("Emotion Recognition", 230, False),

        "repo-ppe.svg": ("PPE Detection", 200, False),

        "repo-jobs.svg": ("AI Job Matcher", 200, False),

    }

    for name, (label, width, filled) in buttons.items():

        content, _width = button(label, width, filled)

        (OUT / name).write_text(content, encoding="utf-8")


    if issues:

        print("LAYOUT WARNINGS")

        for item in issues:

            print(" -", item)

    else:

        print("No overflow warnings")

    print(f"Wrote {OUT / 'profile.svg'} ({height}px)")


if __name__ == "__main__":

    main()
