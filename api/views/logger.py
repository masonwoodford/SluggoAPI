from django.db import models
from .team import Team
from .ticket import Ticket

class Logger(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='tag_list')
    edited = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["id"]
        app_label = "api"