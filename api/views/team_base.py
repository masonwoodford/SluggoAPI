from rest_framework import permissions, viewsets, status, mixins, serializers, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.settings import api_settings

from ..models import Team
from ..permissions import IsAdminMemberOrReadOnly, IsOwnerOrReadOnly, IsMemberUser


class TeamRelatedViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdminMemberOrReadOnly,
        IsMemberUser,
    ]

    @staticmethod
    def get_success_headers(data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @action(
        methods=["POST"], detail=False, permission_classes=[permissions.IsAuthenticated, IsMemberUser]
    )
    def create_record(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            team = serializer.validated_data["team_id"]

            # make sure we're actually allowed to access this team
            self.check_object_permissions(request, team)
            record = serializer.save()

            serialized = self.serializer_class(record)
            return Response(serialized.data, status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            return Response({"msg": e.detail}, e.status_code)

    @action(detail=True, methods=["GET"], permission_classes=permission_classes)
    def list_team(self, request, pk=None):

        queryset = self.filter_queryset(self.get_queryset().filter(team__id=pk))
        serializer = self.serializer_class(queryset, many=True)

        team = get_object_or_404(Team, pk=pk)
        self.check_object_permissions(request, team)
        return Response(serializer.data, status.HTTP_200_OK)

    # note: this is pretty hacky
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)
