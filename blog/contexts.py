def btn_back(request):
    context = dict()
    context['keyword'] = ''
    context['all'] = ''
    if 'q' in request.GET:
        keyword = request.GET['q']
        if keyword:
            context['keyword'] = '?q=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != 1:
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context