import json

from django.http import HttpResponse

from outlines import article_management


def test(request):
    return HttpResponse(2)


def outlines(request):
    if request.method == 'POST':
        return add_one_outline(request)
    if request.method == 'GET':
        return get_outlines(request)


def add_one_outline(request):
    outline = request.json['outline']
    return HttpResponse(json.dumps({
        'outlines': article_management.add_one_outline(outline)
    }, default=lambda x: x.__dict__), content_type='application/json')


def get_outlines(request):
    outlines_ = article_management.get_outlines()
    return HttpResponse(json.dumps({
        'outlines': outlines_
    }, default=lambda x: x.__dict__), content_type='application/json')


def get_one_ready_outline(request):
    return HttpResponse(json.dumps({
        'outline': article_management.pop_one_outline()
    }, default=lambda x: x.__dict__), content_type='application/json')
