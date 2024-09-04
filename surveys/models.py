from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a 'User' with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=128)  # Adjusted for hashed password
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Required fields for createsuperuser

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='surveys_user_set',  # Change related_name here
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='surveys_user_permissions',  # Change related_name here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email
    
    def createToken(self) -> str:
        #TODO: Generate a jwt
        return f"token:{self.name},{self.email}"


class Survey(models.Model):
    user = models.ForeignKey(User, null=True ,on_delete=models.PROTECT, related_name='user_surveys')
    title = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    image = models.URLField(null=True, default=None, blank=True)
    status = models.BooleanField(default=False)
    description = models.TextField(null=True)
    expire_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.status}"

class SurveyQuestion(models.Model):
    type = models.CharField(max_length=50)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.CharField(max_length=2000)
    description = models.TextField(null=True)
    data = models.JSONField(default=dict, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.question}"

class SurveyAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

class SurveyQuestionAnswer(models.Model):
    answer_text = models.TextField()
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(SurveyAnswer, models.CASCADE)
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
