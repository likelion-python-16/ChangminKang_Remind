from django.urls import path, include  # Django의 URL 라우팅을 위한 모듈을 가져옵니다.
from rest_framework.routers import DefaultRouter  # Django REST Framework의 기본 라우터를 가져옵니다.
from .api_views import LikeViewSet, BookmarkViewSet, CommentViewSet, CommentLikeViewSet  # api_views.py에서 LikeViewSet을 가져옵니다. 이 ViewSet은 좋아요 기능을 처리합니다.
from .views import todo_detail_with_interaction  # views.py에서 todo_detail_with_interaction 뷰를 가져옵니다. 이 뷰는 특정 Todo 항목의 상세 정보와 상호작용을 보여줍니다.

router = DefaultRouter()  # Django REST Framework의 기본 라우터를 사용합니다.
router.register(r"likes", LikeViewSet, basename='likes')
router.register(r"bookmarks", BookmarkViewSet, basename='bookmarks')
router.register(r"comments", CommentViewSet, basename='comments')
router.register(r"commentlikes", CommentLikeViewSet, basename='commentlikes')  # CommentViewSet을 'commentlikes'로 등록합니다. // 이 ViewSet은 댓글에 대한 좋아요 기능을 처리합니다. // 'basename'은 URL 네임스페이스를 지정하는 데 사용됩니다. // 예를 들어, 'interaction:commentlikes-list'와 같은 URL 네임스페이스를 생성합니다.
#r은 주소의 마지막을 표시한 것이며 규칙이 아닌 관습

app_name = "interaction"  # 앱 이름을 설정합니다. 이 이름은 URL 네임스페이스로 사용됩니다.

urlpatterns = [
    path("", include(router.urls)),  
    path('todo/detail/<int:pk>/', todo_detail_with_interaction, name='todo_detail'),
]  # URL 패턴을 정의하는 리스트입니다.
