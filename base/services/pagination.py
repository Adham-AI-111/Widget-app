from urllib.parse import urlencode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(request, queryset, per_page=15, page_param='page'):
    """
    Paginate a queryset and return (page_obj, page_queryset, qs_prefix).

    - page_obj: Django Page object for template controls
    - page_queryset: the items for the current page
    - qs_prefix: querystring prefix preserving current GET params except page,
                e.g. "status=Pending&" or "" if none
    """
    paginator = Paginator(queryset, per_page)
    page = request.GET.get(page_param, 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    params = request.GET.copy()
    if page_param in params:
        params.pop(page_param)
    qs_prefix = urlencode(params, doseq=True)
    if qs_prefix:
        qs_prefix += '&'

    return page_obj, page_obj.object_list, qs_prefix


