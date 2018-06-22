from django.urls import include, path

urlpatterns = [
	path('another_tutorial/', include('another_tutorial.urls')),
]