from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status

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


#DRF _ GenericAPIView


from rest_framework import generics

#- list

class TodoGenericsListAPI(generics.ListAPIView):
    queryset = Todo.objects.all()  # 전체 Todo 목록을 가져오는 쿼리셋
    serializer_class = TodoSerializer  # 사용할 직렬화 클래스 지정

#- create  

class TodoGenericsCreateAPI(generics.CreateAPIView):
    pass

#- retrieve

class TodoGenericsRetrieveAPI(generics.RetrieveAPIView):
    pass

#- update

class TodoGenericsUpdateAPI(generics.UpdateAPIView):
    pass

#- delete

class TodoGenericsDeleteAPI(generics.DestroyAPIView):
    pass

# List Create
class TodoGenericsListCreateAPI(generics.ListCreateAPIView):
    pass

# 섞을 수도 있음 retrieve, update, delete를 섞어서 사용할 수도 있음(retrieveUpdateDelete)

class TodoGenericsRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    pass









#DRF _ viewsets