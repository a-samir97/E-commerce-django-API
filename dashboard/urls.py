from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # Users URLS 
    path('all-users/', views.ListAllUserAPI.as_view(), name='list-all-users'),
    path('delete-user/<int:user_id>/', views.DeleteUserAPI.as_view(), name='delete-user'),
    path('block-user/<int:user_id>/', views.ToggleBlockUserAPI.as_view(), name='toggle-block-user'),
    path('golden-user/<int:user_id>/', views.ToggleGoldenUserAPI.as_view(), name='toggle-golden-user'),

    # Products URLS
    path('all-products/', views.ListAllProductAPI.as_view(), name='list-all-products'),
    path('delete-product/<int:product_id>/',views.DeleteProductAPI.as_view(), name='delete-product'),
    path('comments/<int:product_id>/', views.ListCommentsForProduct.as_view(), name='list-comment-for-product'),
    path('delete-comment/<int:comment_id>/', views.DeleteCommentAPI.as_view(), name='delete-comment'),

    # RateProduct URLS
    path('all-rated-product/',views.ListAllRateProductAPI.as_view(), name='all-rated-product'),
    path('rate/<int:rate_product_id>/',views.CreateRatingForProduct.as_view(), name='rate-product'),

    # Reviews URLS
    path('all-reviews/', views.ListAllReviews.as_view(), name='list-all-reviews'),
    path('approve-review/<int:review_id>/',views.ToggleApproveReview.as_view(), name='approve-review')
]