from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tool.models import SessionDBConfiguration
from tool import services


@require_http_methods(["GET"])
def config_page_view(request):
    if not request.session.session_key:
        request.session.save()
    return render(request, template_name='tool/config-page.html')


@require_http_methods(["GET"])
def query_page_view(request):
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    if not SessionDBConfiguration.objects.filter(session_key=session_key).exists():
        return HttpResponseRedirect(reverse('tool-home'))
    return render(request, template_name="tool/nl-query.html")


@api_view(['POST'])
def configure_db(request):
    payload = request.data
    selected_tables = payload.get('selected_db_tables')
    if selected_tables:
        SessionDBConfiguration.objects.update_or_create(session_key=request.session.session_key, defaults={
            'db_config': {
                'db_url': payload['db_url'],
                'selected_tables': selected_tables
            }
        })
        return Response(status=status.HTTP_200_OK, data={'config_success': True})
    return Response(status=status.HTTP_200_OK, data=services.fetch_db_tables_from_url_postgres(payload))


@api_view(['POST'])
def run_natural_language_with_chain(request):
    config = services.get_db_configuration(request.session.session_key)
    payload = request.data
    response = services.langchain_sql_chain(config, payload['query'])
    return Response(status=status.HTTP_200_OK, data=response)


@api_view(['POST'])
def run_natural_language_with_agent(request):
    config = services.get_db_configuration(request.session.session_key)
    payload = request.data
    response = services.langchain_sql_agent(config, payload['query'])
    return Response(status=status.HTTP_200_OK, data=response)
