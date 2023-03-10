from django.urls import path
from .views import CreateProductView,CreateCategoryView,CategoryList, ProductDetailAPI,ProductOfferList, CartItemList,AddToCartView, userCreate,ContactCreate,AdminContactList,ProductDelete,UpdateProductView,LogoutAPIView

from .views import productFilterView,EmailView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [ 
   
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-register/', userCreate.as_view(), name='user-register'),

   path('create-category/', CreateCategoryView.as_view(), name='create-catogory'),
   path('create-product/', CreateProductView.as_view(), name='create-product'),
   path('update-product/<int:pk>', UpdateProductView.as_view(), name='update-product'),
   path('categories/',CategoryList.as_view(), name='catogories'),
   path('products/',productFilterView.as_view(), name='products'),#search sort ...
   path('products-detail/<int:pk>/', ProductDetailAPI.as_view(), name='products-detail'),

   path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
   path('products/offers/', ProductOfferList.as_view(), name='product-offer-list'),
    path('cart/<int:user_id>', CartItemList.as_view(), name='cart-list'),
    path('cart/checkout/', EmailView.as_view(), name='checkout'),
    path('contacts/create/', ContactCreate.as_view(), name='contact-create'),
    path('contacts/', AdminContactList.as_view(), name='admin-contact-list'),
    path('products/delete/<int:pk>/',ProductDelete.as_view(), name='product-delete'),
    path('logout/', LogoutAPIView.as_view(),name="logout"),

]