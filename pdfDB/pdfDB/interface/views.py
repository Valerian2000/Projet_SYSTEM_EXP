from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from django.shortcuts import render, redirect
from .models import Etudiant

from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from pathlib import Path
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


from django.shortcuts import render
from .models import Etudiant
from .forms import EtudiantFilterForm


from django.db.models import Avg

def formulaire(request):
    if request.method == "POST":
        Etudiant.objects.create(
            annee=request.POST['annee'],
            ecole=request.POST['ecole'],
            classe=request.POST['classe'],
            eleve=request.POST['eleve'],
            pourcentage=request.POST['pourcentage']
            )
        return redirect('liste')

    return render(request, 'html/form.html')





def liste(request):
    global data
    data = Etudiant.objects.all()
    form = EtudiantFilterForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data.get('annee'):
            data = data.filter(annee__icontains=form.cleaned_data['annee'])

        if form.cleaned_data.get('ecole'):
            data = data.filter(ecole__icontains=form.cleaned_data['ecole'])

        if form.cleaned_data.get('classe'):
            data = data.filter(classe__icontains=form.cleaned_data['classe'])

        if form.cleaned_data.get('eleve'):
            data = data.filter(eleve__icontains=form.cleaned_data['eleve'])

        if form.cleaned_data.get('pourcentage'):
            data = data.filter(pourcentage__icontains=form.cleaned_data['pourcentage'])

    return render(request, 'html/list.html', {
        'data': data,
        'form': form
    })

    

def generate_pdf(request):
    #Dossier MEDIA
    base_path = Path(settings.MEDIA_ROOT)
    base_path.mkdir(exist_ok=True)

    # Nom du fichier
    file_name = "rapport_constat_avec_image.pdf"
    file_path = base_path / file_name

    # Si existe déjà
    if file_path.exists():
        file_path = base_path / "rapport_constat_avec_image_new.pdf"

    try:

        html_string = render_to_string("html/pdf_template.html", {
            'students': data,
            'moyenne': data.aggregate(average=Avg('pourcentage'))['average']
        })

        # Générer ET enregistrer le PDF dans le fichier
        HTML(
            string=html_string,
            base_url=request.build_absolute_uri("/")
        ).write_pdf(target=str(file_path))

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

