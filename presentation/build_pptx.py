# -*- coding: utf-8 -*-
"""Génère le PowerPoint G4 enrichi (captures, schéma, liens)."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

TEAL = RGBColor(0x0F, 0x5C, 0x4C)
TEAL_MID = RGBColor(0x14, 0x7A, 0x66)
SLATE = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x47, 0x55, 0x69)
MUTED = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CREAM = RGBColor(0xF1, 0xF5, 0xF4)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0xC2, 0x41, 0x0C)
BLUE = RGBColor(0x1D, 0x4E, 0x89)
ORANGE = RGBColor(0xEA, 0x58, 0x0C)
GREEN = RGBColor(0x15, 0x80, 0x3D)

W, H = Inches(13.333), Inches(7.5)
ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "captures"

HUB = "https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4"
GITHUB = "https://github.com/asinyopetro/Les_Hadoop_Riders_G4"
UI_HDFS = "http://localhost:9870"
UI_YARN = "http://localhost:8088"
UI_DN = "http://localhost:9870/dfshealth.html#tab-datanode"


def set_run(run, size=20, bold=False, color=SLATE, font="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_rect(slide, left, top, width, height, fill, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1.25)
    try:
        shape.adjustments[0] = 0.08
    except Exception:
        pass
    return shape


def add_hard_rect(slide, left, top, width, height, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    return shape


def footer(slide, speaker, page, total=12):
    add_hard_rect(slide, 0, Inches(6.95), W, Inches(0.55), TEAL)
    box = slide.shapes.add_textbox(Inches(0.35), Inches(7.05), Inches(10.2), Inches(0.35))
    p = box.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = f"Présenté par : {speaker}"
    set_run(r, 12, True, WHITE)
    num = slide.shapes.add_textbox(Inches(11.4), Inches(7.05), Inches(1.6), Inches(0.35))
    p2 = num.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.RIGHT
    r2 = p2.add_run()
    r2.text = f"{page} / {total}"
    set_run(r2, 11, False, WHITE)


def title_bar(slide, title):
    add_hard_rect(slide, 0, 0, W, Inches(1.05), TEAL)
    add_hard_rect(slide, 0, Inches(1.05), W, Inches(0.07), ACCENT)
    box = slide.shapes.add_textbox(Inches(0.45), Inches(0.28), Inches(12.4), Inches(0.6))
    r = box.text_frame.paragraphs[0].add_run()
    r.text = title
    set_run(r, 26, True, WHITE)


def textbox(slide, left, top, width, height, lines, size=18, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(line.get("space", 6))
        r = p.add_run()
        r.text = line["text"]
        set_run(r, line.get("size", size), line.get("bold", False), line.get("color", SLATE))
        if line.get("url"):
            r.hyperlink.address = line["url"]
    return box


def link_chip(slide, left, top, width, label, url, fill=TEAL_MID):
    shape = add_rect(slide, Inches(left), Inches(top), Inches(width), Inches(0.42), fill)
    # clicable via textbox overlay
    box = slide.shapes.add_textbox(Inches(left), Inches(top + 0.05), Inches(width), Inches(0.35))
    p = box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    set_run(r, 12, True, WHITE)
    r.hyperlink.address = url
    return shape


def add_pic(slide, name, left, top, width=None, height=None):
    path = CAP / name
    if not path.exists():
        return None
    kwargs = {}
    if width is not None:
        kwargs["width"] = Inches(width)
    if height is not None:
        kwargs["height"] = Inches(height)
    return slide.shapes.add_picture(str(path), Inches(left), Inches(top), **kwargs)


def caption(slide, left, top, width, text):
    textbox(slide, left, top, width, 0.3, [
        {"text": text, "size": 11, "color": MUTED}
    ])


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def node_box(slide, left, top, w, h, title, lines, fill=TEAL):
    add_rect(slide, Inches(left), Inches(top), Inches(w), Inches(h), fill)
    textbox(slide, left + 0.1, top + 0.08, w - 0.2, h - 0.15, [
        {"text": title, "size": 14, "bold": True, "color": WHITE, "space": 4},
        *[{"text": x, "size": 11, "color": WHITE, "space": 2} for x in lines],
    ])


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # ========== 1 TITRE ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, TEAL)
    add_hard_rect(s, Inches(8.2), 0, Inches(5.2), H, SLATE)
    # image droite (datanodes)
    add_pic(s, "screenshot-datanodes.png", 8.45, 1.4, width=4.7)
    caption(s, 8.45, 5.55, 4.7, "Capture UI — 5 DataNodes actifs")
    textbox(s, 0.6, 1.5, 7.2, 1.2, [
        {"text": "Cluster Hadoop", "size": 38, "bold": True, "color": WHITE, "space": 4},
        {"text": "avec Docker", "size": 34, "bold": True, "color": RGBColor(0xD1, 0xFA, 0xE5)},
    ])
    textbox(s, 0.6, 3.3, 7.2, 1.4, [
        {"text": "UA1 — Projet 1  |  Groupe G4", "size": 18, "color": WHITE, "space": 8},
        {"text": "Les_Hadoop_Riders", "size": 22, "bold": True, "color": WHITE, "space": 10},
        {"text": "HDFS · YARN · Docker Compose · MapReduce π", "size": 14, "color": RGBColor(0xCB, 0xD5, 0xE1)},
    ])
    link_chip(s, 0.6, 5.2, 3.3, "Docker Hub →", HUB)
    link_chip(s, 4.1, 5.2, 3.0, "GitHub →", GITHUB, BLUE)
    footer(s, "Komla Petro Asinyo", 1)
    add_notes(s, "Introduire le groupe. Montrer qu’on a une vraie UI avec 5 DataNodes. Citer Hub + GitHub.")

    # ========== 2 PLAN ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Plan de la présentation")
    items = [
        ("01", "E-commerce & 3V", "Kassoum"),
        ("02", "HDFS vs FS local", "Joel"),
        ("03", "YARN (RM / NM)", "Forbes"),
        ("04", "Architecture Docker", "Frank"),
        ("05", "Déploiement & Hub", "Frank"),
        ("06", "Manipulations HDFS", "Wren"),
        ("07", "Job π + monitoring", "Forbes / Joel"),
        ("08", "Troubles & conclusion", "Kassoum / Komla"),
    ]
    for i, (num, label, who) in enumerate(items):
        col = i % 4
        row = i // 4
        left = 0.45 + col * 3.2
        top = 1.45 + row * 2.4
        add_rect(s, Inches(left), Inches(top), Inches(3.0), Inches(2.1), CARD, TEAL_MID)
        textbox(s, left + 0.15, top + 0.25, 2.7, 1.7, [
            {"text": num, "size": 22, "bold": True, "color": TEAL, "space": 6},
            {"text": label, "size": 16, "bold": True, "color": SLATE, "space": 8},
            {"text": who, "size": 13, "color": MUTED},
        ])
    footer(s, "Komla Petro Asinyo", 2)
    add_notes(s, "Annoncer le plan rapidement, sans lire chaque carte.")

    # ========== 3 3V ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Cas d’usage e-commerce — les 3V")
    cards = [
        (0.4, "Volume", "Millions d’événements\nhistorique multi-années", BLUE, "📦"),
        (4.55, "Vélocité", "Commandes & paiements\nen continu", ORANGE, "⚡"),
        (8.7, "Variété", "CSV, JSON, logs,\nimages produits", GREEN, "🧩"),
    ]
    for left, title, body, color, icon in cards:
        add_rect(s, Inches(left), Inches(1.4), Inches(3.85), Inches(3.4), CARD, color)
        add_hard_rect(s, Inches(left), Inches(1.4), Inches(3.85), Inches(0.7), color)
        textbox(s, left + 0.2, 1.5, 3.4, 0.5, [
            {"text": f"{icon}  {title}", "size": 20, "bold": True, "color": WHITE}
        ])
        textbox(s, left + 0.25, 2.4, 3.4, 2.0, [
            {"text": line, "size": 16, "color": SLATE, "space": 8}
            for line in body.split("\n")
        ])
    textbox(s, 0.5, 5.1, 12.2, 1.4, [
        {"text": "Chaîne de magasins : tickets de caisse + logs web + stocks", "size": 16, "bold": True, "color": TEAL, "space": 6},
        {"text": "HDFS → stockage distribué     |     YARN → traitements (MapReduce, etc.)", "size": 16, "color": SLATE},
    ])
    footer(s, "Kassoum Dene", 3)
    add_notes(s, "Un exemple concret par V. Finir sur HDFS + YARN.")

    # ========== 4 HDFS ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "HDFS vs système de fichiers classique")
    # gauche FS local
    add_rect(s, Inches(0.4), Inches(1.35), Inches(5.9), Inches(5.2), CARD, GRAY)
    textbox(s, 0.6, 1.5, 5.5, 0.5, [{"text": "FS classique (NTFS / ext4)", "size": 18, "bold": True, "color": GRAY}])
    # disque unique
    node_box(s, 1.7, 2.4, 3.2, 1.6, "1 machine", ["Fichier entier", "OS local = métadonnées"], SLATE)
    textbox(s, 0.7, 4.4, 5.3, 1.6, [
        {"text": "• Un seul point de défaillance", "size": 15, "space": 6},
        {"text": "• Pas de réplication native", "size": 15, "space": 6},
        {"text": "• Limité à la capacité du disque", "size": 15},
    ])
    # droite HDFS
    add_rect(s, Inches(6.7), Inches(1.35), Inches(6.2), Inches(5.2), CARD, TEAL)
    textbox(s, 6.9, 1.5, 5.8, 0.45, [{"text": "HDFS (distribué)", "size": 18, "bold": True, "color": TEAL}])
    node_box(s, 8.3, 2.15, 2.8, 1.0, "NameNode", ["namespace + blocs"], TEAL)
    # 3 DN
    for i, x in enumerate([7.0, 9.0, 11.0]):
        node_box(s, x, 3.5, 1.8, 1.15, f"DN{i+1}", ["blocs répliqués"], TEAL_MID)
    textbox(s, 6.9, 5.0, 5.8, 1.2, [
        {"text": "Fichier découpé en blocs + réplication", "size": 14, "bold": True, "color": SLATE, "space": 4},
        {"text": "Tolérance aux pannes sur plusieurs nœuds", "size": 14, "color": SLATE},
    ])
    footer(s, "Joel Kazoni Tugirimana", 4)
    add_notes(s, "Pointer le schéma : NameNode en haut, DataNodes en bas avec réplication.")

    # ========== 5 YARN ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "YARN : ResourceManager et NodeManager")
    # flux
    node_box(s, 0.5, 1.5, 3.6, 2.2, "1. Client", ["soumet le job", "yarn jar … pi 4 1000"], BLUE)
    node_box(s, 4.8, 1.5, 3.8, 2.2, "2. ResourceManager", ["master", "alloue conteneurs", "lance ApplicationMaster"], TEAL)
    node_box(s, 9.3, 1.5, 3.5, 2.2, "3. NodeManagers", ["sur chaque worker", "exécutent les tâches"], TEAL_MID)
    add_pic(s, "screenshot-yarn.png", 0.5, 4.0, width=7.8)
    caption(s, 0.5, 6.45, 7.8, "UI YARN — http://localhost:8088")
    textbox(s, 8.5, 4.0, 4.4, 2.5, [
        {"text": "En résumé", "size": 16, "bold": True, "color": TEAL, "space": 8},
        {"text": "RM orchestre", "size": 15, "space": 6},
        {"text": "NM exécute localement", "size": 15, "space": 10},
        {"text": "Ouvrir l’UI →", "size": 14, "bold": True, "color": BLUE, "url": UI_YARN},
    ])
    footer(s, "Forbes Magène", 5)
    add_notes(s, "Suivre les 3 boîtes. Montrer la capture YARN.")

    # ========== 6 ARCHITECTURE ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Architecture Docker — 1 master + 5 workers")
    node_box(s, 3.5, 1.35, 6.3, 1.55, "hadoop-master", [
        "NameNode · ResourceManager · SecondaryNameNode",
        "Ports : 9870 · 8088 · 9000",
    ], TEAL)
    for i in range(5):
        x = 0.45 + i * 2.55
        node_box(s, x, 3.3, 2.4, 1.45, f"worker{i+1}", ["DataNode", "NodeManager"], TEAL_MID)
    textbox(s, 0.5, 5.05, 12.2, 1.5, [
        {"text": "Réseau Docker : hadoop-net     |     Image : leshadoopriders/hadoop-tp-g4:1.0", "size": 15, "bold": True, "color": SLATE, "space": 8},
        {"text": "UI HDFS →  localhost:9870", "size": 14, "color": BLUE, "url": UI_HDFS, "space": 4},
        {"text": "UI YARN →  localhost:8088", "size": 14, "color": BLUE, "url": UI_YARN},
    ])
    footer(s, "Frank A Simo Ngounou", 6)
    add_notes(s, "Montrer le schéma master au-dessus, 5 workers en dessous.")

    # ========== 7 DEPLOIEMENT ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Déploiement + publication Docker Hub")
    textbox(s, 0.45, 1.3, 5.8, 3.8, [
        {"text": "Commandes clés", "size": 18, "bold": True, "color": TEAL, "space": 10},
        {"text": "docker compose up --build -d", "size": 15, "space": 8},
        {"text": "docker ps   →  6 conteneurs", "size": 15, "space": 8},
        {"text": "hdfs dfsadmin -report", "size": 15, "space": 8},
        {"text": "→ Live datanodes (5)", "size": 15, "bold": True, "color": GREEN, "space": 12},
        {"text": "docker push …/hadoop-tp-g4:1.0", "size": 15, "space": 10},
        {"text": "Ouvrir Docker Hub →", "size": 14, "bold": True, "color": BLUE, "url": HUB, "space": 4},
        {"text": "Ouvrir GitHub →", "size": 14, "bold": True, "color": BLUE, "url": GITHUB},
    ])
    add_pic(s, "screenshot-terminal-01.png", 6.4, 1.25, width=6.5)
    caption(s, 6.4, 5.05, 6.5, "Terminal — docker ps / dfsadmin")
    add_pic(s, "screenshot-namenode.png", 6.4, 5.35, height=1.4)
    footer(s, "Frank A Simo Ngounou", 7)
    add_notes(s, "Montrer le terminal. Rappeler Hub en minuscules.")

    # ========== 8 HDFS PRATIQUE ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Manipulations HDFS — /data/ventes/2026")
    textbox(s, 0.4, 1.25, 5.6, 5.2, [
        {"text": "Étapes réalisées", "size": 17, "bold": True, "color": TEAL, "space": 8},
        {"text": "1. mkdir + chmod + put (CSV)", "size": 15, "space": 7},
        {"text": "2. fsck / stat → HEALTHY, rep=3", "size": 15, "space": 7},
        {"text": "3. cat | head (5 lignes)", "size": 15, "space": 7},
        {"text": "4. getmerge (2 fichiers)", "size": 15, "space": 7},
        {"text": "5. rm + Trash", "size": 15, "space": 7},
        {"text": "6. setrep -w 2 → réplication 2", "size": 15, "bold": True, "color": GREEN, "space": 12},
        {"text": "Fichier petit = 1 bloc (128 Mo)", "size": 13, "color": MUTED},
    ])
    add_pic(s, "screenshot-terminal-02.png", 6.2, 1.3, width=6.7)
    caption(s, 6.2, 5.15, 6.7, "Terminal — commandes HDFS")
    footer(s, "Wren Surprenant-Nicolson", 8)
    add_notes(s, "Parcourir la liste en montrant la capture.")

    # ========== 9 JOB PI ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Job YARN — calcul de π (SUCCEEDED)")
    textbox(s, 0.4, 1.25, 5.5, 4.5, [
        {"text": "yarn jar … examples … pi 4 1000", "size": 15, "bold": True, "color": TEAL, "space": 10},
        {"text": "App : application_…_0001", "size": 15, "space": 7},
        {"text": "Nom : QuasiMonteCarlo", "size": 15, "space": 7},
        {"text": "État : SUCCEEDED", "size": 18, "bold": True, "color": GREEN, "space": 7},
        {"text": "π ≈ 3.14", "size": 18, "bold": True, "color": SLATE, "space": 12},
        {"text": "UI YARN →", "size": 14, "bold": True, "color": BLUE, "url": UI_YARN, "space": 4},
        {"text": "Détail application →", "size": 14, "bold": True, "color": BLUE, "url": UI_YARN},
    ])
    add_pic(s, "screenshot-yarn-app.png", 6.1, 1.25, width=6.8)
    caption(s, 6.1, 4.85, 6.8, "Détail application — FINISHED / SUCCEEDED")
    add_pic(s, "screenshot-terminal-03.png", 6.1, 5.15, height=1.55)
    footer(s, "Forbes Magène", 9)
    add_notes(s, "Insister SUCCEEDED + numéro d’app. Capture UI à droite.")

    # ========== 10 MONITORING ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Monitoring — interfaces web")
    add_pic(s, "screenshot-namenode.png", 0.35, 1.3, width=6.2)
    caption(s, 0.35, 4.55, 6.2, "NameNode — localhost:9870")
    add_pic(s, "screenshot-datanodes.png", 6.8, 1.3, width=6.1)
    caption(s, 6.8, 4.55, 6.1, "DataNodes — 5 Live")
    link_chip(s, 0.35, 5.0, 3.5, "Ouvrir NameNode →", UI_HDFS)
    link_chip(s, 4.0, 5.0, 3.5, "Liste DataNodes →", UI_DN, BLUE)
    link_chip(s, 7.7, 5.0, 3.5, "Ouvrir YARN →", UI_YARN, ORANGE)
    textbox(s, 0.4, 5.6, 12.2, 1.0, [
        {"text": "Pas de missing block  ·  setrep met à jour la cible de réplication sur le NameNode", "size": 14, "color": SLATE},
    ])
    footer(s, "Joel Kazoni Tugirimana", 10)
    add_notes(s, "Montrer les deux captures. Cliquer les liens si connexion live.")

    # ========== 11 TROUBLESHOOTING ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Problèmes rencontrés → solutions")
    problems = [
        ("Pull access denied", "Image pas encore sur Hub", "pull_policy: never + build local", ACCENT),
        ("Tag majuscules", "Docker Hub refuse G4", "leshadoopriders/hadoop-tp-g4:1.0", ORANGE),
        ("Download trop lent", "archive.apache.org bloqué", "Base apache/hadoop:3.3.6", BLUE),
    ]
    for i, (title, cause, sol, color) in enumerate(problems):
        top = 1.35 + i * 1.7
        add_rect(s, Inches(0.45), Inches(top), Inches(12.4), Inches(1.55), CARD, color)
        add_hard_rect(s, Inches(0.45), Inches(top), Inches(0.18), Inches(1.55), color)
        textbox(s, 0.85, top + 0.15, 11.7, 1.3, [
            {"text": f"{i+1}. {title}", "size": 17, "bold": True, "color": SLATE, "space": 4},
            {"text": f"Cause : {cause}", "size": 14, "color": MUTED, "space": 4},
            {"text": f"Solution : {sol}", "size": 15, "bold": True, "color": TEAL},
        ])
    footer(s, "Kassoum Dene", 11)
    add_notes(s, "3 problèmes, 3 solutions. Lien Hub pour prouver la publication.")

    # ========== 12 CONCLUSION ==========
    s = prs.slides.add_slide(blank)
    add_hard_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Conclusion — merci !")
    bullets = [
        "Cluster 1 master + 5 DataNodes opérationnel",
        "HDFS : droits, fsck, merge, trash, setrep",
        "Job MapReduce π → SUCCEEDED (π ≈ 3.14)",
        "Image publique sur Docker Hub",
    ]
    for i, b in enumerate(bullets):
        y = 1.35 + i * 0.85
        add_rect(s, Inches(0.5), Inches(y), Inches(7.8), Inches(0.72), CARD, TEAL_MID)
        textbox(s, 0.75, y + 0.18, 7.4, 0.5, [{"text": f"✓  {b}", "size": 16, "bold": True, "color": SLATE}])
    add_pic(s, "screenshot-yarn-app.png", 8.6, 1.35, width=4.3)
    caption(s, 8.6, 4.3, 4.3, "Preuve job SUCCEEDED")
    link_chip(s, 8.6, 4.7, 4.3, "Docker Hub →", HUB)
    link_chip(s, 8.6, 5.3, 4.3, "GitHub du projet →", GITHUB, BLUE)
    textbox(s, 0.5, 5.0, 7.8, 1.4, [
        {"text": "Questions ?", "size": 28, "bold": True, "color": TEAL, "space": 6},
        {"text": "Komla · Kassoum · Joel · Forbes · Frank · Wren", "size": 13, "color": MUTED},
    ])
    footer(s, "Komla Petro Asinyo", 12)
    add_notes(s, "Récap 20 s. Pointer Hub + GitHub. Ouvrir les questions.")

    out = ROOT / "presentation" / "PRESENTATION-G4-Les_Hadoop_Riders.pptx"
    prs.save(str(out))
    print("OK", out)
    return out


if __name__ == "__main__":
    build()
