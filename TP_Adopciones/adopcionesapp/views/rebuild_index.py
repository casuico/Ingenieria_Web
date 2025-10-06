from django.views import View

def rebuild_index(request):
    from django.core.management import call_command
    from django.http import JsonResponse
    try:
        call_command('rebuild_index', noinput=False)
        result = "Rebuilded index"
    except Exception as err:
        result = f"Error: {err}"

    return JsonResponse({"result": result})
    