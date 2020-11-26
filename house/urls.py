"""
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from house.core.views import ControllerView, RestartCam, Temp, ResetArduino, \
    Boiler, Rele



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', ControllerView.as_view(), name='form'),
    url(r'^restart/$', RestartCam.as_view(), name='restart_cam'),
    url(r'^temp/$', Temp.as_view(), name = 'temp'),
    url(r'^reset_arduino/$', ResetArduino.as_view(), name = 'reset_arduino'),
    url(r'^boiler/$', Boiler.as_view(), name = 'boiler'),

    url(r'^rele/([1-9])/$', Rele.as_view(), name = 'rele'),
    url(r'^test/', include('house.core.test_urls')),

    ]
