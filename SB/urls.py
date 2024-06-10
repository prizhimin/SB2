from django.contrib import admin
from django.urls import path, reverse_lazy, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('dashboard')), name='home'),
    path('admin/', admin.site.urls),
    path('daily/', include('daily.urls')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('general_weekly/', include('general_weekly.urls')),
    path('sixmonths2024/', include('sixmonths2024.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
