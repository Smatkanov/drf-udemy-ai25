from rest_framework import serializers

from .models import (UserProfile,Category,Course,Lesson,Assignment,ExamQuestion,Variants,ExamAnswer,
                     Submission,Certificate,Question,Exam,
                     Review,Cart,CartItem,Favorite,Message)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username','user_role','bio']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','full_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]

class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id','user']

class FavoriteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id','user','course','added_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'stars','comment']

class CourseListSerializer(serializers.ModelSerializer):
    teacher = UserProfileSerializer()
    category = CategoryListSerializer()
    favorite = FavoriteListSerializer(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id','course_image', 'title', 'get_avg_rating','get_count_rating', 'teacher','category','title','price','favorite',]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()




class CategoryDetailSerializer(serializers.ModelSerializer):
    category = CourseListSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ['id','name', 'category']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestion
        fields = '__all__'


class VariantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variants
        fields = '__all__'


class ExamAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAnswer
        fields = '__all__'



class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class CartItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart','course','added_at']

class CartItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart','course','added_at']


class CartDetailSerializer(serializers.ModelSerializer):
    cart = CartItemListSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = ['user','created_at','cart']



class CourseDetailSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['teacher','category','title','video','get_avg_rating','get_count_rating','description','course_level','is_paid',
                  'price','review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'