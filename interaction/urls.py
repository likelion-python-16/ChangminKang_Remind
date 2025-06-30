from django.urls import path, include  # Django의 URL 라우팅을 위한 모듈을 가져옵니다.
from rest_framework.routers import DefaultRouter  # Django REST Framework의 기본 라우터를 가져옵니다.
from .api_views import LikeViewSet, BookmarkViewSet, CommentViewSet  # api_views.py에서 LikeViewSet을 가져옵니다. 이 ViewSet은 좋아요 기능을 처리합니다.

router = DefaultRouter()  # Django REST Framework의 기본 라우터를 사용합니다.
router.register(r"likes", LikeViewSet, basename='likes')
router.register(r"bookmarks", BookmarkViewSet, basename='bookmarks')
router.register(r"comments", CommentViewSet, basename='comments')
#r은 주소의 마지막을 표시한 것이며 규칙이 아닌 관습

app_name = "interaction"  # 앱 이름을 설정합니다. 이 이름은 URL 네임스페이스로 사용됩니다.

urlpatterns = [
    path("", include(router.urls)),  
]  # URL 패턴을 정의하는 리스트입니다.
