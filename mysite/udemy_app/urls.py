
from django.urls import include,path
from rest_framework import routers
from .views import (UserProfileViewSet,CategoryListViewSet,CategoryDetailViewSet,CourseListViewSet,CourseDetailViewSet,LessonViewSet,AssignmentViewSet,
                    ExamQuestionViewSet,VariantsViewSet,ExamAnswerViewSet,SubmissionViewSet,CertificateViewSet,QuestionViewSet,ExamViewSet,ReviewViewSet,
                    CartViewSet,CartItemListViewSet,CartItemDetailViewSet,FavoriteListViewSet,FavoriteDetailViewSet,MessageViewSet,
                    CustomLoginView,RegisterView,LogoutView)


router =routers.DefaultRouter()
router.register(r'user_profile', UserProfileViewSet, basename='user_profile'),
router.register(r'lesson', LessonViewSet, basename='lesson'),
router.register(r'assignment', AssignmentViewSet, basename='assignment'),
router.register(r'exam_question', ExamQuestionViewSet, basename='exam_question'),
router.register(r'variants', VariantsViewSet, basename='variants'),
router.register(r'exam_answer', ExamAnswerViewSet, basename='exam_answer'),
router.register(r'submission', SubmissionViewSet, basename='submission'),
router.register(r'certificate', CertificateViewSet, basename='certificate'),
router.register(r'question', QuestionViewSet, basename='question'),
router.register(r'exam', ExamViewSet, basename='exam'),
router.register(r'review', ReviewViewSet, basename='review'),
router.register(r'message', MessageViewSet, basename='message')

urlpatterns = [
    path('',include(router.urls)),

    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('category/', CategoryListViewSet.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailViewSet.as_view(), name='category_detail'),

    path('course/', CourseListViewSet.as_view(),name='course_list'),
    path('course/<int:pk>/', CourseDetailViewSet.as_view(), name='course_detail'),

    path('cart/<int:pk>/',CartViewSet.as_view(),name='cart_detail'),

    path('cart_item/', CartItemListViewSet.as_view(), name='cart_item_list'),
    path('cart_item/<int:pk>/', CartItemDetailViewSet.as_view(), name = 'cart_item_detail'),

    path('favorite/', FavoriteListViewSet.as_view(), name='favorite_list'),
    path('favorite/<int:pk>/', FavoriteDetailViewSet.as_view(), name = 'favorite_detail')




]
