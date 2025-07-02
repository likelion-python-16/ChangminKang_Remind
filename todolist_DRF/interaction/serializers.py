from .models import Like, Bookmark, Comment, CommentLike  # 모델을 가져옵니다.
from rest_framework import serializers

#user.username todo.name 이라는 외래키를 가져와서 serializer로 변환합니다.

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # 사용자 이름을 직렬화합니다. // source=  'user.username'는 Like 모델의 user 필드에서 username 속성을 가져옵니다. // read_only=True는 이 필드가 읽기 전용임을 나타냅니다. 즉, 클라이언트가 이 필드를 수정할 수 없음을 의미합니다.
    todo_name = serializers.CharField(source='todo.name', read_only=True)  # Todo 항목의 이름을 직렬화합니다. // source='todo.name'는 Like 모델의 todo 필드에서 name 속성을 가져옵니다. // read_only=True는 이 필드가 읽기 전용임을 나타냅니다. 즉, 클라이언트가 이 필드를 수정할 수 없음을 의미합니다.
   
    class Meta:
        model = Like
        # fields = "__all__" (모델의 모든 필드를 포함합니다. 이 설정은 모델의 모든 필드를 직렬화하고 역직렬화할 수 있게 합니다. 하지만 좋지 못하기에 특정화)
        fields = ["id", "todo", "user", "is_like", "username", "todo_name"]  # 직렬화할 필드를 지정합니다. // 이 설정은 Like 모델의 id, todo, user, is_like 필드와 username, todo_name 필드를 직렬화합니다. // username과 todo_name은 Like 모델의 외래키 필드에서 가져온 값입니다.
        read_only_fields = ["user"]


# read_only= True 이 필드는 출력전용으로 클라이언트가 값을 보내도 저장에는 사용되지 않습니다.

class BookmarkSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    todo_name = serializers.CharField(source='todo.name', read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id, todo", "todo_name", "user", "is_bookmarked", "username"]
        read_only_fields = ["user"]
    
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    todo_name = serializers.CharField(source='todo.name', read_only=True)

    like_count = serializers.SerializerMethodField()  # 댓글에 대한 좋아요 수를 계산하는 필드입니다. // SerializerMethodField는 메서드를 통해 값을 계산하는 필드입니다. // 이 필드는 get_like_count 메서드를 통해 댓글에 대한 좋아요 수를 계산합니다.   
    is_liked = serializers.SerializerMethodField()  # 현재 로그인 사용자가 댓글을 좋아요 했는지 여부를 반환하는 필드입니다. // SerializerMethodField는 메서드를 통해 값을 계산하는 필드입니다. // 이 필드는 get_is_liked 메서드를 통해 현재 로그인 사용자가 댓글을 좋아요 했는지 여부를 반환합니다.
    
    class Meta:
        model = Comment
        fields = ["id", "todo", "todo_name", "user", "content", "created_at", "username", "like_count", "is_liked"]  # 직렬화할 필드를 지정합니다. // 이 설정은 Comment 모델의 id, todo, user, content, created_at 필드와 username, like_count, is_liked 필드를 직렬화합니다. // username은 댓글 작성자의 사용자 이름을 나타내며, like_count는 댓글에 대한 좋아요 수를 나타냅니다. is_liked는 현재 로그인 사용자가 댓글을 좋아요 했는지 여부를 나타냅니다.
        read_only_fields = ["todo", "user", "created_at"]

    def get_like_count(self, obj):
        
        # 댓글에 대한 좋아요 수를 반환합니다.
    
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        
       #현재 로그인 사용자가 댓글을 좋아요 했는지 여부를 반환합니다.
        
        request = self.context.get('request') # 현재 요청을 보낸 사용자를 알아내기 위한 준비 // Serializer는 context라는 딕셔너리를 통해 추가 정보를 받을 수 있습니다.
        if request and request.user.is_authenticated: # 요청 객체가 존재하고, 로그인된 사용자일 경우에만 실행합니다.로그인을 안 했거나 익명 사용자면 False를 반환하게 됩니다.
            return obj.likes.filter(id=request.user.id).exists() # obj.likes는 Comment 모델의 likes 필드입니다 → ManyToManyField → 좋아요 누른 유저 목록 // .filter(id=request.user.id) → 현재 사용자가 이 댓글을 좋아요 눌렀는지 확인 // .exists() → 있으면 True, 없으면 False  
        return False
    


# 시리얼라이저? 유효성 검증, 프리젠테이션 로직을 처리(사용자에게 보여지는 방식). // 화면에 표시되는 방식, 스타일과 관련된 로직을 처리한다. 
'''
시리얼라이저는:
📥 데이터를 받을 때 = "검사하고 정리하고"
📤 데이터를 보낼 때 = "보기 좋게 포장해서 전달
''' 

# M2M (다대다 관계를 의미) 추가

class CommentLikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # 좋아요를 누른 사용자의 이름을 직렬화합니다.
    comment_content = serializers.CharField(source='comment.content', read_only=True)  # 좋아요가 눌린 댓글의 내용을 직렬화합니다.

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'comment_content', 'is_like', 'username',"is_liked","liked_at"]  # 직렬화할 필드를 지정합니다. // 이 설정은 CommentLike 모델의 id, user, comment, is_like 필드와 username, comment_content, is_liked, liked_at 필드를 직렬화합니다.
        read_only_fields = ['user']  # id와 liked_at 필드는 읽기 전용입니다.