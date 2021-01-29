from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    # Users URLS 
    path('all-users/', views.ListAllUserAPI.as_view(), name='list-all-users'),
    path('delete-user/<int:user_id>/', views.DeleteUserAPI.as_view(), name='delete-user'),
    path('block-user/<int:user_id>/', views.ToggleBlockUserAPI.as_view(), name='toggle-block-user'),
    path('golden-user/<int:user_id>/', views.ToggleGoldenUserAPI.as_view(), name='toggle-golden-user'),
    path('login/', views.DashboardLoginAPIView.as_view(), name='login'),
    path('update-user/<int:pk>/', views.DashboardUpdateUserAPI.as_view(), name='update-user'),
    path('change-password/', views.ChangePasswordAPI.as_view(), name='change-password'),
    
    # Products URLS
    path('all-products/', views.ListAllProductAPI.as_view(), name='list-all-products'),
    path('delete-product/<int:product_id>/',views.DeleteProductAPI.as_view(), name='delete-product'),
    path('comments/<int:product_id>/', views.ListCommentsForProduct.as_view(), name='list-comment-for-product'),
    path('delete-comment/<int:comment_id>/', views.DeleteCommentAPI.as_view(), name='delete-comment'),
    path('update-product/<int:pk>/', views.UpdateProductAPI.as_view(), name='update-product'),
    path('delete-product-image/<int:product_image_id>/', views.DeleteProductImage.as_view(), name='delete-product-image'),

    # RateProduct URLS
    path('all-rated-product/',views.ListAllRateProductAPI.as_view(), name='all-rated-product'),
    path('push_rate_message/<int:rate_product_id>/',views.SendRatingProductMessage.as_view(),name='push_rate_message'),
    path('rate/<int:rate_product_id>/',views.CreateRatingForProduct.as_view(), name='rate-product'),
    path('update-rate-product/<int:pk>/', views.UpdateRateProduct.as_view(), name='update-rate-product'),
    path('delete-rate-image/<int:rate_product_image_id>/',views.DeleteRateProductImage.as_view(), name='delete-rate-product-image'),

    # Reviews URLS
    path('all-reviews/', views.ListAllReviews.as_view(), name='list-all-reviews'),
    path('approve-review/<int:review_id>/',views.ToggleApproveReview.as_view(), name='approve-review'),
    path('delete-review/<int:review_id>/',views.DeleteReviewAPI.as_view(), name='delete-review'),

    # Categories URLS
    path('add-category/', views.AddCategoryAPI.as_view(), name='add-category'),
    path('categories/', views.ListAllCategory.as_view(), name='list-categories'),
    path('subcategories/', views.ListAllSubcategory.as_view(), name='list-subcategories'),
    path('add-subcategory/', views.AddSubcategoryAPI.as_view(), name='add-subcategory'),
    path('subcategories/<int:category_id>/',views.ListSubcategoriesOfCategory.as_view(), name='list-subcategories-category'),

    # Cart URLS
    path('ordered-carts/', views.GetAllOrderedCart.as_view(), name='ordered-cart'),
]