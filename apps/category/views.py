from django.shortcuts import render
from django.views.generic import View

from .models import Category
from post.models import Article
from tools.views.paginate import getPages


class CategoryView(View):
    """
    博客分类
    """
    def get(self, request, category_id):
        categories = Category.objects.all()

        # filter(is_published=True)排除未发表文章，filter需要放到query后面？为什么？
        # article_category_list = Article.objects.query_by_category(category_id).filter(is_published=True).order_by('-created_time')
        if request.user.username == "chenzhixiang1992":
            article_category_list = Article.objects.filter(category_id=category_id).order_by('-created_time')
        else:
            article_category_list = Article.objects.filter(category_id=category_id, is_published=True).order_by('-created_time')
        pages, article_category_list = getPages(request, article_category_list, 10)

        data = {}
        data['categories'] = categories
        data['current_category_id'] = category_id
        data['pages'] = pages
        data['article_category_list'] = article_category_list
        return render(request, 'category/article_category_page.html', data)


class ArticleFilterView(View):
    """
    博客分类之后筛选
    """
    def get(self, request):
        categories = Category.objects.all()
        category_id = request.GET.get('current_category_id')
        post_filter_type = request.GET.get('post_filter_type')

        # filter(is_published=True)排除未发表文章，filter需要放到query后面？为什么？
        if post_filter_type == 'recommend':
            # article_category_list = Article.objects.filter(category_id=category_id, is_published=True, is_recommend=True).order_by('-created_time')
            sql = "SELECT post_article.* FROM `post_article` WHERE (`post_article`.`category_id` = %s AND `post_article`.`is_published` = True AND `post_article`.`is_recommend` = True) ORDER BY `post_article`.`created_time` DESC" % category_id
        elif post_filter_type =='hot_favorite':
            sql = "SELECT post_article.*, COUNT( `tools_favorite`.`favorite_id` ) AS `favorite_nums` FROM post_article LEFT OUTER JOIN `tools_favorite` ON ( `post_article`.`id` = `tools_favorite`.`favorite_id` AND ( `tools_favorite`.`favorite_type` = 1 ) ) WHERE `post_article`.`is_published` = TRUE AND `post_article`.`category_id` = %s GROUP BY post_article.id ORDER BY favorite_nums DESC" % category_id
        else:
            sql = "SELECT post_article.* FROM post_article LEFT JOIN ( SELECT * FROM django_comments WHERE content_type_id = 12 ) AS c ON post_article.id = c.object_pk WHERE `post_article`.`is_published` = TRUE AND `post_article`.`category_id` = %s GROUP BY post_article.id ORDER BY count( c.object_pk ) DESC" % category_id

        article_category_list = Article.objects.raw(sql)
        add_len_to_raw_query(article_category_list)
        pages, article_category_list = getPages(request, article_category_list, 10)

        data = {}
        data['categories'] = categories
        data['current_category_id'] = int(category_id)  # {% for category in categories %}中category.id为int，而category_id为str
        data['post_filter_type'] = post_filter_type
        data['pages'] = pages
        data['article_category_list'] = article_category_list
        return render(request, 'category/article_category_page.html', data)


#给rawqueryset对象加上len()方法
def add_len_to_raw_query(query):
    from django.db.models.query import RawQuerySet
    def __len__(self):
        from django.db import connection
        sql = 'select count(*) from (%s) as newsql' % query.raw_query
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchone()
        return row[0]
    setattr(RawQuerySet, '__len__', __len__)



