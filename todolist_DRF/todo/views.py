from django.shortcuts import render
from .models import Todo
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

def todo_list(request): #urls 속 todo_list와 연결을 위해 이름이 같아야한다.
    todos = Todo.objects.all() #모델 Todo의 모든 것을 가져온다
    return render(request, "todo/todo.html", {"todos" : todos}) 
#render()는 Django에서 HTML 페이지를 만들어 응답(Response)으로 보내주는 함수입니다.
#request	클라이언트(브라우저)로부터 들어온 요청 객체입니다. 항상 첫 번째 인자로 들어가야 해요.
#"todo/todo.html"	사용할 템플릿 파일의 경로입니다. 프로젝트의 templates/ 디렉토리 아래 경로로 해석됩니다. 예: templates/todo/todo.html
#{"todos": todos}	템플릿으로 넘길 데이터(Context). 이건 템플릿에서 사용할 수 있는 변수들을 딕셔너리 형태로 전달해요.
#"todos" (앞쪽)	템플릿에서 사용할 변수 이름입니다. HTML에서 {{ todos }}로 접근 가능.
# #todos (뒤쪽)	파이썬에서 정의한 변수입니다. 이 코드에서는 Todo.objects.all() 결과를 담고 있죠.
#위로는 인솜니아 통해서 데이터를 입력할 수 없음 (admin을 통해 시작 --> admin.py를 통해 model과 연결 필요)


#전체보기
class TodoListViews(ListView): #제너릭뷰 / urls.py 클래스형 명과 동일시 / ListView는 제너릭
    model = Todo
    template_name = "todo/list.html" #todo였다가 list로 바꾸는거면 templates 변경 필요
    context_object_name = "todos"# def 내용 두개를 포함하는 내용은 위 세개 / 아래 두개는 옵션
    ordering = ["-created_at"]
    success_url = reverse_lazy("todo_List")

#생성
class TodoCreateViews(CreateView):
    model = Todo
    template_name = "todo/create.html"
    fields = ["name", "description", "complete", "exp","image"]
    success_url = reverse_lazy("todo_List") ## reverse_lazy는 URL을 지연 평가하는 함수로, URL이 아직 정의되지 않았을 때도 사용할 수 있습니다.
    # reverse_lazy("todo_List")는 urls.py에서 정의한 todo_List라는 이름의 URL 패턴을 찾아서 해당 URL로 리다이렉트합니다.
    # 이때 reverse_lazy를 사용하면 URL이 아직 로드되지 않았더라도 안전하게 사용할 수 있습니다.
    # reverse_lazy는 URL을 문자열로 반환하는 대신, URL 패턴이 실제로 존재할 때까지 평가를 지연시킵니다.
    # 따라서 URL 패턴이 정의되지 않은 상태에서도 사용할 수 있습니다.
    # 이 방식은 Django의 URL 네임스페이스를 활용하여 URL을 동적으로 생성할 수 있게 해줍니다.
    # # 예를 들어, todo_List라는 이름의 URL 패턴이 urls.py에 정의되어 있다면, 
    # reverse_lazy("todo_List")는 해당 URL 패턴의 URL을 반환합니다.
    # # 이렇게 하면 URL이 변경되더라도 코드에서 직접 URL을 수정할 필요 없이, 
    # URL 패턴의 이름만 변경하면 됩니다. 이는 코드의 유지보수성을 높이는 데 도움이 됩니다.
    # # 따라서, reverse_lazy("todo_List")는 URL 패턴의 이름을 사용하여 해당 URL로 리다이렉트하는 데 사용됩니다. 
    #성공했을 때 redirect 할 url을 지정하는 것

#상세보기
class TodoDetailViews(DetailView):
    model = Todo
    template_name = "todo/detail.html"
    context_object_name = "todos"

#업데이트
class TodoUpdateViews(UpdateView):
    model = Todo
    template_name = "todo/update.html"
    fields = ["name", "description", "complete", "exp", "image"]
    context_object_name = "todos"
    # fields는 모델의 필드를 지정하는 옵션입니다.
    success_url = reverse_lazy("todo_List")
    # CreateView를 사용했지만, UpdateView로 변경하는 것이 더 적절합니다
    # UpdateView는 기존 객체를 수정하는 데 사용되며, CreateView는 새로운 객체를 생성하는 데 사용됩니다.
    # 따라서, TodoUpdateViews는 UpdateView로 변경하는 것이 좋습니다.
    # UpdateView를 사용하면, 기존 객체를 수정할 때 자동으로 해당 객체를 가져와서 수정할 수 있습니다.


# #삭제
# class TodoDeleteViews(DeleteView):
#     model = Todo
#     template_name = "todo/delete.html"
#     context_object_name = "todos"
#     success_url = reverse_lazy("todo_List")
#     # DeleteView는 객체를 삭제하는 데 사용됩니다. 
#     # 이 클래스는 객체를 삭제할 때 자동으로 해당 객체를 가져와서 삭제할 수 있습니다.
#     # 따라서, TodoDeleteViews는 DeleteView로 변경하는 것이 좋습니다.
#     # DeleteView를 사용하면, 기존 객체를 삭제할 때 자동으로 해당 객체를 가져와서 삭제할 수 있습니다.


