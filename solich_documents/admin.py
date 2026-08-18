from django.contrib import admin

from solich_documents.models import Document, DocumentRequest

# Register your models here.
admin.site.register(Document)
admin.site.register(DocumentRequest)
