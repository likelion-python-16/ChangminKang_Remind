from django.db import models
from todo.models import Todo
from django.contrib.auth.models import User  # Django의 기본 User 모델을 가져옵니다.

# 세가지 모델을 나눠서 만드는 이유는 연결이 아닌 각각 객체로 존재하므로 따로 정리 (좋아요 누른다고 댓글을 달 수도 안 달 수도 있기 때문에) 
#좋아요 모델 
class Like(models.Model):
    # 공통필드
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 좋아요를 누른 사용자
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)  # 좋아요가 눌린 Todo 항목
    # 개별필드 (좋아요 좋아요 취소 클릭으로 바뀌게 -> complete 필드와 비슷 : booleanField)
    is_like= models.BooleanField(default=True)  # 좋아요 상태 (True: 좋아요, False: 좋아요 취소) // 기본값은 True로 설정되어 있습니다. // 이 필드는 사용자가 좋아요를 누른 상태인지 여부를 나타냅니다. // 기본값은 True로 설정되어 있습니다. // 이 필드는 사용자가 좋아요를 누른 상태인지 여부를 나타냅니다. // 기본값은 True로 설정되어 있습니다. // 이 필드는 사용자가 좋아요를 누른 상태인지 여부를 나타냅니다.
    class Meta: # 메타 클래스는 모델의 메타데이터를 정의합니다. // 메타클래스는 무엇인가요: # 메타클래스는 클래스의 클래스입니다. 즉, 클래스를 정의하는 클래스입니다.(class Meta는 Django 모델 내부에서 **메타데이터(Meta-data)**를 정의하는 내부 클래스입니다. 말 그대로 “모델에 대한 부가 정보”를 정의하는 공간) // 메타클래스는 클래스의 속성이나 동작을 정의하는 데 사용됩니다. // 예를 들어, 모델의 이름, 데이터베이스 테이블 이름, 정렬 순서 등을 정의할 수 있습니다. 
        unique_together = ('user', 'todo')  # 유저와 Todo 항목의 조합이 유일해야 함을 정의합니다. // 이 설정은 같은 사용자가 같은 Todo 항목에 대해 중복으로 좋아요를 누르는 것을 방지합니다. // 즉, 한 사용자가 동일한 Todo 항목에 대해 여러 번 좋아요를 누를 수 없도록 합니다. // 이 설정은 데이터베이스에서 유일한 제약 조건을 생성하여 중복 데이터를 방지합니다.
        #todo, user 속성은 중복 데이터를 아예 저장하지 못하게 막아주는 제약조건
        #중복방지 코드는 같은 사용자가 좋아요 2번 못누르게 하는 기능
        #좋아요 버튼을 여러 번 누르면 의도하지 않게 여러 개의 Like 레코드가 생길 수 있는데, 이를 방지하기 위해 이 제약을 둡니다. //코드로 막는 것도 가능하지만, DB에서 보장하면 더 안전합니다.
        #중복방지 코드는 같은 사용자가 좋아요 2번 못누르게 하는 기능 (중복된 좋아요 방지: A 사용자가 같은 할 일(Todo 3번)에 대해 여러 번 Like를 생성할 수 없습니다.) (DB 차원에서 막음: 장고가 아닌 데이터베이스 수준에서 "user와 todo가 함께 있는 조합"이 단 한 번만 등장할 수 있도록 제한합니다.)
    
    def __str__(self):
        return f"{self.user.username} ❤️ {self.todo.name}" # 좋아요를 누른 사용자와 Todo 항목의 이름을 문자열로 반환합니다. // 이 메서드는 객체를 문자열로 표현할 때 사용됩니다. // 예를 들어, Django 관리자 페이지나 쉘에서 Like 객체를 출력할 때, 객체의 사용자 이름과 Todo 항목의 이름이 표시됩니다. // 하트 모양은 웹 폰트로 이미지다운로드 사용
        # admin ❤️ 공부하기 

#북마크 모델
class Bookmark(models.Model):
    # 공통필드
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 좋아요를 누른 사용자
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)  # 좋아요가 눌린 Todo 항목
    is_bookmarked = models.BooleanField(default=True)  # 북마크 상태 (True: 북마크, False: 북마크 취소) // 기본값은 True로 설정되어 있습니다. // 이 필드는 사용자가 북마크를 누른 상태인지 여부를 나타냅니다. // 기본값은 True로 설정되어 있습니다. // 이 필드는 사용자가 북마크를 누른 상태인지 여부를 나타냅니다. // 기본값은 True로 설정되어 있습니다. // 이 필드는 사용자가 북마크를 누른 상태인지 여부를 나타냅니다.

    class Meta: 
        unique_together = ('user', 'todo')
    
    def __str__(self):
        return f"{self.user.username} 📌 {self.todo.name}"

#댓글 모델
class Comment(models.Model):
    # 공통필드
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 좋아요를 누른 사용자
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)  # 좋아요가 눌린 Todo 항목
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간 # foreignkey는 다른 모델과의 관계를 나타내는 필드입니다. // 이 필드는 댓글이 작성된 시간을 자동으로 저장합니다. // auto_now_add=True는 객체가 생성될 때 현재 시간을 자동으로 설정합니다. // 이 필드는 댓글이 작성된 시간을 자동으로 저장합니다. // auto_now_add=True는 객체가 생성될 때 현재 시간을 자동으로 설정합니다.
    
    #댓글을 좋아요 누른 유저들을 저장하는 필드 (기사 하나에 여러명이 접근하여 댓글을 달 수 있고, 그 댓글에 여러명이 좋아요를 누를 수 있기 때문에 다대다 관계로 설정합니다.)
    likes = models.ManyToManyField(User, through = "CommentLike", related_name='liked_comments', blank=True)  # 댓글을 좋아요 누른 사용자들 // ManyToManyField는 다대다 관계를 나타내는 필드입니다. // 이 필드는 댓글을 좋아요 누른 사용자들을 저장합니다. // related_name은 역참조 시 사용할 이름을 지정합니다. // blank=True는 이 필드가 비어있을 수 있음을 의미합니다. // 이 필드는 댓글을 좋아요 누른 사용자들을 저장합니다.
    # **역참조(reverse access)**는 _반대 방향에서 관계를 조회_하는 것을 의미합니다. 즉, User 모델에서 이 사용자가 어떤 댓글에 좋아요를 눌렀는지를 찾고 싶을 때: user.liked.all() // 여기서 liked는 바로 related_name='liked'에서 지정한 이름입니다.즉, user.liked는 "이 사용자가 좋아요를 누른 댓글 목록"을 의미합니다.
    # through = "CommentLike"는 중간 모델을 통해 다대다 관계를 설정합니다. // 이 설정은 Comment와 User 사이의 다대다 관계를 관리하기 위해 CommentLike 모델을 사용합니다. // 이 모델은 댓글과 좋아요를 누른 사용자 간의 관계를 저장합니다. 


    # # 같은 유저가 같은 todo에 댓글을 여러 번 달 수 없게 하고 싶다
    # class Meta:
    #     unique_together = ('user', 'todo')

    def __str__(self):
        return f"{self.user.username} 💬 {self.content[:20]}"

# 누가 어떤 댓글을 언제 좋아요 눌렀는지 저장하는 모델
class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)  # 좋아요가 눌린 댓글
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 좋아요를 누른 사용자
    liked_at = models.DateTimeField(auto_now_add=True)  # 좋아요가 눌린 시간
    is_like = models.BooleanField(default=True) # 현재 좋아요가 유효한지 여부의 boolean 필드

    class Meta:
        unique_together = ('user', 'comment')
    
    def __str__(self):
        return f"{self.user.username} ❤️ {self.comment.id}"