from django.urls import path, include
from . import views
from . import api_views 
from .api_views import  TodoGenericsListAPI, TodoGenericsCreateAPI, TodoGenericsRetrieveAPI, TodoGenericsUpdateAPI, TodoGenericsDeleteAPI, TodoGenericsRetrieveUpdateDeleteAPI, TodoGenericsListCreateAPI, CustomLogoutApi
# import *는  모든 것을 가져온다는 의미(비추천) / genericview가 아닌  apiview를 쓴 이유는 apiview 안에 gernericapiview가 포함

#viewsets
from rest_framework.routers import DefaultRouter  # DRF의 DefaultRouter를 사용하여 viewsets를 위한 라우터를 생성합니다.
from .api_views import TodoViewSet  # api_views.py에서 TodoViewSet을 가져옵니다.
#viewsets (api_views.py 작성 전 urls.py 작성 필수)
router = DefaultRouter()  # DRF의 DefaultRouter를 사용하여 viewsets를 위한 라우터 생성
router.register(r"view", TodoViewSet, basename='todo')  # TodoViewSet을 등록합니다. basename은 URL의 접두사 역할을 합니다. r"view"는 URL의 접두사로 사용됩니다. 이 URL은 /todo/viewsets/view/로 매핑됩니다. view가 마지막이다 더이상 없다. view/는 뒤에 더 있을 수도 있다.

app_name = "todo"  # 앱 이름을 설정합니다. 이 이름은 URL 네임스페이스로 사용됩니다.

urlpatterns = [
    # path("list/", views.todo_list, name = "todo_List" ), #list 목록보기 / name은 프로젝트 url 속 redirect name (함수형)

    path("list/", views.TodoListViews.as_view(), name="todo_List"), # list 목록보기 (위와 같고 class형)_template view 
    path("create/", views.TodoCreateViews.as_view(), name= "todo_Create"),
    path("detail/<int:pk>/", views.TodoDetailViews.as_view(), name= "todo_Detail"), # detail은 pk를 받아서 특정 항목을 보여주기 때문에 <int:pk>로 설정
    path("update/<int:pk>/", views.TodoUpdateViews.as_view(), name= "todo_Update"), # update는 pk를 받아서 수정하기 때문에 <int:pk>로 설정
    # path("delete/<int:pk>/", views.TodoDeleteViews.as_view(), name= "todo_Delete"), # delete는 pk를 받아서 삭제하기 때문에 <int:pk>로 설정


    # API URL 패턴
    # api_views.py에서 작성한 APIViews를 연결합니다.
    path("api/list/",api_views.TodoListAPI.as_view(), name = "todo_api_list"),  #apiViews 속 TodoListAPI.as_view()로 연결
    path("api/create/", api_views.TodoCreateAPI.as_view(), name= "todo_api_create"), # apiViews 속 TodoCreateAPI.as_view()로 연결
    path("api/retrieve/<int:pk>/", api_views.TodoRetrieveAPI.as_view(), name= "todo_api_retrieve"),  #apiViews 속 TodoRetrieveAPI.as_view()로 연결
    path("api/update/<int:pk>/", api_views.TodoUpdateAPI.as_view(), name= "todo_api_update"),  #apiViews 속 TodoUpdateAPI.as_view()로 연결
    path("api/delete/<int:pk>/", api_views.TodoDeleteAPI.as_view(), name= "todo_api_delete"),  #apiViews 속 TodoDeleteAPI.as_view()로 연결

    # GenericAPIView  위에는 api_views. 을 붙여야 하는데, 아래는 api_views를 import 했기 때문에 붙이지 않아도 됨 // api_views.py에서 작성한 GenericAPIView를 연결했어서 앞에 generics. 안 붙여도 됌
    path("generics/list/", TodoGenericsListAPI.as_view(), name="todo_generics_list"),  # Generics List API
    path("generics/create/", TodoGenericsCreateAPI.as_view(), name="todo_generics_create"),  # Generics Create API
    path("generics/retrieve/<int:pk>/", TodoGenericsRetrieveAPI.as_view(), name="todo_generics_retrieve"),  # Generics Retrieve API
    path("generics/update/<int:pk>/", TodoGenericsUpdateAPI.as_view(), name="todo_generics_update"),  # Generics Update API
    path("generics/delete/<int:pk>/", TodoGenericsDeleteAPI.as_view(), name="todo_generics_delete"),
    #GenericAPIView + Mixin
    path("generics/<int:pk>/", TodoGenericsRetrieveUpdateDeleteAPI.as_view(), name="todo_generics_retrieve_update_delete"),  # Generics Retrieve, Update, Delete API
    path("generics/", TodoGenericsListCreateAPI.as_view(), name="todo_generics_retrieve_update"),  # Generics Retrieve, Update API

    # ViewSets URL 패턴
    path("viewsets/", include(router.urls)), #/todo/viewsets/view/  // viewsets를 위한 URL 패턴을 포함합니다. 이 URL 패턴은 TodoViewSet에 의해 처리됩니다.
      # todo/viewsets/view/  // viewsets를 위한 URL 패턴을 추가합니다. viewsets는 CRUD 작업을 모두 처리할 수 있는 강력한 기능을 제공합니다.

    #logout
    path("api/custom-logout/", CustomLogoutApi.as_view() , name="custom-logout"),  # CustomLogoutApi를 사용하여 로그아웃 기능을 구현합니다.
]

