from django.urls import path
from .import views

urlpatterns=[
    path('',views.Home,name="home"),
    path('register',views.Register,name="reg"),
    path('login',views.Login_page,name="login"),
    path('logout',views.Logout_page,name="logout"),
    path('cart', views.Cart_page, name="cart"),
    path('fav', views.Wishlist_page, name="fav"),
    path('favviewpage', views.Wishlist_Viewpage, name="favviewpage"),
    path('remove_fav/<str:fid>', views.Remove_fav, name="remove_fav"),
    path('remove_cart/<str:cid>',views.Remove_cart,name="remove_cart"),
    path('collections',views.Collection,name="collect"),
    path('collections/<str:name>',views.CollectionView,name="collects"),
    path('collections/<str:cname>/<str:pname>',views.ProductDetails,name="product_details"),
    path('addtocart', views.Add_to_cart, name="addtocart"),
    path('blog', views.Blog_page, name="blog"),
    path('about', views.About_page, name="about"),
    path('faq', views.Faq_page, name="faq"),

]