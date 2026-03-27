# Regenerate the PDF with an image included using reportlab

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PIL import Image as PILImage, ImageDraw

# Create a simple placeholder image
img_path = "mos.jpg"
img = PILImage.new('RGB', (400, 200), color=(200, 220, 255))
draw = ImageDraw.Draw(img)
draw.text((50, 80), "IMAGE DU CONSTAT", fill=(0, 0, 0))
img.save(img_path)

# Create PDF
doc_path = "rapport_constat_avec_image.pdf"
doc = SimpleDocTemplate(doc_path)
styles = getSampleStyleSheet()

content = []

# Title
content.append(Paragraph("RAPPORT DE CONSTAT", styles["Title"]))
content.append(Spacer(1, 12))

# Add Image
content.append(Image(img_path, width=4*inch, height=2*inch))
content.append(Spacer(1, 12))

# Sections
content.append(Paragraph("1. Introduction", styles["Heading2"]))
content.append(Paragraph(
    "Ce rapport présente un constat général basé sur l'observation d'une situation donnée.", 
    styles["Normal"]))
content.append(Spacer(1, 12))

content.append(Paragraph("2. Description du constat", styles["Heading2"]))
content.append(Paragraph(
    "Plusieurs anomalies ont été relevées, notamment un manque d'organisation.", 
    styles["Normal"]))
content.append(Spacer(1, 12))

content.append(Paragraph("3. Analyse", styles["Heading2"]))
content.append(Paragraph(
    "Les problèmes sont liés à une mauvaise planification.", 
    styles["Normal"]))
content.append(Spacer(1, 12))

content.append(Paragraph("4. Recommandations", styles["Heading2"]))
content.append(Paragraph(
    "Mettre en place un système de gestion efficace.", 
    styles["Normal"]))

doc.build(content)

doc_path