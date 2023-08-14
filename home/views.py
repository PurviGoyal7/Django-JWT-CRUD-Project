from django.http import HttpResponse

# Create your views here.
def health(request):
    return HttpResponse("OK")
    

