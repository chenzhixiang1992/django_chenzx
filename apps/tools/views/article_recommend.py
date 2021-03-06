"""文章随机推荐和定向推荐"""
from post.models import Article

# 随机推荐文章
def rand_article(except_id=0):
    """
    随机推荐文章，默认推荐十篇文章，并且排除现在在看的这一篇
    在blog应用中引用rand_article方法：data['rand_articles'] = rand_article(),
    再由其传去前端，filter(is_published=True)来过滤已经发表的文章
    """
    rand_num = 5
    return Article.objects.exclude(id=except_id).filter(is_published=True).order_by('?')[:rand_num]

# 上一篇和下一篇文章推荐
def pre_next_article(id):
    """
    在artilce_show中引用pre_next_article方法，并传递参数id(当前文章的id)
    到pre_next_article方法，然后按照下面的方法得到上一篇和下一篇文章。
    data['pre_article'] = pre_next_article(id)[0] # 代表引用pre_next_article方法返回的第一个参数
    data['next_article'] = pre_next_article(id)[1] # 代表引用pre_next_article方法返回的第二个参数
    """
    current_article = Article.objects.get(id=id)  # 当前打开的博客
    """得到当前文章的前面部分和后面部分全部文章，按照id大小排列，例如：
    当前id = 26，获得的next_article和pre_article的id分别为[27,28,29,...]
    和[25,24,23,...]，如果缺少27，列表便是[28,29,30,...]接下来，获取它们的
    第一条记录，便是上一篇和下一篇文章；其中，__gt和__lt分别是大于和小于的意思，
    可以修饰到判断条件的字段上；exclude(is_published=False)用来排除没有发表的博客。
    """
    pre_article = Article.objects.exclude(is_published=False).filter(id__lt=current_article.id).order_by('-id')
    next_article = Article.objects.exclude(is_published=False).filter(id__gt=current_article.id).order_by('id')

    # 获取第一条记录
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None

    return pre_article, next_article


