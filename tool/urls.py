from django.urls import path

from tool import views

app_name = "tool"

urlpatterns = [
    # views
    path('query', views.query_page_view, name='tool-query'),

    # apis
    path('api/v1/configure', views.configure_db, name='api-v1-configure'),
    path('api/v1/query', views.run_natural_language_with_chain, name='api-v1-query'),
    path('api/v1/query-agent', views.run_natural_language_with_agent, name='api-v1-query-agent')
]
