import json
from django.http import HttpResponse
from django.shortcuts import render_to_response

from generation.models import Prime, MaxIndex


def home(request):
    return render_to_response('home.html', {'count': MaxIndex.get().index})

def get_prime(request):
    try:
        index = int(request.GET['index'])
    except:
        index = None
    return HttpResponse(json.dumps({"value": Prime.get(index)
        if index else ""}), content_type="application/json")

def primes(request):
    return HttpResponse(str(Prime.get_values()))