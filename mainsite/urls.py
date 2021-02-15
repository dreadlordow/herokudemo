from django.urls import path
from mainsite.views import categories_view, search_view, cart_view, index_views, create_product_view, profile_view, \
    edit_view, \
    delete_item_view, checkout_view, admin_view
from mainsite.views.categories_view import search_in_category
from mainsite.views.change_profile_picture_view import change_profile_picture
from mainsite.views.index_views import IndexView
from mainsite.views.profile_view import ProfileUpdate
from mainsite.views.search_view import SearchView

urlpatterns = [
    #path('', index_views.index, name='index'),
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>', index_views.product, name='product'),
    path('product/<int:pk>/<str:slug>/', index_views.product, name='product'),
    path('create/', create_product_view.create_product, name='create'),
    path('profile/<str:slug>/', profile_view.profile, name='profile'),
    path('cart/<int:pk>', cart_view.add_to_cart, name='add_to_cart'),
    path('edit/<int:pk>', edit_view.edit, name='edit_item'),
    path('remove/<int:pk>', cart_view.remove_from_cart, name='remove_from_cart'),
    #path('search/', search_view.search, name='search'),
    path('search/', SearchView.as_view(), name='search'),
    path('category/<str:category>', categories_view.category_view, name='category_view'),
    path('delete/<int:pk>', delete_item_view.delete, name='delete item'),
    path('checkout', checkout_view.checkout, name='checkout'),
    path('order/<int:pk>', checkout_view.order, name='order'),
    path('admin_page/', admin_view.admin_view, name='admin view'),
    #path('change_profile_picture/<int:pk>', change_profile_picture, name='change pfp'),
    path('change_profile_picture/<str:slug>/<int:pk>', change_profile_picture, name='change pfp'),
    path('update_profile/<int:pk>', ProfileUpdate.as_view(), name='update profile'),
    path('category/<str:category>/search/', search_in_category, name='search in category'),
    #path('search/', )

]