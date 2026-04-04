from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.mixins import PageTitleMixin
from store.models import Store
from store.serializers import StoreSerializer


# Create your views here.
from rest_framework.permissions import BasePermission

class StoreCRUPPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in ['GET']:
            return user.has_perm('store.view_store')
        elif request.method in ['POST']:
            return user.has_perm('store.add_store')
        elif request.method in ['PUT', 'PATCH']:
            return user.has_perm('store.change_store')
        elif request.method == 'DELETE':
            return user.has_perm('store.delete_store')
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class ListStoreView(APIView):
    permission_classes = [StoreCRUPPermissions]
    def get(self, request: Request) -> Response:
        cars = Store.objects.all()
        serializer = StoreSerializer(cars, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailStoreView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [StoreCRUPPermissions]


class StorePageView(UserPassesTestMixin, PageTitleMixin, TemplateView):
    template_name = 'store/store_page.html'
    page_title = 'Store management'

    def test_func(self):
        user = self.request.user
        return (user.has_perm('store.add_store')
                or user.has_perm('store.change_store')
                or user.has_perm('store.delete_store')
                or user.has_perm('store.view_store')
                or user.is_staff)
