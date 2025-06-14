from django.http import HttpResponse, Http404
from django.shortcuts import redirect
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code == 404:
                raise Http404("Page not found")
            return response
        except Http404:
            return redirect("home")
        except Exception as e:
            return self.get_response(request)
    
    def process_exception(self, request, exception):
        return HttpResponse(f"An error occurred: {str(exception)}", status=500)

