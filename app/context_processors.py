from app.models import News, Category


def latest_post(request):
    latest_news = News.published.all().order_by('-publish_time')
    categories = Category.objects.all()
    context = {
        'latest_news': latest_news,
        'categories': categories,
    }
    return context
