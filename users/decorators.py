from django.http import HttpResponseForbidden

# Decorator to check if the user is an author or not
def author_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_role') != 'author':
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
