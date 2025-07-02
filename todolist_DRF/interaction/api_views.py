
from rest_framework import viewsets
from .models import Like, Bookmark, Comment, CommentLike  # 모델을 가져옵니다.
from .serializers import LikeSerializer, BookmarkSerializer, CommentSerializer, CommentLikeSerializer  # 시리얼라이저를 가져옵니다.
from rest_framework import permissions  # 권한 설정을 위한 모듈
from rest_framework.decorators import action  # 액션 데코레이터를 가져옵니다. (추가적인 행동을 정의할 때 사용합니다.)
from todo.models import Todo  # Todo 모델을 가져옵니다. (Todo 항목의 상세 정보를 보여주기 위해 필요합니다.)
from rest_framework.response import Response  # 응답 객체를 가져옵니다. (직렬화된 데이터를 반환할 때 사용합니다.)
from todo.serializers import TodoSerializer  # Todo 모델의 직렬화 클래스를 가져옵니다. (Todo 항목을 직렬화하는 데 사용됩니다.)
from django.shortcuts import get_object_or_404

class LikeViewSet(viewsets.ModelViewSet):
    #좋아요의 전체데이터 (정렬 필요 업ㅄㅇ)
    queryset = Like.objects.all()  # Like 모델의 모든 객체를 가져옵니다.
    serializer_class = LikeSerializer  # 직렬화 클래스 지정
    permission_classes = [permissions.IsAuthenticated]  # 권한 설정 (필요에 따라 수정)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        # 좋아요를 토글하는 액션입니다. ("토글(toggle)"은 컴퓨터나 UI(사용자 인터페이스)에서 두 가지 상태(예: ON/OFF, 열림/닫힘, 보이기/숨기기 등)를 전환하는 동작이나 버튼을 뜻)
    
        todo = get_object_or_404(Todo,pk=pk)  # Todo 객체를 가져옵니다.
        user = request.user  # 현재 로그인한 사용자
        like, created = Like.objects.get_or_create(user=user, todo=todo)  # 좋아요 객체를 가져오거나 생성합니다.(	해당 user와 todo에 대한 Like가 이미 DB에 존재하면 가져오고, 없으면 새로 생성함)
        like.is_like = not like.is_like  # 좋아요 상태를 토글합니다.  # is_like가 True면 False로, False면 True로 변경합니다.
        like.save()  # 변경된 상태를 저장합니다. 
        serializer = TodoSerializer(todo, context = {"request" : request})  # Todo 객체를 직렬화합니다.
        return Response(serializer.data)




# 좋아요 클릭시 -> 자바스크립트가 서버에 post 요청 -> 장고의 toggle 액션이 실행됨 -> get or create로 좋아요 객체를 가져오거나 생성함 -> is_like 필드를 토글함(눌렸음 끄고 꺼져있음 누르고) -> 저장함 -> 직렬화된 Todo 객체를 반환함

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()  # Like 모델의 모든 객체를 가져옵니다.
    serializer_class = BookmarkSerializer  # 직렬화 클래스 지정
    permission_classes = [permissions.IsAuthenticated]  # 권한 설정 (필요에 따라 수정)

    @action(detail=True, methods=["post"]) 
    def toggle(self, request, pk=None): 
        todo = get_object_or_404(Todo, pk=pk)
        user = request.user

        bookmark, created = Bookmark.objects.get_or_create(todo=todo, user=user) 
        bookmark.is_bookmarked = not bookmark.is_bookmarked 
        bookmark.save() 

        serializer = TodoSerializer(todo, context={"request": request}) 
        return Response(serializer.data) 


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        todo_id = self.request.query_params.get("todo_pk") 
        return Comment.objects.filter(todo_id=todo_id).order_by("-created_at")

    def perform_create(self, serializer):
        todo_id = self.request.data.get("todo_pk")
        todo = Todo.objects.get(pk=todo_id)
        serializer.save(user=self.request.user, todo=todo)

class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])  # /commentlikes/{pk}/toggle/
    def toggle(self, request, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        user = request.user
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        like.is_like = not like.is_like
        like.save()
        return Response({
            "is_liked": like.is_like,
            "like_count": CommentLike.objects.filter(comment=comment, is_like=True).count()
        })

