from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('genres', views.GenreViewSet)
router.register('categories', views.CategoryViewSet)
router.register('titles', views.TitleViewSet)
router.register('users', views.UsersViewSet)

router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet, basename='Review')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments',
                views.CommentViewSet, basename='Comment')

urlpatterns = [
    path('v1/', include([path('auth/email/',
                              views.GetConfirmationCodeByMail.as_view()),
                         path('auth/token/',
                              views.GetTokenForEmail.as_view())])),
    path('v1/', include(router.urls)),
]
