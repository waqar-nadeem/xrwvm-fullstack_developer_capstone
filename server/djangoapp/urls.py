# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views # <--- UNCOMMENTED

app_name = 'djangoapp'
urlpatterns = [
 # # path for registration

 # path for login
 # path(route='login', view=views.login_user, name='login'),

    # Path for get_cars view
    path(route='get_cars', view=views.get_cars, name ='getcars'), # <--- ADDED

 # path for dealer reviews view

 # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   