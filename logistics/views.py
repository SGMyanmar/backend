from django.shortcuts import redirect

def redirect_swagger_view(request):
    return redirect('/api/swagger')