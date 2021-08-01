from rest_framework.pagination import PageNumberPagination


class GlobalPageNumberPagination(PageNumberPagination):
    def __init__(self):
        super(GlobalPageNumberPagination, self).__init__()
        self.page_size_query_param = 'page_size'
        self.max_page_size = 1000  # 这个设置很重要
