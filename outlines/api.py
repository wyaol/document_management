import json
import os
from io import BytesIO

from django.http import FileResponse
from django.http import HttpResponse
from outlines import article_management
from outlines.word_to_excel_utils import read_doc_to_data_set, get_excel_workbook, get_zip_output


def test(request):
    return HttpResponse(2)


def outlines(request):
    if request.method == 'POST':
        return add_one_outline(request)
    if request.method == 'GET':
        return get_outlines(request)
    if request.method == 'DELETE':
        return delete_outlines(request)



def add_one_outline(request):
    outline = json.loads(request.body)['outline']
    return HttpResponse(json.dumps({
        'outlines': article_management.add_one_outline(outline)
    }, default=lambda x: x.__dict__), content_type='application/json')


def get_outlines(request):
    outlines_ = article_management.get_outlines()
    return HttpResponse(json.dumps({
        'outlines': outlines_
    }, default=lambda x: x.__dict__), content_type='application/json')


def delete_outlines(request):
    outlines_ = article_management.delete_outlines()
    return HttpResponse(json.dumps({
        'outlines': outlines_
    }, default=lambda x: x.__dict__), content_type='application/json')


def get_one_ready_outline(request):
    return HttpResponse(json.dumps({
        'outline': article_management.pop_one_outline()
    }, default=lambda x: x.__dict__), content_type='application/json')


def revert_outline(request, id):
    return HttpResponse(json.dumps({
        'outlines': article_management.revert_outline(id)
    }, default=lambda x: x.__dict__), content_type='application/json')


def add_one_paragraph(request):
    conversation_id = json.loads(request.body)['conversation_id']
    paragraph = json.loads(request.body)['paragraph']
    article_management.add_one_paragraph(conversation_id, paragraph)
    return HttpResponse(json.dumps({
        'status': 'ok'
    }, default=lambda x: x.__dict__), content_type='application/json')


def add_title(request):
    conversation_id = json.loads(request.body)['conversation_id']
    title = json.loads(request.body)['title']
    article_management.add_title(conversation_id, title)
    return HttpResponse(json.dumps({
        'status': 'ok'
    }, default=lambda x: x.__dict__), content_type='application/json')


def finish_paragraph(request):
    conversation_id = json.loads(request.body)['conversation_id']
    article_management.finish_one_connector(conversation_id)
    return HttpResponse(json.dumps({
        'status': 'ok'
    }, default=lambda x: x.__dict__), content_type='application/json')


def download_document(request):
    file_name = json.loads(request.body)['file_name']
    file = open('output/%s' % file_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response['Content-Disposition'] = 'attachment;filename= ' + '文件'.encode('utf-8').decode('ISO-8859-1') + '.docx'
    return response


def download_document_by_path(request, file_name):
    file = open('output/%s' % file_name, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response['Content-Disposition'] = 'attachment;filename= ' + file_name.encode('utf-8').decode('ISO-8859-1')
    return response


def documents(request):
    if request.method == 'GET':
        return get_documents(request)
    if request.method == 'DELETE':
        return delete_documents(request)


def delete_documents(request):
    article_management.delete_documents()
    return HttpResponse(json.dumps({
        'files': os.listdir('output')
    }, default=lambda x: x.__dict__), content_type='application/json')


def get_documents(request):
    return HttpResponse(json.dumps({
        'files': ['https://123.207.27.133:5001/outlines/documents/down/' + item for item in os.listdir('output')]
    }, default=lambda x: x.__dict__), content_type='application/json')


def add_articles(request):
    paragraphs = json.loads(request.body)['paragraphs']
    article_management.add_articles(paragraphs)
    return HttpResponse(json.dumps({
        'status': 'ok'
    }, default=lambda x: x.__dict__), content_type='application/json')


def words_to_excels(request):
    if 'words' not in request.FILES:
        return HttpResponse("No file uploaded")
    file_streams = request.FILES.getlist('words')

    workbook_objs = []
    for file_stream in file_streams:
        data_set = read_doc_to_data_set(bytes(file_stream.read()))
        workbook_obj = get_excel_workbook(data_set, file_stream.name)
        workbook_objs.append(workbook_obj)

    output = get_zip_output(workbook_objs)
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="excels.zip"'

    return response
