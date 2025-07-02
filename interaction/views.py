from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from todo.models import Todo  # Todo 모델을 가져옵니다. (Todo 항목의 상세 정보를 보여주기 위해 필요합니다.)
from interaction.models import Like, Bookmark, Comment  # 상호작용 모델을 가져옵니다. (좋아요, 북마크, 댓글 모델을 가져옵니다. 이 모델들은 Todo 항목과의 상호작용을 나타냅니다.)

# Create your views here.(화면에 나가는 출력 부분)

# 로그인하지 않은 사용자가 이 뷰를 실행하지 못하도록 막아주는 데코레이션 
@login_required # 로그인한 사용자만 이 뷰에 접근할 수 있도록 합니다. (이 데코레이터는 사용자가 로그인하지 않은 경우 로그인 페이지로 리다이렉트합니다.)
def todo_detail_with_interaction(request, pk):
    """
    특정 Todo 항목의 상세 정보와 상호작용(좋아요, 북마크, 댓글 등)을 보여주는 뷰입니다.
    """
    # Todo 항목을 가져옵니다. (pk는 URL에서 전달된 Todo 항목의 기본 키입니다.)
    todo = get_object_or_404(Todo, pk=pk) # pk는 URL에서 전달된 Todo 항목의 기본 키입니다. get_object_or_404는 주어진 모델(Todo)에서 pk에 해당하는 객체를 가져오고, 만약 해당 객체가 없으면 404 오류를 발생시킵니다.
    user = request.user # 현재 로그인한 사용자 정보를 가져옵니다. (이 정보는 나중에 상호작용 데이터와 연결하는 데 사용될 수 있습니다.)

    like_obj = Like.objects.filter(todo=todo, is_like = True).first()
    is_liked = like_obj.is_like if like_obj else False
    # 현재 사용자가 해당 Todo 항목에 좋아요를 눌렀는지 여부를 확인합니다. (Like 모델에서 todo 필드가 현재 Todo 항목과 일치하고, is_like가 True인 레코드를 가져옵니다. 만약 해당 레코드가 없다면 None을 반환합니다.)
    like_count = Like.objects.filter(todo=todo, is_like=True).count()  
    # 해당 Todo 항목에 대한 좋아요 수를 계산합니다. (Like 모델에서 todo 필드가 현재 Todo 항목과 일치하고, is_like가 True인 레코드의 수를 세어 좋아요 수를 계산합니다.)
    bookmark_obj = Bookmark.objects.filter(todo=todo, user = user).first()  
    # 현재 사용자가 해당 Todo 항목을 북마크했는지 여부를 확인합니다. (Bookmark 모델에서 todo 필드가 현재 Todo 항목과 일치하고, user 필드가 현재 사용자와 일치하는 레코드를 가져옵니다. 만약 해당 레코드가 없다면 None을 반환합니다.)
    comments = Comment.objects.filter(todo=todo).order_by('-created_at')  
    # 해당 Todo 항목에 대한 댓글을 가져옵니다. (Comment 모델에서 todo 필드가 현재 Todo 항목과 일치하는 레코드를 가져오고, 작성 시간(created_at)을 기준으로 내림차순으로 정렬합니다.)
    
    context = {
        'todo': todo,  # Todo 항목 정보
        'like_obj': like_obj,  # 현재 사용자가 해당 Todo 항목에 좋아요를 눌렀는지 여부 (존재하지 않을 수도 있음)
        'like_count': like_count,  # 해당 Todo 항목에 대한 좋아요 수
        'bookmark_obj': bookmark_obj,  # 북마크 객체 (존재하지 않을 수도 있음)
        'comments': comments,  # 댓글 목록
    } # context 딕셔너리는 템플릿에서 사용할 데이터를 포함합니다. 템플릿에서 보여줄 데이터를 모아놓은 바구니    

    return render(request, "interaction/todo_detail.html", context) # 템플릿을 렌더링합니다. (템플릿 파일은 interaction/todo_detail.html입니다. 이 템플릿은 Todo 항목의 상세 정보와 상호작용 데이터를 표시하는 데 사용됩니다.)