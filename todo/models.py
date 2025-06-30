from django.db import models
from django.utils import timezone  

class Todo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    exp = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #이미지 필드 추가 (pip install Pillow 필요)
    image = models.ImageField(upload_to='todo_images/', null=True, blank=True) # null=True, blank=True는 이 필드가 비어있을 수 있음을 의미합니다. upload_to는 이미지가 저장될 디렉토리를 지정합니다. 예를 들어, todo_images/ 디렉토리에 이미지를 저장합니다.

    def __str__ (self):
        return self.name # __str__ 메서드는 객체를 문자열로 표현할 때 사용됩니다. 여기서는 Todo 객체의 이름을 반환합니다. 이 메서드를 정의하면, Django 관리자 페이지나 쉘에서 Todo 객체를 출력할 때, 객체의 이름이 표시됩니다.
    
    # 기본 동작 보안: 완성된 날짜 (completed_at) 값에 따라 자동으로 시간이 처리되게 

# def save(self, *args, **kwargs):
#     if self.complete and self.completed_at is None: # 완료 상태로 변경되면 completed_at을 현재 시간으로 설정
#             self.completed_at = timezone.now()  # 완료되면 현재 시간으로 설정
#     if not self.complete and self.completed_at is not None: # 완료되지 않은 상태로 변경되면 completed_at을 None으로 설정
#             self.completed_at = None
#     super().save(*args, **kwargs)  # 부모 클래스의 save 메서드를 호출하여 저장 작업을 수행합니다.

    def save(self, *args, **kwargs):
        if self.complete and self.completed_at is None:
                self.completed_at = timezone.now()  # 완료되면 현재 시간으로 설정
        if not self.complete and self.completed_at is not None: # 완료되지 않은 상태로 변경되면 completed_at을 None으로 설정
                self.completed_at = None
        super().save(*args, **kwargs)  # 부모 클래스의 save 메서드를 호출하여 저장 작업을 수행합니다.