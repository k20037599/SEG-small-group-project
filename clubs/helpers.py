from django.shortcuts import redirect
from django.conf import settings


def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function


class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
