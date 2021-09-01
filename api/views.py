import uuid

from api_yamdb.settings import EMAIL_ADMIN
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django_filters import rest_framework as dfilters
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User, UserConfirmationCode
from .permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnlyPermission,
                          IsSuperuserPermission)
from .serializers import (CategorySerializer, CommentViewSerializer,
                          EmailConfirmCodeSerializer, EmailSerializer,
                          GenreSerializer, ReviewViewSerializer,
                          TitleCreateSerializer, TitleGetSerializer,
                          UserSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentViewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnlyPermission]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewViewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnlyPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['score', ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(title=title, author=self.request.user)


class BaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    http_method_names = ['get', 'post', 'delete']


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [dfilters.DjangoFilterBackend]
    filterset_class = TitleFilter
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleGetSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperuserPermission,)
    lookup_field = 'username'

    def perform_update(self, serializer):
        if 'role' in serializer.validated_data:
            if serializer.validated_data['role'] == User.ADMIN:
                serializer.save(is_superuser=True)
            else:
                serializer.save(is_superuser=False)
        else:
            serializer.save()

    @action(methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated],
            url_path='me',
            url_name='me',
            detail=False)
    def me(self, request):
        serializer = UserSerializer(self.request.user)
        if self.request.method == 'PATCH':
            serializer = UserSerializer(
                self.request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetConfirmationCodeByMail(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = str(uuid.uuid4())
        validated_email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=validated_email)
        except User.DoesNotExist:
            user = User(
                username=slugify(validated_email),
                email=validated_email,
            )
            user.save()
        if user.confirm_code.exists():
            user.confirm_code.all().delete()
        user_cc = UserConfirmationCode(
            user=user,
            confirmation_code=confirmation_code
        )
        user_cc.save()
        if user.is_superuser:
            user.role = User.ADMIN
            user.save()
        send_mail(
            'Confirmation_code for YaMDB',
            f'confirmation_code = {confirmation_code}',
            EMAIL_ADMIN,
            [validated_email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenForEmail(APIView):
    def post(self, request):
        serializer = EmailConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data['email'])
        user_confirm_code = user.confirm_code.values()[0][
            'confirmation_code'
        ]

        if user_confirm_code == serializer.data['confirmation_code']:
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )

        return Response(
            {'confirmation_code': ['Enter a valid confirmation code.']},
            status=status.HTTP_400_BAD_REQUEST)
