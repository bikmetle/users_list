from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from api.v1.users.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    params:\n
    to sort by field pass field name by key `sort_by`\n
    to filter pass name as value by key `first_name` or `last_name`
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            sort_param = self.request.query_params.get('sort_by')
            first_name_param = self.request.query_params.get('first_name')
            last_name_param = self.request.query_params.get('last_name')

            if sort_param:
                queryset = queryset.order_by(sort_param)
            if first_name_param:
                queryset = queryset.filter(first_name__icontains=first_name_param)
            if last_name_param:
                queryset = queryset.filter(last_name__icontains=last_name_param)

        return queryset
    