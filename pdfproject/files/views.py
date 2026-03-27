from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from pathlib import Path
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def home(request):
    return render(request, 'files/home.html')

def view_pdf(request):
    # Définir le dossier MEDIA
    base_path = Path(settings.MEDIA_ROOT)
    base_path.mkdir(exist_ok=True)

    # Nom du fichier
    file_name = "rapport_constat_avec_image.pdf"
    file_path = base_path / file_name

    # Si le fichier existe déjà, créer un nouveau nom
    if file_path.exists():
        file_path = base_path / "rapport_constat_avec_image_new.pdf"

    # Génération du PDF
    try:
        doc = SimpleDocTemplate(str(file_path))
        styles = getSampleStyleSheet()

        content = []

        # Titre
        content.append(Paragraph("RAPPORT DE CONSTAT", styles["Title"]))
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

    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération du PDF : {e}")

    # Action utilisateur
    action = request.GET.get("action")

    try:
        if action == "download":
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        else:
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

    except FileNotFoundError:
        return HttpResponse("Fichier introuvable")