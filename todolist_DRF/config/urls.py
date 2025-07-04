"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include(('todo.urls', 'todo'), namespace='todo')), # url 주소는 앱이름과 같아야 한다.
    path('', lambda request: redirect("todo:todo_List")), #127.0.0.1:8000/todo/list로 바로 가짐 / todo_List는 todo URL 과 연결 / redirect(reverse("todo_List"))도 이 역할을 함
    #reverse("todo_List"): URL name을 실제 경로 문자열로 바꿈 (예: "/todo/") 그 결과를 redirect()에 넘김 → 더 명시적이고 안전함 (예: URL name이 없으면 에러 발생해서 바로 알 수 있음)
    #path('', lambda request: redirect("todo_List")): redirect(...)는 내부적으로 "todo_List"가 URL name인지 확인해서 자동으로 reverse("todo_List")를 호출 → 편리하긴 하지만, 실수해도 바로 에러가 안 나고, 문자열을 경로로 착각하거나 "todo_List"가 실제 경로라고 오해할 수 있음.
    path("api-auth/",include('rest_framework.urls')), # DRF의 인증 시스템을 사용하기 위한 URL 설정 (로그인, 로그아웃 등)
    path("accounts/", include("django.contrib.auth.urls")), # Django의 기본 인증 시스템을 사용하기 위한 URL 설정 (로그인, 로그아웃 등)
    # 배포용
    path("api/interaction/", include("interaction.urls")), # 상호작용 관련 URL 설정 (좋아요, 북마크, 댓글 등)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # MEDIA_URL과 MEDIA_ROOT를 사용하여 미디어 파일을 제공하는 URL 설정



