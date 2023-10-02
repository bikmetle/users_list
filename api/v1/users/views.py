from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from api.v1.users.serializers import UserSerializer
from django_filters import rest_framework as filters


class UserModelFilter(filters.FilterSet):
    sort_by_field = filters.CharFilter(method='sort_by_filter')
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'sort_by_field')

    def sort_by_filter(self, queryset, name, value):
        return queryset.order_by(value)

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = UserModelFilter
