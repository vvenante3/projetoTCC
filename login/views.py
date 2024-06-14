from django.shortcuts import render, redirect

# LOGIN
def pagina_login(request):
    return render(request, 'login/login.html')