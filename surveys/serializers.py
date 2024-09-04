from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import User,Survey,SurveyQuestion

class UserSerializer(ModelSerializer):
    image = SerializerMethodField()
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups']

    def get_image(self, obj):
        image_path = obj.image
        if image_path is None:
            return
        if image_path.startswith('http://') or image_path.startswith('https://'):
            return image_path
        else:
            image_path = f"/{image_path}"
        return self.context['request'].build_absolute_uri(image_path)


class SurveyQuestionSerializer(ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = '__all__'

class SurveySerializer(ModelSerializer):
    questions = SurveyQuestionSerializer(many=True, read_only=True, source='surveyquestion_set')
    image = SerializerMethodField()
    class Meta:
        model = Survey
        fields = '__all__'
    
    def get_image(self, obj):
        image_path = obj.image
        if image_path is None:
            return
        if image_path.startswith('http://') or image_path.startswith('https://'):
            pass
        else:
            image_path = f"/{image_path}"

        return (self.context['request'].build_absolute_uri(image_path)) if obj.image else None

class SurveyShellSerializer(ModelSerializer):
    class Meta:
        model = Survey
        exclude = ['id']
        