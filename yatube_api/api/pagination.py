from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit == None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        ordered_queryset = queryset.order_by('pk')
        return list(
            ordered_queryset[self.offset:self.offset + self.limit])
