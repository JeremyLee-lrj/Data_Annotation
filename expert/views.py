import json

from django.http import HttpResponse
from pymilvus import (
    connections,
    Collection,
)


# Create your views here.

def get(request):
    conn = connections.connect(host="10.100.2.241", port="19530")
    collection = Collection(name="test_with_len")
    data = collection.query(expr="entry_text_len > 100",
                            output_fields=["entry_text","entry_text_len"])
    return HttpResponse(data)
