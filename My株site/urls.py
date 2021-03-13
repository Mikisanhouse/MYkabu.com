from django.urls import path, include
from .views import HomePage, Company, Signup, Login, Logout,  Result, Favorite_List, Favorite_Company, img_plot_company, Favorite_Create, img_plot_reslut, Board, Board_detail, Board_create, img_plot_board, Favorite_code_delete, Board_delete

urlpatterns = [
    path('', HomePage, name='homepage'),
    path('company/', Company, name='company'),
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('result/', Result, name='result'),
    path('favorite_list/', Favorite_List, name='favorite_list'),
    path('favorite_list/delete/<int:pk>', Favorite_code_delete.as_view(),
         name='favorite_code_delete'),
    path('favorite_company/<int:pk>', Favorite_Company, name='favorite_company'),
    path('company/plot', img_plot_company, name='img_plot'),
    path('board/plot/<int:pk>', img_plot_board, name='img_plot_board'),
    path('company/favorite_create/', Favorite_Create, name='favorite_create'),
    path('result/plot', img_plot_reslut, name='img_plot_reslut'),
    path('board/', Board, name='board'),
    path('board/delete/<int:pk>', Board_delete.as_view(), name='board_delete'),
    path('board/<int:pk>', Board_detail, name='board_detail'),
    path('create/', Board_create.as_view(), name='create'),
]
