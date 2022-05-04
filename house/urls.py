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
import os

from django.contrib import admin
from django.urls import include, path, re_path

from house.core.views import (
    Alarms,
    Boiler,
    ControllerView,
    Info,
    Light,
    Printer,
    Rele,
    ResetArduino,
    RestartCam,
    Temp,
    RefreshTestDiagram,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", ControllerView.as_view(), name="form"),
    path("restart/", RestartCam.as_view(), name="restart_cam"),
    path("temp/", Temp.as_view(), name="temp"),
    path("reset_arduino/", ResetArduino.as_view(), name="reset_arduino"),
    path("boiler/", Boiler.as_view(), name="boiler"),
    path("printer/", Printer.as_view(), name="printer"),
    path("light/", Light.as_view(), name="light"),
    re_path(r"^rele/([1-9])/$", Rele.as_view(), name="rele"),
    path("test/", include("house.core.tests_urls")),
    path("poliv/", include("house.core.poliv_urls")),
    path("alarms/", Alarms.as_view(), name="alarms"),
    path("solnce/", include("house.core.solnce_urls")),
    path("info/", Info.as_view(), name="info"),
    path("info/refresh/", RefreshTestDiagram.as_view(), name="refresh")
]
