
from rest_framework import viewsets
from interaction.models import Like, Bookmark, Comment  # 모델을 가져옵니다.

class LikeViewSet(viewsets.ModelViewSet):
    pass
    #좋아요의 전체데이터 (정렬 필요 업ㅄㅇ)
    #직렬화 / 역직렬화
    # 권한

class BookmarkViewSet(viewsets.ModelViewSet):
    pass
    # 북마크의 전체데이터
    # 직렬화 / 역직렬화 

class CommentViewSet(viewsets.ModelViewSet):
    pass
    # 댓글의 전체데이터
    # 직렬화 / 역직렬화