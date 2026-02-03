from django.db import models
from django.contrib.auth.models import  AbstractUser


class UserProfile(AbstractUser):
    USER_ROLE = (
    ('Студент','Студент'),
    ('Предподаватель','Предподаватель'),
    )
    user_role = models.CharField(max_length=20, choices=USER_ROLE)
    full_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_picture/')
    bio = models.TextField()

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teacher_course')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True, related_name='category')
    title = models.CharField(max_length=50)
    course_image = models.ImageField(upload_to='course_image')
    video = models.FileField(null=True,blank=True)
    description = models.TextField()
    COURSE_LEVEL = (
    ('Начальный','Начальный'),
    ('Средний','Средний'),
    ('Продвинутый','Продвинутый')
    )
    course_level = models.CharField(max_length=15, choices=COURSE_LEVEL)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits = 7,
        decimal_places=2,
        null=True,
        blank=True,
        default=0

    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def get_avg_rating(self):
        review = self.review.all()
        if review.exists():
            return sum([i.stars for i in review]) / review.count()
        return 0

    def get_count_rating(self):
        review = self.review.all()
        if review.exists():
            return review.count()
        return 0



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    video = models.FileField(upload_to='video/')
    order = models.PositiveSmallIntegerField(default=1)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}:{self.course}'


class Assignment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}:{self.user}'



class Submission(models.Model):

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='submission_file/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.assignment}:{self.user}'



class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title =models.TextField(blank=True)
    question_image = models.FileField(upload_to='question_image/', null=True, blank=True)

    def __str__(self):
        return f'{self.title}:{self.course}'




class Exam(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    passing_score = models.PositiveSmallIntegerField(default=60)
    duration = models.PositiveSmallIntegerField(default=0)


    def __str__(self):
        return f'{self.title}:{self.course}:{self.question}'




class ExamQuestion(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question_image = models.FileField(upload_to='question_image/')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title}:{self.teacher}:{self.exam}'



class Variants(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teacher')
    exam = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    VARIANTS_CHOICES = (
    ('А','А'),
    ('Б','Б'),
    ('В','В')
    )
    variant = models.CharField(max_length=5, choices= VARIANTS_CHOICES)
    variant_text = models.TextField()
    true_variant = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.teacher}:{self.exam}'


class ExamAnswer(models.Model):
    students = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='student')
    variants = models.ForeignKey(Variants, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.students}:{self.variants}'





class SubmissionAnswer(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    grade = models.DecimalField(decimal_places=30, max_digits=100)

    STATUS_CHOICES = [
        ('Аткарган жок', 'Аткарган жок'),
        ('Аткарды','Аткарды')
    ]
    status_choices = models.CharField(max_length=15, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.teacher}:{self.submission}'




class Certificate(models.Model):
    student = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at =models.DateTimeField(auto_now_add=True)
    certificate_url = models.FileField()

    def __str__(self):
        return f'{self.student}:{self.course}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='review')
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user}:{self.course}:{self.stars}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}:{self.created_at}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cart}:{self.course}'



class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='student_favorite')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}:{self.course}'


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='user_receiver')
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}:{self.receiver}:{self.course}'








