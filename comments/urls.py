from django.urls import path

from .views import CommentAPIViewSet

app_name = 'comments'

comments_list = CommentAPIViewSet.as_view({'get': 'list'})
create_comment = CommentAPIViewSet.as_view({'post': 'create'})

comment_details = CommentAPIViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
    'get':'retrieve'
})

urlpatterns = [
    path('all/<int:product_id>', comments_list, name='comments-list'),
    path('new/<int:product_id>', create_comment, name='create-comment'),
    path('<int:pk>', comment_details, name='comment-details')
]