"""
Generate UI capture images for the Livrable 2 deliverable.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("eval/captures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1200, 750
BG_COLOR = (248, 249, 250)
SIDEBAR_BG = (240, 242, 246)
PRIMARY = (255, 75, 75)
TEXT_COLOR = (49, 51, 63)
MUTED = (128, 131, 140)
CARD_BG = (255, 255, 255)
BORDER_COLOR = (224, 226, 230)
GREEN = (40, 167, 69)
RED = (220, 53, 69)

def draw_base_ui(draw, role_label, allowed_families, query_text="", has_photo=False):
    # Sidebar
    draw.rectangle([0, 0, 320, H], fill=SIDEBAR_BG)
    draw.line([320, 0, 320, H], fill=BORDER_COLOR, width=2)
    draw.text((30, 30), "⚙️ Configuration", fill=TEXT_COLOR)
    draw.text((30, 70), "Groupe utilisateur :", fill=MUTED)
    draw.rectangle([30, 95, 290, 135], fill=(255, 255, 255), outline=BORDER_COLOR)
    draw.text((40, 105), role_label, fill=TEXT_COLOR)
    
    draw.text((30, 160), "Familles autorisées :", fill=TEXT_COLOR)
    y = 190
    for fam in allowed_families:
        draw.rectangle([30, y, 290, y + 30], fill=(235, 240, 255), outline=(180, 200, 240))
        draw.text((40, y + 7), f"✓ {fam}", fill=(30, 60, 150))
        y += 40
        
    # Main Header
    draw.text((350, 30), "🔧 MaintiDoc — Recherche Multimodale", fill=TEXT_COLOR)
    draw.text((350, 60), "Livrable 2 · Qdrant + BGE-M3 + CLIP ViT-B/32 · EMSI-2026", fill=MUTED)
    draw.line([350, 90, 1150, 90], fill=BORDER_COLOR, width=1)
    
    # Input Area
    draw.text((350, 110), "🔍 Question / Requête texte :", fill=TEXT_COLOR)
    draw.rectangle([350, 135, 1150, 180], fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((365, 148), query_text, fill=TEXT_COLOR if query_text else MUTED)
    
    # Photo box
    if has_photo:
        draw.rectangle([350, 195, 1150, 240], fill=(240, 248, 255), outline=(100, 160, 240), width=1)
        draw.text((365, 208), "📷 Photo query jointe : mire_test_buses_nozzle_check_epson.png (1024x768)", fill=(30, 80, 180))
    else:
        draw.rectangle([350, 195, 1150, 240], fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((365, 208), "📷 Glisser-déposer une image de composant ou schéma (optionnel)", fill=MUTED)

# 1. Recherche Texte
img1 = Image.new("RGB", (W, H), BG_COLOR)
d1 = ImageDraw.Draw(img1)
draw_base_ui(d1, "techniciens_audiovisuel", ["appareils_photo"], "Comment nettoyer le capteur d'un Canon EOS R50 ?")
d1.rectangle([350, 260, 480, 300], fill=PRIMARY)
d1.text((375, 272), "Rechercher", fill=(255, 255, 255))
d1.rectangle([350, 320, 1150, 360], fill=(230, 245, 230), outline=GREEN)
d1.text((365, 332), "✓ 2 résultat(s) trouvé(s) — Pré-filtrage RBAC validé (famille: appareils_photo)", fill=GREEN)

# Result Card 1
d1.rectangle([350, 380, 1150, 520], fill=CARD_BG, outline=BORDER_COLOR)
d1.text((370, 395), "#1 — proc_nettoyage_capteur_canon_officiel p.1 [texte] · Score RRF = 0.0328", fill=(20, 50, 120))
d1.text((370, 425), "Extrait retenu :", fill=MUTED)
d1.text((370, 445), "Procédure officielle Canon EOS R50 : Toujours utiliser une poire soufflante propre.", fill=TEXT_COLOR)
d1.text((370, 465), "Ne jamais utiliser de solvant agressif ni d'écouvillon non certifié. Éteindre le boîtier.", fill=TEXT_COLOR)
d1.text((370, 495), "Source : Collection Qdrant maintidoc_text · Validé RBAC", fill=MUTED)

# Result Card 2
d1.rectangle([350, 535, 1150, 675], fill=CARD_BG, outline=BORDER_COLOR)
d1.text((370, 550), "#2 — manuel_canon_r50_base p.4 [texte] · Score RRF = 0.0161", fill=(20, 50, 120))
d1.text((370, 580), "Extrait retenu :", fill=MUTED)
d1.text((370, 600), "Chapitre 4 : Entretien périodique du capteur CMOS APS-C. Activation du mode nettoyage automatique.", fill=TEXT_COLOR)
d1.text((370, 620), "En cas de tache persistante, se référer à la procédure de maintenance officielle P04.", fill=TEXT_COLOR)
d1.text((370, 650), "Source : Collection Qdrant maintidoc_text · Validé RBAC", fill=MUTED)
img1.save(OUT_DIR / "recherche_texte.png")

# 2. Recherche Photo
img2 = Image.new("RGB", (W, H), BG_COLOR)
d2 = ImageDraw.Draw(img2)
draw_base_ui(d2, "techniciens_impression", ["imprimantes_pro"], "Vérification des buses d'impression", has_photo=True)
d2.rectangle([350, 260, 480, 300], fill=PRIMARY)
d2.text((375, 272), "Rechercher", fill=(255, 255, 255))
d2.rectangle([350, 320, 1150, 360], fill=(230, 245, 230), outline=GREEN)
d2.text((365, 332), "✓ 2 résultat(s) multimodal trouvé(s) — Fusion RRF Texte + CLIP Embeddings", fill=GREEN)

# Result Card 1 (Image match)
d2.rectangle([350, 380, 1150, 530], fill=CARD_BG, outline=(100, 160, 240))
d2.text((370, 395), "#1 — mire_test_buses_nozzle_check_epson [image] · Score RRF = 0.0323", fill=(20, 50, 120))
d2.rectangle([370, 425, 480, 510], fill=(220, 230, 245), outline=BORDER_COLOR)
d2.text((385, 460), "[Mire Epson]", fill=(40, 80, 160))
d2.text((500, 430), "Type d'élément : Figure technique / Contrôle qualité visuel", fill=TEXT_COLOR)
d2.text((500, 455), "Légende : Image technique : mire test buses nozzle check epson", fill=TEXT_COLOR)
d2.text((500, 480), "Similarité visuelle CLIP : 0.894 (Correspondance directe avec la photo)", fill=GREEN)
d2.text((500, 505), "Source : Collection Qdrant maintidoc_images · Validé RBAC", fill=MUTED)

# Result Card 2 (Text context)
d2.rectangle([350, 545, 1150, 680], fill=CARD_BG, outline=BORDER_COLOR)
d2.text((370, 560), "#2 — guide_maint_tete_epson_standard p.2 [texte] · Score RRF = 0.0161", fill=(20, 50, 120))
d2.text((370, 590), "Procédure d'évaluation de la mire : des segments manquants indiquent des buses obstruées.", fill=TEXT_COLOR)
d2.text((370, 615), "Exécuter un cycle de nettoyage standard avant toute intervention mécanique sur la tête.", fill=TEXT_COLOR)
d2.text((370, 650), "Source : Collection Qdrant maintidoc_text · Validé RBAC", fill=MUTED)
img2.save(OUT_DIR / "recherche_photo.png")

# 3. Accès Refusé
img3 = Image.new("RGB", (W, H), BG_COLOR)
d3 = ImageDraw.Draw(img3)
draw_base_ui(d3, "techniciens_audiovisuel", ["appareils_photo"], "Montre-moi le rapport d'atelier Epson")
d3.rectangle([350, 260, 480, 300], fill=PRIMARY)
d3.text((375, 272), "Rechercher", fill=(255, 255, 255))

# Access Refused Alert
d3.rectangle([350, 320, 1150, 420], fill=(255, 235, 235), outline=RED, width=2)
d3.text((375, 340), "⛔ ACCÈS REFUSÉ — CONTRÔLE D'ACCÈS RBAC STRICT", fill=RED)
d3.text((375, 370), "L'utilisateur 'techniciens_audiovisuel' tente d'accéder aux documents de la famille 'imprimantes_pro'.", fill=TEXT_COLOR)
d3.text((375, 395), "Filtrage appliqué en amont (Pre-filter Qdrant) : Aucun vecteur de cette collection n'a été interrogé.", fill=TEXT_COLOR)

# RBAC Explanation Card
d3.rectangle([350, 440, 1150, 620], fill=CARD_BG, outline=BORDER_COLOR)
d3.text((370, 460), "Détails de l'application de la politique RBAC :", fill=(20, 50, 120))
d3.text((370, 495), "• Familles autorisées pour votre profil : ['appareils_photo']", fill=TEXT_COLOR)
d3.text((370, 520), "• Document ciblé : rapport_atelier_epson_p700_scan (Famille : imprimantes_pro)", fill=TEXT_COLOR)
d3.text((370, 545), "• Décision de sécurité : Rejet immédiat sans fuite de métadonnées ni de score vectoriel.", fill=RED)
d3.text((370, 580), "• Événement consigné dans le journal d'audit de sécurité MaintiDoc.", fill=MUTED)
img3.save(OUT_DIR / "acces_refuse.png")

print("✓ 3 captures générées avec succès dans eval/captures/")
