
from rest_framework import viewsets,permissions,generics,status
from .models import (UserProfile,Category,Course,Lesson,Assignment,ExamQuestion,Variants,
                    ExamAnswer,Submission,Certificate,Question,Exam,
                     Review,Cart,CartItem,Favorite,Message)
from .serializers import (UserProfileSerializer, CategoryListSerializer, CategoryDetailSerializer, CourseListSerializer,CourseDetailSerializer,
                          LessonSerializer, AssignmentSerializer,
                          ExamQuestionSerializer, VariantsSerializer, ExamAnswerSerializer, SubmissionSerializer,
                          CertificateSerializer, QuestionSerializer, ExamSerializer,
                          ReviewSerializer, CartItemListSerializer,CartItemDetailSerializer, FavoriteListSerializer,
                          FavoriteDetailSerializer,MessageSerializer, UserSerializer, LoginSerializer, CartDetailSerializer)
from .permission import CheckAdminStatus,CheckOwner,CheckStudentStatus,CheckUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import CoursePagination
from .filter import CourseFilter

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckAdminStatus]

class CategoryListViewSet(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['name']


class CategoryDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['name']


class CourseListViewSet(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckAdminStatus]
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price','course_level']
    filterset_class = CourseFilter

class CourseDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckAdminStatus, CheckOwner]
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price','course_level']
    filterset_class = CourseFilter



class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    django_filters = [DjangoFilterBackend,SearchFilter]
    search_fields = ['title']


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ExamQuestionViewSet(viewsets.ModelViewSet):
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VariantsViewSet(viewsets.ModelViewSet):
    queryset = Variants.objects.all()
    serializer_class = VariantsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ExamAnswerViewSet(viewsets.ModelViewSet):
    queryset = ExamAnswer.objects.all()
    serializer_class = ExamAnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckAdminStatus]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckAdminStatus]

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckAdminStatus]



class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckStudentStatus,CheckUser]


class CartViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartItemListViewSet(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartItemDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class FavoriteListViewSet(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CheckAdminStatus]

class FavoriteDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteDetailSerializer
    permission_classes = [permissions.IsAuthenticated]



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
