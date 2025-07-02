from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import filters # 필터링 백엔드 설정 (예: DjangoFilterBackend, SearchFilter 등) // 필터링 백엔드는 API 요청에 대한 필터링을 처리하는 클래스입니다.

#이미지 추가
from rest_framework.parsers import MultiPartParser, FormParser # 파일 업로드를 위한 파서 클래스 (파일 업로드가 필요한 경우에만 사용)

#전체 목록보기
class TodoListAPI(APIView):
    def get(self, request):
        todos = Todo.objects.all() # views 속 todos는 별개의 것 (거기 todos는 template 전용이고 여긴 api 뷰 전용, 역할이 같아 이름만 같게)
        serializer = TodoSerializer(todos, many = True)
        return Response(serializer.data) # .data 는 테이블 속 일반 json 데이터 .data 가 늘어날수록 평탄화 과정
    
#평탄화: 복잡한 Django 모델 인스턴스나 쿼리셋을 → JSON 형태의 딕셔너리로 바꾸는 과정
# 예시 1: 모델 인스턴스 (Todo)
# python
# 복사
# 편집
# todo = Todo(
#     name="공부하기",
#     description="DRF 복습",
#     complete=False,
#     exp=10
# )
# 이건 Python 객체이고, 템플릿이나 API에 그대로 보내면 브라우저가 해석할 수 없습니다.

#평탄화를 하면 
# {
#   "id": 1,
#   "name": "공부하기",
#   "description": "DRF 복습",
#   "complete": false,
#   "exp": 10,
#   "created_at": "2025-06-19T15:30:00Z"
# }

# 이렇게 평탄한 JSON 구조로 바뀝니다.
# 여기서 "평탄하다"는 의미는:

# 중첩된 구조가 없고 (예: 안에 다른 모델이 또 안 들어가 있음)

# 딱딱 키-값 쌍으로 정리되어 있음 (예: "name": "공부하기")

# 예시 2: 중첩된 모델 (예: Todo 안에 User 정보가 있을 때)
# models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Todo(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     complete = models.BooleanField(default=False)
#     exp = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ 중첩관계

# 이걸 그냥 serializer.data로 보낸다면?
# todos = Todo.objects.all()
# serializer = TodoSerializer(todos, many=True)
# print(serializer.data)
# 결과
# [
#   {
#     "id": 1,
#     "name": "Django 공부",
#     "description": "모델링 복습하기",
#     "complete": false,
#     "exp": 20,
#     "user": 3  // ForeignKey라 ID만 나감!
#   }
# ]

#중첩구조로 확장한다면 
# serializers.py
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Todo

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']  # 평탄화 수준 선택 가능

# class TodoSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)  # ✅ 중첩 serializer 명시

#     class Meta:
#         model = Todo
#         fields = '__all__'
# 위 코드로 하면 
# [
#   {
#     "id": 1,
#     "name": "Django 공부",
#     "description": "모델링 복습하기",
#     "complete": false,
#     "exp": 20,
#     "user": {
#       "id": 3,
#       "username": "chriskang",
#       "email": "chriskang@example.com"
#     }
#   }
# ]

class TodoCreateAPI(APIView):

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        todo = serializer.save()
        return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED) 
    
class TodoRetrieveAPI(APIView):
    def get(self, request, pk):
        # data 중에 삭제된 내용이 있다면 부르지 않도록 try except
        try:
            todo = Todo.objects.get(pk=pk) #model Todo에서 pk로 가져옴
        except Todo.DoesNotExist:
            return Response({"Error":"해당 Todo가 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(todo) #todo는 어디서 가져온 것인가? Todo 모델에서 가져온 것 / Serializer는 뭐지? # Todo 모델을 평탄화해서 JSON 형태로 바꿔주는 역할
        return Response(serializer.data)
    
class TodoUpdateAPI(APIView):
    def put(self, request, pk): #put은 전체 업데이트를 위한 메소드로, 모든 필드를 포함한 데이터를 보내야 합니다.
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"Error":"해당 Todo가 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True) #유효성 검사
        todo = serializer.save() #save는 저장하는 메소드
        serializer = TodoSerializer(todo)
        # serializer.save()는 수정된 데이터를 저장하고, 다시 serializer를 통해 평탄화
        return Response(serializer.data)
        
    def patch(self, request, pk): 
        # patch는 부분 업데이트를 위한 메소드로, 전체 데이터를 보내지 않고 일부만 수정할 때 사용
        # 예를 들어, 완료 상태만 변경하고 싶을 때 유용
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"Error":"해당 Todo가 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data) # Todo 모델 인스턴스와 요청 데이터를 기반으로 serializer를 생성
        # data=request.data 는 요청에서 받은 데이터를 serializer에 전달
        # 이때 request.data는 JSON 형태로 전달된 데이터입니다. 
        # serializer는 이 데이터를 Todo 모델에 맞게 변환합니다.
        # 예를 들어, {"name": "새로운 이름"} 이라면, Todo 모델의 name 필드만 업데이트합니다.
        # 만약 name 필드만 보내면, 나머지 필드는 그대로 유지됩니다
        # Serializer는 우리가 Django에서 사용하는 파이썬 객체나 쿼리셋 같이 복잡한 객체들을 Rest API에서 사용할 간단한 JSON 형태로 변환해주는 어댑터
        serializer.is_valid(raise_exception=True) #유효성 검사
        if not serializer.is_valid():
            print("유효성 검사 실패:", serializer.errors)
        todo = serializer.save() #save는 저장하는 메소드
        serializer = TodoSerializer(todo)
        # serializer.save()는 수정된 데이터를 저장하고, 다시 serializer를 통해 평탄화
        return Response(serializer.data)

#삭제하기
class TodoDeleteAPI(APIView): # 인증이 필요 없는 API로 설정
    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"Error":"해당 Todo가 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) #204는 성공적으로 삭제되었음을 나타내는 HTTP 상태 코드입니다. 
        # 이 코드는 클라이언트에게 요청이 성공적으로 처리되었지만, 반환할 데이터가 없음을 의미합니다.
        # 예를 들어, Todo를 삭제한 후에는 더 이상 해당 Todo에 대한 데이터를 반환할 필요가 없으므로, 빈 응답을 보내는 것입니다.


#DRF _ GenericAPIView (DRF GenericAPIView는 Django REST Framework에서 제공하는 클래스 기반 뷰로, CRUD(Create, Read, Update, Delete) 작업을 쉽게 구현할 수 있도록 도와줍니다.)
#Django의 generic views와 유사하게, DRF의 GenericAPIView는 기본적인 CRUD 작업을 위한 뷰를 제공합니다.
# 이 GenericAPIView는 Django의 기본 View를 상속받아, RESTful API를 구현할 때 자주 사용되는 기본적인 동작을 제공합니다.
# 예를 들어, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView 등 다양한 GenericAPIView가 제공되어
# 각각의 작업에 맞는 API를 쉽게 만들 수 있습니다.
# 이 GenericAPIView를 사용하면, 코드의 중복을 줄이고, 더 간결하고 유지보수가 쉬운 API를 만들 수 있습니다.
from rest_framework import generics

#- list

class TodoGenericsListAPI(generics.ListAPIView):
    queryset = Todo.objects.all()  # 전체 Todo 목록을 가져오는 쿼리셋 (모델 속 데이터 모두 가져옴) // queryset은 데이터베이스에서 가져올 데이터를 정의하는 부분
    serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정 // 직렬화 클래스는 모델 데이터를 JSON 형태로 변환하는 역할을 합니다.

#- create  

class TodoGenericsCreateAPI(generics.CreateAPIView):
     serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정 (만드는 부분으로 queryset은 필요 없음)


#- retrieve(상세 조회)

class TodoGenericsRetrieveAPI(generics.RetrieveAPIView):
    queryset = Todo.objects.all()  # 전체 Todo 목록을 가져오는 쿼리셋
    serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정

#- update(수정)

class TodoGenericsUpdateAPI(generics.UpdateAPIView):
    queryset = Todo.objects.all()  # 전체 Todo 목록을 가져오는 쿼리셋
    serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정

#- delete(destroy)(삭제)

class TodoGenericsDeleteAPI(generics.DestroyAPIView):
    queryset = Todo.objects.all()  # 전체 Todo 목록을 가져오는 쿼리셋
    serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정

# DRF GenericAPIView는 Django REST Framework에서 제공하는 클래스 기반 뷰로, CRUD(Create, Read, Update, Delete) 작업을 쉽게 구현할 수 있도록 도와줍니다.
# 이 GenericAPIView는 Django의 기본 View를 상속받아, RESTful API를 구현할 때 자주 사용되는 기본적인 동작을 제공합니다.
# 예를 들어, ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView 등 다양한 GenericAPIView가 제공되어, 각각의 작업에 맞는 API를 쉽게 만들 수 있습니다.
# 이 GenericAPIView를 사용하면, 코드의 중복을 줄이고, 더 간결하고 유지보수가 쉬운 API를 만들 수 있습니다.
# 예를 들어, ListAPIView는 전체 목록을 조회하는 API를 쉽게 만들 수 있도록 도와주며, CreateAPIView는 새로운 객체를 생성하는 API를 쉽게 구현할 수 있습니다.
# 이 GenericAPIView는 Django REST Framework의 강력한 기능 중 하나로, 개발자가 API를 빠르게 구축할 수 있도록 도와줍니다.
# 아래 두 개를 통해 위 네가지 기능 모두 사용 가능

# List Create (list 또는 create를 동시에 사용하고 싶을 때)
class TodoGenericsListCreateAPI(generics.ListCreateAPIView):
    queryset = Todo.objects.all()  # 전체 Todo 목록을 가져오는 쿼리셋
    serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정

# 섞을 수도 있음 retrieve, update, delete를 섞어서 사용할 수도 있음(retrieveUpdateDelete) (예: 상세 조회, 수정, 삭제를 동시에 처리하는 API)

class TodoGenericsRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()  # 전체 Todo 목록을 가져오는 쿼리셋
    serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정




#DRF _ viewsets

from .pagination import CustomPageNumberPagination  # 커스텀 페이지네이션 클래스 가져오기
# 커스텀 페이지네이션 클래스를 가져와서, GenericAPIView에 적용할 수 있습니다.
# 이 페이지네이션 클래스는 페이지 크기를 동적으로 조정할 수 있는 기능을 제공합니다.
# 예를 들어, 쿼리 파라미터로 page_size를 받아서, 그 값에 따라 페이지 크기를 조정할 수 있습니다.
# 만약 page_size가 "all"이면 전체 데이터를 한 번에 보여줍니다.
# 만약 page_size가 숫자가 아니면, 기본 페이지 크기를 사용합니다.
# 이 설정은 서버의 성능을 보호하고, 너무 많은 데이터를 한 번에 처리하는 것을 방지하기 위해 사용됩니다.
from rest_framework.authentication import SessionAuthentication  # 세션 인증 클래스
from rest_framework.permissions import IsAuthenticated  # 인증된 사용자만 접근할 수 있도록 하는 권한 클래스
# 이 설정은 해당 API에 접근하기 위해 사용자가 인증되어야 함을 의미합니다.
# 예를 들어, 인증된 사용자만 Todo 목록을 조회하거나, 새로운 Todo를 생성할 수 있도록 제한할 수 있습니다.
from rest_framework import viewsets

class TodoViewSet(viewsets.ModelViewSet):
    #pagination
    pagination_class = CustomPageNumberPagination  # 커스텀 페이지네이션 클래스 설정

    #예를 들어, 특정 사용자의 Todo만 가져오고 싶다면 (인증 또는 권한)
    #인증
    authentication_classes = []  # 인증 클래스 설정 (예: SessionAuthentication, TokenAuthentication 등)
    #권한
    permission_classes = [AllowAny]  # 권한 클래스 설정 (예: IsAuthenticated, IsAdminUser 등)
    # 이 설정은 해당 API에 접근하기 위해 사용자가 인증되어야 함을 의미
    # 예를 들어, 인증된 사용자만 Todo 목록을 조회하거나, 새로운 Todo를 생성할 수 있도록 제한할 수 있습니다.
    # 만약 인증이 필요 없는 API를 만들고 싶다면, permission_classes를 []
    # permission_classes = []로 설정하면 인증이 필요 없는 API를 만들 수 있습니다.  

    #이미지
    parser_classes = [MultiPartParser, FormParser]  # 파일 업로드를 위한 파서 클래스 (파일 업로드가 필요한 경우에만 사용) parser(파서)**는 어떤 데이터를 읽고 → 해석해서 → 구조화된 정보로 바꾸는 도구입니다.
    # MultiPartParser는 파일 업로드를 처리할 때 사용되는 파서입니다.
    # FormParser는 일반 폼 데이터를 처리할 때 사용됩니다.

    #검색기능
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]  # 필터링 백엔드 설정 (예: DjangoFilterBackend, SearchFilter 등) // 필터링 백엔드는 API 요청에 대한 필터링을 처리하는 클래스입니다.

    #   queryset = Todo.objects.all().order_by("-created_at") 를 아래처럼 작성 가능
    def get_queryset(self):
        qs = Todo.objects.all().order_by("-created_at") 
        return qs # 전체 Todo 목록을 가져오는 쿼리셋
    serializer_class = TodoSerializer

    # queryset = Todo.objects.all().order_by("-created_at")  # 전체 Todo 목록을 가져오는 쿼리셋 // 만약 순서를 바꾸고 싶다면 queryset = Todo.objects.all().order_by('name') 처럼 쿼리셋을 수정할 수 있습니다.
    # queryset은 데이터베이스에서 가져올 데이터를 정의하는 부분입니다.
    # 예를 들어, queryset = Todo.objects.filter(complete=False) 는 완료되지 않은 Todo 항목만 가져오는 쿼리셋을 정의합니다. 
    # 만약 다양한 조건이 있다면 또는 조건을 추가해야한다면?DRF, Django CBV에서는 get_queryset()을 오버라이드해서 동적으로 쿼리를 바꾸는 게 일반적인 패턴입니다
    # 1. 재사용을 위해 2. 클래스 기반 뷰(CBV)에서 권장되는 방식 (오바라이딩 해서 동적 쿼리) 3. 가독성 주석 설명
    #방법은 아래 def get_queryset(self): 메소드를 오버라이드하여 쿼리셋을 정의하는 것입니다.


    # 예를 들어, 특정 사용자의 Todo만 가져오고 싶다면
    #     user = self.request.user  # 현재 요청한 사용자
    #     return Todo.objects.filter(user=user)  # 해당 사용자의 Todo만 가져오는 queryset
    # # get_queryset 메소드를 오버라이드하여, 요청한 사용자에 따라 다른 queryset을 반환할 수 있습니다.
    # # 예를 들어, 특정 사용자의 Todo만 가져오고 싶다면, self.request.user를 사용하여 현재 요청한 사용자를 가져오고, 해당                     
    # # 사용자의 Todo만 가져오는 queryset을 반환할 수 있습니다.
    # # 이 메소드는 viewset이 호출될 때마다 실행되며, 요청에 따라 동적으로 queryset을 변경할 수 있습니다.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # 로그에 오류 출력
            return Response(serializer.errors, status=400)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


#로그인 (제공해주는 형식 링크 DRF 제공 링크: https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication)

    #logoutapi (서버에 로그아웃 요청) -> post 방식으로 요청을 보내야 합니다.(Axios, fetch 등으로) // 장고기본 지원 (웹)
class CustomLogoutApi(APIView):
    def post(self, request): #상태변화가 일어나는 요청
        # 로그아웃 처리
        from django.contrib.auth import logout
        from django.shortcuts import redirect
        logout(request)
        # return redirect('todo_List')  # 로그아웃 후 리다이렉트할 URL을 지정합니다. (예: todo_List로 리다이렉트) # -- 이건 apiview 방식
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK) #-- 이건 axios 방식으로 왜냐면 axios 에서 리다이렉트 함
        # 로그아웃 처리는 Django의 기본 logout 함수를 사용하여 세션을 종료
        # 로그아웃 후에는 클라이언트에게 성공 메시지를 반환합니다.
        # 이 API는 POST 요청을 통해 로그아웃을 처리하며, 클라이언트는 이 API를 호출하여 로그아웃할 수 있습니다.
        # 예를 들어,
        # axios.post('/api/custom-logout/')
        # 또는 fetch('/api/custom-logout/', { method: 'POST' })
        # 와 같이 요청을 보낼 수 있습니다.



