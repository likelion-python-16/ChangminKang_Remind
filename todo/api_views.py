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
    def put(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"Error":"해당 Todo가 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TodoSerializer(todo, data=request.data) #request.data는 클라이언트가 보낸 데이터
        serializer.is_valid(raise_exception=True) #유효성 검사
        todo = serializer.save() #save는 평탄화된 데이터를 저장하는 것
        return Response(TodoSerializer(todo).data, status=status.HTTP_200_OK)

class TodoDeleteAPI(APIView):
    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"Error":"해당 Todo가 없습니다"}, status=status.HTTP_404_NOT_FOUND)
        
        todo.delete() #삭제
        return Response(status=status.HTTP_204_NO_CONTENT) #204는 삭제 성공을 의미