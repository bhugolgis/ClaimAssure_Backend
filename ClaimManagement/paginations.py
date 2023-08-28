
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LimitsetPagination(LimitOffsetPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10000




