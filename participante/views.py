from django.shortcuts import render
from .models import Participante

# PARTICIPANTE
def participante(request):
    participantes = Participante.objects.all()
    return render(request, "index.html", {"participantes": participantes})
