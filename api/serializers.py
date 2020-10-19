"""
A REST API needs to provide a way of serializing and deserializing the models created into representations such as json.
We can do this by declaring serializers that work very similar to Django's forms. Create a file in the app directory
named serializers.py and create your classes.
"""
from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework.utils import model_meta

from django.conf import settings
from . import models as api_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "first_name", "last_name"]


class TeamSerializer(serializers.ModelSerializer):

    # make the following fields read only
    id = serializers.ReadOnlyField()
    ticket_head = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()
    activated = serializers.ReadOnlyField()
    deactivated = serializers.ReadOnlyField()

    class Meta:
        model = api_models.Team
        fields = [
            "id",
            "name",
            "description",
            "ticket_head",
            "created",
            "activated",
            "deactivated",
        ]


class MemberSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    owner = UserSerializer(many=False, read_only=True)
    team_id = serializers.ReadOnlyField(source="team.id")
    created = serializers.ReadOnlyField()
    activated = serializers.ReadOnlyField()
    deactivated = serializers.ReadOnlyField()

    class Meta:
        model = api_models.Member
        fields = [
            "id",
            "owner",
            "team_id",
            "role",
            "bio",
            "created",
            "activated",
            "deactivated",
        ]


class TicketCommentSerializer(serializers.ModelSerializer):
    """
    Serialzier for comments. to be used with tickets
    """

    class Meta:
        model = api_models.TicketComment
        ticket_id = serializers.ReadOnlyField(source="ticket.id")
        team_id = serializers.ReadOnlyField(source="team.id")
        owner = UserSerializer(many=False, read_only=True)

        fields = [
            "id",
            "ticket_id",
            "team_id",
            "owner",
            "content",
            "created",
            "activated",
            "deactivated",
        ]


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer Class for the Ticket model.

    The fields that are serialized and visible currently are:
        id: The id of the Ticket
        team_id: id of owner team
        owner: The user that created the ticket
        assigned_user: The user assigned to the ticket
        title: The title of the ticket
        description: The description of the ticket
        comments: The comments associated with this ticket
        started: When the ticket was started
        completed: When the ticket was finished
        due_date: When the ticket is due
    """

    team_id = serializers.ReadOnlyField(source="team.id")
    owner = serializers.ReadOnlyField(source="owner.email")
    comments = TicketCommentSerializer(many=True, required=False)
    assigned_user = UserSerializer(read_only=False)

    class Meta:
        model = api_models.Ticket
        fields = [
            "id",
            "team_id",
            "ticket_number",
            "owner",
            "assigned_user",
            "title",
            "description",
            "comments",
            "activated",
            "deactivated",
        ]


class TicketStatusSerializer(serializers.ModelSerializer):
    team_id = serializers.ReadOnlyField(source="team.id")

    class Meta:
        model = api_models.TicketStatus
        fields = ["id", "team_id", "title", "created", "activated", "deactivated"]
