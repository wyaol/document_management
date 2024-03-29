from django.urls import path

from .api import *

urlpatterns = [
    path('test', test),
    path('ready', get_one_ready_outline),
    path('add', add_one_outline2),
    path('revert/<int:id>', revert_outline),
    # path('paragraphs', add_one_paragraph),
    path('articles', add_articles),
    # path('paragraphs/finish', finish_paragraph),
    # path('paragraphs/title', add_title),
    path('documents/down', download_document),
    path('documents/down/<str:file_name>', download_document_by_path),
    path('documents', documents),
    path('words/to/excels', words_to_excels),
]
