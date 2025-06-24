from django.urls import path, include
from . import views
from . import api_views

urlpatterns = [
    # path("list/", views.todo_list, name = "todo_List" ), #list 목록보기 / name은 프로젝트 url 속 redirect name (함수형)

    path("list/", views.TodoListViews.as_view(), name="todo_List"), # list 목록보기 (위와 같고 class형)_template view 
    path("create/", views.TodoCreateViews.as_view(), name= "todo_Create"),
    path("detail/<int:pk>/", views.TodoDetailViews.as_view(), name= "todo_Detail"), # detail은 pk를 받아서 특정 항목을 보여주기 때문에 <int:pk>로 설정
    path("update/<int:pk>/", views.TodoUpdateViews.as_view(), name= "todo_Update"), # update는 pk를 받아서 수정하기 때문에 <int:pk>로 설정
    # path("delete/<int:pk>/", views.TodoDeleteViews.as_view(), name= "todo_Delete"), # delete는 pk를 받아서 삭제하기 때문에 <int:pk>로 설정

    path("api/list/",api_views.TodoListAPI.as_view(), name = "todo_api_list"),  #apiViews 속 TodoListAPI.as_view()로 연결
    path("api/create/", api_views.TodoCreateAPI.as_view(), name= "todo_api_create"), # apiViews 속 TodoCreateAPI.as_view()로 연결
    path("api/retrieve/<int:pk>/", api_views.TodoRetrieveAPI.as_view(), name= "todo_api_retrieve"),  #apiViews 속 TodoRetrieveAPI.as_view()로 연결
    path("api/update/<int:pk>/", api_views.TodoUpdateAPI.as_view(), name= "todo_api_update"),  #apiViews 속 TodoUpdateAPI.as_view()로 연결
    path("api/delete/<int:pk>/", api_views.TodoDeleteAPI.as_view(), name= "todo_api_delete"),  #apiViews 속 TodoDeleteAPI.as_view()로 연결
]