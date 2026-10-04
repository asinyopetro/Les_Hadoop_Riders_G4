# -*- coding: utf-8 -*-
"""Génère le PowerPoint de présentation G4 (~10 min)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
# Couleurs (tech / Hadoop — pas violet IA)
TEAL = RGBColor(0x0F, 0x5C, 0x4C)
TEAL_LIGHT = RGBColor(0x14, 0x7A, 0x66)
SLATE = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x47, 0x55, 0x69)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CREAM = RGBColor(0xF8, 0xFA, 0xF9)
ACCENT = RGBColor(0xC2, 0x41, 0x0C)  # orange terre pour accent ponctuel

W, H = Inches(13.333), Inches(7.5)  # 16:9


def set_run(run, size=20, bold=False, color=SLATE, font="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_rect(slide, left, top, width, height, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    return shape


def footer(slide, speaker, page, total=12):
    # barre bas
    add_rect(slide, 0, Inches(6.95), W, Inches(0.55), TEAL)
    box = slide.shapes.add_textbox(Inches(0.4), Inches(7.05), Inches(10), Inches(0.35))
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = f"Présenté par : {speaker}"
    set_run(run, 12, True, WHITE)
    num = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.35))
    tf2 = num.text_frame
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.RIGHT
    r2 = p2.add_run()
    r2.text = f"{page} / {total}"
    set_run(r2, 11, False, WHITE)


def title_bar(slide, title):
    add_rect(slide, 0, 0, W, Inches(1.15), TEAL)
    add_rect(slide, 0, Inches(1.15), W, Inches(0.08), ACCENT)
    box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.7))
    tf = box.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    set_run(run, 28, True, WHITE)


def bullets(slide, items, left=0.5, top=1.5, width=12.3, height=5.2, size=20):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = item.get("level", 0)
        p.space_after = Pt(10)
        run = p.add_run()
        run.text = item["text"]
        set_run(run, item.get("size", size), item.get("bold", False), item.get("color", SLATE))
    return tf


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # --- 1 Titre ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, TEAL)
    add_rect(s, 0, Inches(5.8), W, Inches(1.7), SLATE)
    t = s.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.2))
    p = t.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Cluster Hadoop avec Docker"
    set_run(r, 40, True, WHITE)
    t2 = s.shapes.add_textbox(Inches(0.8), Inches(3.1), Inches(11.5), Inches(0.6))
    p = t2.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "UA1 — Projet 1 | Groupe G4 — Les_Hadoop_Riders"
    set_run(r, 22, False, RGBColor(0xD1, 0xFA, 0xE5))
    t3 = s.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.5), Inches(1.0))
    tf = t3.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Komla · Kassoum · Joel · Forbes · Frank · Wren"
    set_run(r, 16, False, WHITE)
    p = tf.add_paragraph()
    r = p.add_run()
    r.text = "Image : leshadoopriders/hadoop-tp-g4:1.0"
    set_run(r, 14, False, RGBColor(0xCB, 0xD5, 0xE1))
    footer(s, "Komla Petro Asinyo", 1)
    add_notes(s, "Bonjour, nous sommes Les_Hadoop_Riders, groupe G4. "
              "On présente notre cluster Hadoop (HDFS + YARN) déployé avec Docker. "
              "Durée prévue : environ 8 à 10 minutes.")

    # --- 2 Plan ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Plan de la présentation")
    bullets(s, [
        {"text": "1. Cas d’usage Big Data (e-commerce) et les 3V", "bold": True},
        {"text": "2. HDFS vs système de fichiers classique"},
        {"text": "3. YARN : ResourceManager et NodeManager"},
        {"text": "4. Architecture Docker (1 master + 5 workers)"},
        {"text": "5. Déploiement, image Docker Hub"},
        {"text": "6. Manipulations HDFS et job π sur YARN"},
        {"text": "7. Monitoring, setrep, problèmes rencontrés"},
        {"text": "8. Conclusion"},
    ], size=22)
    footer(s, "Komla Petro Asinyo", 2)
    add_notes(s, "Voici le plan. Chacun présente sa partie. On commence par le contexte théorique.")

    # --- 3 3V ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Cas d’usage : e-commerce et les 3V")
    bullets(s, [
        {"text": "Contexte : chaîne de magasins (ventes, logs web, stocks)", "bold": True},
        {"text": "Volume — millions d’événements, historique long"},
        {"text": "Vélocité — commandes / paiements en continu"},
        {"text": "Variété — CSV, JSON, logs, images produits"},
        {"text": "Pourquoi Hadoop ?", "bold": True, "color": TEAL},
        {"text": "HDFS → stocker en distribué  |  YARN → lancer les traitements"},
    ], size=22)
    footer(s, "Kassoum Dene", 3)
    add_notes(s, "On a choisi l’e-commerce. Expliquer chaque V avec un exemple concret. "
              "HDFS pour stocker, YARN pour traiter.")

    # --- 4 HDFS ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "HDFS vs système de fichiers classique")
    # deux colonnes
    add_rect(s, Inches(0.5), Inches(1.5), Inches(5.8), Inches(4.9), WHITE)
    add_rect(s, Inches(6.9), Inches(1.5), Inches(5.8), Inches(4.9), WHITE)
    bullets(s, [
        {"text": "FS classique (NTFS, ext4)", "bold": True, "color": TEAL, "size": 20},
        {"text": "Fichier sur une seule machine"},
        {"text": "Métadonnées gérées par l’OS local"},
        {"text": "Si le disque tombe → données perdues"},
    ], left=0.7, top=1.7, width=5.4, height=4.5, size=18)
    bullets(s, [
        {"text": "HDFS", "bold": True, "color": TEAL, "size": 20},
        {"text": "Fichier découpé en blocs"},
        {"text": "Blocs répliqués sur plusieurs DataNodes"},
        {"text": "NameNode = namespace (noms + emplacements)"},
        {"text": "Tolérance aux pannes par réplication"},
    ], left=7.1, top=1.7, width=5.4, height=4.5, size=18)
    footer(s, "Joel Kazoni Tugirimana", 4)
    add_notes(s, "Comparer clairement local vs HDFS. Insister sur blocs + réplication + rôle NameNode.")

    # --- 5 YARN ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "YARN : ResourceManager et NodeManager")
    bullets(s, [
        {"text": "ResourceManager (master)", "bold": True, "color": TEAL},
        {"text": "Reçoit la demande de job, connaît les ressources du cluster"},
        {"text": "Alloue des conteneurs, démarre l’ApplicationMaster"},
        {"text": "NodeManager (chaque worker)", "bold": True, "color": TEAL},
        {"text": "Lance et surveille les conteneurs sur sa machine"},
        {"text": "Remonte l’état au ResourceManager"},
        {"text": "En une phrase : RM orchestre, NM exécute localement.", "bold": True},
    ], size=20)
    footer(s, "Forbes Magène", 5)
    add_notes(s, "Bien séparer RM et NM. Si le prof demande ApplicationMaster : c’est le chef du job, "
              "lancé grâce au RM, qui négocie les ressources.")

    # --- 6 Architecture ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Architecture : 1 master + 5 workers")
    bullets(s, [
        {"text": "hadoop-master", "bold": True, "color": TEAL},
        {"text": "NameNode + ResourceManager + SecondaryNameNode"},
        {"text": "hadoop-worker1 … worker5", "bold": True, "color": TEAL},
        {"text": "Chaque worker : DataNode + NodeManager"},
        {"text": "Réseau Docker : hadoop-net", "bold": True},
        {"text": "Ports : 9870 (UI HDFS) · 8088 (UI YARN) · 9000 (HDFS RPC)"},
        {"text": "Image : leshadoopriders/hadoop-tp-g4:1.0"},
    ], size=20)
    footer(s, "Frank A Simo Ngounou", 6)
    add_notes(s, "Montrer mentalement le schéma : 1 master, 5 workers. Citer les ports utiles pour la démo.")

    # --- 7 Déploiement ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Déploiement et publication Docker Hub")
    bullets(s, [
        {"text": "Lancer le cluster", "bold": True, "color": TEAL},
        {"text": "docker compose up --build -d"},
        {"text": "Vérifier : docker ps  →  6 conteneurs"},
        {"text": "hdfs dfsadmin -report  →  Live datanodes (5)"},
        {"text": "Publier l’image", "bold": True, "color": TEAL},
        {"text": "docker push leshadoopriders/hadoop-tp-g4:1.0"},
        {"text": "Hub : hub.docker.com/r/leshadoopriders/hadoop-tp-g4"},
    ], size=20)
    footer(s, "Frank A Simo Ngounou", 7)
    add_notes(s, "Dire les commandes à voix haute. Rappeler que Docker Hub impose les minuscules (g4).")

    # --- 8 HDFS pratique ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Manipulations HDFS (données ventes)")
    bullets(s, [
        {"text": "mkdir + chmod + put  →  /data/ventes/2026/transactions.csv"},
        {"text": "fsck / stat  →  1 bloc, réplication 3, HEALTHY"},
        {"text": "cat | head  →  lecture des 5 premières lignes"},
        {"text": "getmerge  →  fusion de deux CSV"},
        {"text": "rm + Trash  →  suppression avec corbeille"},
        {"text": "setrep -w 2  →  réplication passée à 2"},
    ], size=20)
    footer(s, "Wren Surprenant-Nicolson", 8)
    add_notes(s, "Parcourir les étapes dans l’ordre. Fichier petit = 1 seul bloc (normal, bloc 128 Mo).")

    # --- 9 Job pi ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Job YARN : calcul de π (Monte Carlo)")
    bullets(s, [
        {"text": "yarn jar …/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000", "bold": True},
        {"text": "Application : application_1791039798429_0001"},
        {"text": "Nom : QuasiMonteCarlo"},
        {"text": "État final : SUCCEEDED"},
        {"text": "Estimation de π ≈ 3.14"},
        {"text": "Visible dans l’UI YARN : http://localhost:8088"},
    ], size=20)
    footer(s, "Forbes Magène", 9)
    add_notes(s, "Expliquer vite Monte Carlo (points aléatoires). Insister sur SUCCEEDED et le numéro d’app.")

    # --- 10 Monitoring ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Monitoring : interfaces web")
    bullets(s, [
        {"text": "NameNode UI — localhost:9870", "bold": True, "color": TEAL},
        {"text": "5 DataNodes actifs, pas de missing block"},
        {"text": "YARN UI — localhost:8088", "bold": True, "color": TEAL},
        {"text": "Job pi en FINISHED / SUCCEEDED"},
        {"text": "Métriques : mémoire et vcores consommés"},
        {"text": "setrep : NameNode met à jour la cible de réplication"},
    ], size=20)
    footer(s, "Joel Kazoni Tugirimana", 10)
    add_notes(s, "Si possible ouvrir les UI en live. Sinon montrer les captures du rapport.")

    # --- 11 Troubleshooting ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Problèmes rencontrés (et solutions)")
    bullets(s, [
        {"text": "1. pull access denied (image pas encore sur Hub)", "bold": True},
        {"text": "→ pull_policy: never + build local", "level": 1, "size": 18},
        {"text": "2. Tag avec majuscules refusé par Docker Hub", "bold": True},
        {"text": "→ leshadoopriders/hadoop-tp-g4:1.0 (minuscules)", "level": 1, "size": 18},
        {"text": "3. Téléchargement Hadoop trop lent", "bold": True},
        {"text": "→ image de base apache/hadoop:3.3.6 + notre config", "level": 1, "size": 18},
    ], size=20)
    footer(s, "Kassoum Dene", 11)
    add_notes(s, "Montrer qu’on a débogué pour de vrai. Une phrase cause → solution pour chaque point.")

    # --- 12 Conclusion ---
    s = prs.slides.add_slide(blank)
    add_rect(s, 0, 0, W, H, CREAM)
    title_bar(s, "Conclusion")
    bullets(s, [
        {"text": "Cluster opérationnel : 1 master + 5 DataNodes"},
        {"text": "HDFS manipulé (droits, fsck, merge, trash, setrep)"},
        {"text": "Job MapReduce π terminé avec succès (SUCCEEDED)"},
        {"text": "Image publiée sur Docker Hub"},
        {"text": "Merci — questions ?", "bold": True, "color": TEAL, "size": 24},
    ], size=22)
    footer(s, "Komla Petro Asinyo", 12)
    add_notes(s, "Récap en 20 secondes, puis ouvrir les questions. "
              "Rappeler Hub + GitHub si demandé.")

    out = r"C:\Users\asiny\Desktop\Les_Hadoop_Riders_G4\presentation\PRESENTATION-G4-Les_Hadoop_Riders.pptx"
    prs.save(out)
    print("OK", out)


if __name__ == "__main__":
    build()
