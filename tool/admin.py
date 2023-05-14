from django.contrib import admin
from tool.models import SessionDBConfiguration, NaturalQuery


@admin.register(SessionDBConfiguration)
class SessionDBConfigurationAdmin(admin.ModelAdmin):
    list_display = ["session_key", "db_config"]


@admin.register(NaturalQuery)
class NaturalQueryAdmin(admin.ModelAdmin):
    list_display = ["nl_query", "sql_query"]
