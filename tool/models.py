from django.db import models


class SessionDBConfiguration(models.Model):
    """Should have one entry per session per user"""
    session_key = models.CharField(max_length=50, null=True, db_index=True)
    db_config = models.JSONField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class NaturalQuery(models.Model):
    session_key = models.ForeignKey(SessionDBConfiguration, null=True, on_delete=models.SET_NULL)
    nl_query = models.TextField(null=True)
    sql_query = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
