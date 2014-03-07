from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import ExampleModel

def index(request):
    example_model, created = ExampleModel.objects.get_or_create(label="sample")

    return render_to_response("index.html", { 'example_model': example_model }, context_instance=RequestContext(request))