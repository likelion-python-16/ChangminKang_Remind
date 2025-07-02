from django.contrib import admin
from .models import Like, Bookmark, Comment, CommentLike  # 모델을 가져옵니다.

# admin.py 파일은 Django 관리자 사이트에서 모델을 관리할 수 있도록 설정하는 곳입니다.

admin.site.register(Like)
admin.site.register(Bookmark)

# admin.site.register(Comment) # 주석 처리된 이유: Comment 모델은 아래에서 CommentAdmin 클래스를 통해 커스터마이징되어 등록됩니다. (site.register()는 모델을 관리자 사이트에 등록하는 함수입니다. 이 함수는 Django 관리자 사이트에서 해당 모델을 관리할 수 있도록 합니다. 수정을 위해서라면 site를 빼야한다. )
@admin.register(Comment) # admin 화면 설계 (site가 없는 이유: @admin.register(Comment)는 Comment 모델을 관리자 사이트에 등록하는 데 사용되는 데코레이터입니다. 이 방식은 admin.site.register(Comment)와 동일한 기능을 수행하지만, 더 간결하고 가독성이 좋습니다. )
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'todo', 'content', 'created_at', "like_count")

    def like_count(self, obj):
        """
        댓글에 대한 좋아요 수를 반환합니다.
        """
        return obj.likes.count()

admin.site.register(CommentLike)
