from django.http import HttpResponseNotFound
from django.shortcuts import redirect

from mainsite.models import Product


def delete(request, pk):
    if request.method == 'GET':
        user_id = request.user.id
        to_delete = Product.objects.get(pk=pk)
        if to_delete.owner_id == user_id or request.user.is_superuser:
            to_delete.delete()
            return redirect('index')
        else:
            return HttpResponseNotFound('<h1>Access denied<h1>')