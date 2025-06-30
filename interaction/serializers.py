from .models import Like, Bookmark, Comment  # 모델을 가져옵니다.
from rest_framework import serializers



class LikeSerializer():
    class Meta:
        model = Like
        # fields = "__all__" (모델의 모든 필드를 포함합니다. 이 설정은 모델의 모든 필드를 직렬화하고 역직렬화할 수 있게 합니다. 하지만 좋지 못하기에 특정화)
        fields = [""]
        
class BookmarkSerializer():
    class Meta:
        model = Bookmark
        fields = "__all__"
    
class CommentSerializer():
    class Meta:
        model = Comment
        fields = "__all__"