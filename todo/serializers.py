#DRF에서는 Forms.py 사용 X : forms.py는 Django의 전통적인 "HTML 폼 기반" 개발 방식에서 사용하는 것이고,DRF(Django REST Framework)는 JSON API를 기반으로 동작하기 때문에 기본적으로 forms.py를 사용하지 않습니다.
#이유 프론트엔드가 JSON으로 요청을 보내기 때문에,Django의 form.as_p() 같은 HTML 폼 기능이 필요하지 않으며, serializers.py가 forms.py의 역할을 대신합니다: 유효성 검사, 필드 정의, 데이터 저장 등
#정리 forms.py는 서버 템플릿 + HTML 폼 기반 앱에서 필요합니다. // DRF 프로젝트에서는 대부분 serializers.py만 사용합니다.// 대신 프론트에서는 JavaScript로 JSON을 만들어 API로 POST/PUT 요청을 합니다.
#form 예시
#model 
# from django.db import models

# class Todo(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     complete = models.BooleanField(default=False)
#     exp = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)

#forms.py 
# from django import forms
# from .models import Todo

# class TodoForm(forms.ModelForm):
#     class Meta:
#         model = Todo
#         fields = ['name', 'description', 'complete', 'exp']

# views.py
# from django.shortcuts import render, redirect
# from .forms import TodoForm

# def create_todo(request):
#     if request.method == "POST":
#         form = TodoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("todo_list")  # 또는 success url
#     else:
#         form = TodoForm()

#     return render(request, "todo/create.html", {"form": form})

#template 예시
# <!-- create.html -->
# <form method="post">
#   {% csrf_token %}
#   {{ form.as_p }}
#   <button type="submit">할 일 등록</button>
# </form>

# ✅ 차이 요약
# 구분	  :        Django (HTML 뷰 기반)	  //  DRF (JSON API 기반)
# 주로 사용하는 폼 :	forms.py의 Form 또는 ModelForm	// serializers.py의 Serializer 또는 ModelSerializer
# 사용자 입력 처리 방식 :	HTML <form> → 서버에서 유효성 검사	// JS에서 JSON 전송 → API에서 유효성 검사
# 사용하는 뷰 :	CreateView, UpdateView 등 // APIView, GenericAPIView 등
# 사용 예 :	블로그 글 작성, 로그인 폼 등	// 프론트엔드와 분리된 API 서버

from rest_framework.serializers import ModelSerializer
from .models import Todo

class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        # fields = ["name", "description", "complete", "exp", "completed_at", "created_at", "updated_at"]
        # exclude = ["completed_at", "exp",]
        fields = "__all__" #모델 값 전체를 데려올 수 있음 위처럼 번거롭게 할 필요가 없음
