from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache

from .models import ExampleModel

@never_cache
def index(request):
    example_model, created = ExampleModel.objects.get_or_create(label="sample")

    return render_to_response("index.html", { 'example_model': example_model }, context_instance=RequestContext(request))