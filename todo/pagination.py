from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.conf import settings

class CustomPageNumberPagination(PageNumberPagination):
  default_page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 10) # 기본 페이지 크기를 설정합니다. settings.py에서 PAGE_SIZE를 가져오고, 없으면 10으로 설정합니다.

  # 페이지네이션할 때, 몇 개씩 데이터를 자를지를 동적으로 결정합니다.
  # 쿼리 파라미터로 page_size를 받아서, 그 값에 따라 페이지 크기를 조정합니다.
  # 만약 page_size가 "all"이면 전체 데이터를 한 번에 보여줍니다.
  # 만약 page_size가 숫자가 아니면, 기본 페이지 크기를 사용합니다.
  # 예를 들어, ?page_size=5이면 5개씩 데이터를 보여주고, ?page_size=all이면 전체 데이터를 한 번에 보여줍니다.
  # 만약 page_size가 쿼리 파라미ter로 주어지지 않으면, settings.py에서 설정한 기본 페이지 크기를 사용합니다
  # (예: settings.py에서 PAGE_SIZE = 10으로 설정했다면, 기본 페이지 크기는 10이 됩니다).
  page_size_query_param = "page_size" # 쿼리 파라미터 이름을 "page_size"로 설정합니다. 이 파라미터를 통해 페이지 크기를 조정할 수 있습니다.
  max_page_size = 1000 # 최대 페이지 크기를 1000으로 설정합니다. 이 값은 사용자가 요청할 수 있는 최대 페이지 크기를 제한합니다. 예를 들어, ?page_size=1000이면 최대 1000개씩 데이터를 보여줄 수 있습니다. 만약 사용자가 1000보다 큰 값을 요청하면,
  # 페이지 크기는 1000으로 제한됩니다. 이 설정은 서버의 성능을 보호하고, 너무 많은 데이터를 한 번에 처리하는 것을 방지하기 위해 사용됩니다.
  def paginate_queryset(self, queryset, request, view=None): 
    page_size = request.query_params.get("page_size", self.default_page_size) # 페이지 크기를 쿼리 파라미터에서 가져옵니다. 없으면 기본 페이지 크기를 사용합니다.

    if page_size == "all":
      self.page_size = queryset.count()
    else:
      try:
        self.page_size = int(page_size)
      except ValueError:
        self.page_size = self.default_page_size

    return super().paginate_queryset(queryset, request, view)

  def get_paginated_response(self, data):
    return Response(
      OrderedDict([
        ("data", data), # 페이지네이션된 데이터 (serializer.data가 여기로 전달됨)
        ("page_size", len(data)), # 현재 페이지에 포함된 데이터의 수  (ex: 5개면 5)
        ("total_count", self.page.paginator.count), # 전체 데이터의 수  (ex: Todo 전체가 30개면 30)
        ("page_count", self.page.paginator.num_pages), #  전체 페이지 수 (ex: 한 페이지에 5개면 6페이지)
        ("current_page", self.page.number),# 현재 보고 있는 페이지 번호 (1부터 시작)
        ("next", self.get_next_link()), # 다음 페이지 링크 (없으면 None) 다음 페이지로 이동할 수 있는 URL (ex: /todo/viewsets/view/?page=2), 없으면 null
        ("previous", self.get_previous_link()), # 이전 페이지 링크 (없으면 None) 이전 페이지로 이동할 수 있는 URL (ex: /todo/viewsets/view/?page=1), 없으면 null
      ])
    )