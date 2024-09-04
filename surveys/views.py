from django.shortcuts import render
from django.http import response
from django.utils.text import slugify
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListCreateAPIView,mixins
from .forms import RegisterForm,LoginForm
from .models import User,Survey,SurveyQuestion
from .serializers import UserSerializer,SurveySerializer,SurveyShellSerializer
import base64,os,re,uuid

# Create your views here.

def handle_image(base64Image, save_dir='media/images/surveys') ->str:
    # Extract MIME type and base64 data
    match = re.match(r'data:(.*?);base64,(.*)', base64Image)
    if match:
        mime_type = match.group(1)
        image_data = match.group(2)
        # Mime type confirm
        if mime_type not in ['image/jpeg', 'image/png', 'image/gif']:
            return Response({ 'detail': 'Unsupported image' }, status=status.HTTP_400_BAD_REQUEST)
        
        # Decode the imade
        image_bytes = base64.b64decode(image_data)

        # Filename
        filename = f"{uuid.uuid4()}.{mime_type.split('/')[1]}"
        file_path = os.path.join(save_dir, filename)
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as file:
            file.write(image_bytes)
            
        return file_path


class AuthRegister(APIView):
    def post(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            # Create new user
            cleaned_data = form.cleaned_data
            user = User(email=cleaned_data['email'], name=cleaned_data['fullname'])
            user.set_password(cleaned_data['password'])

            try:
                user.save()
                #TODO: add a cookie
                serializer = UserSerializer(user)
                return Response({ "user": serializer.data, "token": user.createToken() }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "error": str(e) }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AuthLogin(APIView):
    def post(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            try:
                user = User.objects.get(email=cleaned_data['email'])
            except User.DoesNotExist:
                return Response({"message": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if user.check_password(cleaned_data['password']):
                # TODO: Add a cookie
                serializer = UserSerializer(user, context={ 'request': request })
                return Response({
                    "user": serializer.data,
                    "token": user.createToken()
                }, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({ "message": "Invalid username or password" }, status=status.HTTP_401_UNAUTHORIZED)

        # Invalid data 
        else:
            return Response(form.errors)

class AuthUser(GenericAPIView):
    serializer_class = UserSerializer
    def put(self, request, pk=None):
        if pk is None:
            return Response({'detail': 'Not possible'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(pk=pk)
            data = request.data
            image = data.get('image')
            if image:
                user.image = handle_image(image, save_dir='media/images/users')
            
            user.save()
            serializer = UserSerializer(user, context= { 'request': request })
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        except User.DoesNotExist:
            return Response({'detail': 'No user found'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk=None):
        if pk is None:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True, context={ 'request': request })
            return Response(serializer.data)
        try:
            user = User.objects.get(pk=pk)
            return Response(UserSerializer(user, context={ 'request': request }).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'No user found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class SurveyAPIView(GenericAPIView):
    serializer_class = SurveySerializer

    def get(self, request, pk=None):
        # List all surveys
        if pk is None:
            surveys = Survey.objects.all()
            serializer = self.get_serializer(surveys, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                survey = Survey.objects.get(pk=pk)
                serializer = self.get_serializer(survey)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Survey.DoesNotExist:
                return Response({ 'detail': 'No survey found' }, status=status.HTTP_404_NOT_FOUND)
        
    
    def post(self, request, pk=None):
        if pk is not None:
            return Response({ 'detail': 'Method not allowed' }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        else:
            # Create a survey
            surveydata = request.data
            survey = Survey(title=surveydata.get('title'),
                            slug=slugify(surveydata.get('title')),
                            status=surveydata.get('status'),
                            expire_date=surveydata.get('expire_date'),
                            description=surveydata.get('description'),
                            )
            
            # Handle image 
            base64Image = surveydata.get('image', None)

            if base64Image:
                survey.image = handle_image(base64Image)

            # print(surveydata)
            survey.save()

            # Add survey questions
            questions_data:list = surveydata.get('questions') 
            if questions_data:
                for question in questions_data:
                    new_question = SurveyQuestion(
                        survey=survey,
                        type=question.get('type'),
                        question=question.get('question'),
                        description=question.get('description'),
                        data=question.get('data'),
                    )
                    new_question.save()

            serializer = self.get_serializer(survey)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def delete(self, request, pk=None):
        if pk is None:
            return Response({'detail': 'No way to do this!🤪'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        else:
            try:
                survey = Survey.objects.get(pk=pk)
                image = survey.image
                survey.delete()
                # Delete image file
                if image:
                    image_path = os.path.join(os.path.curdir, image)
                    if os.path.isfile(image_path):
                        os.remove(image_path)
                serializer = SurveyShellSerializer(survey)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            except Survey.DoesNotExist:
                return Response({'detail': 'No survey found'}, status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request, pk=None):
        if pk is None:
            return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            try:
                survey = Survey.objects.get(pk=pk)
                data = request.data
                
                # Update title + slug, status, description, expire_date
                title = data.get('title', None)
                if title:
                    survey.title = title
                    survey.slug = slugify(title)

                status_qn = data.get('status', None)
                if status_qn is not None:
                    survey.status = status_qn
                
                description = data.get('description', None)
                if description:
                    survey.description = description
                
                expire_date = data.get('expire_date', None)
                if expire_date:
                    survey.expire_date = expire_date
        
                # Handle image
                image = data.get('image', None)
                if image:
                    survey.image = handle_image(image)

                # Clear questions and add new ones
                SurveyQuestion.objects.filter(survey=survey).delete()

                #New questions
                questions_data = data.get('questions', [])

                for question_data in questions_data:
                    question = SurveyQuestion(
                        survey=survey,
                        type=question_data.get('type'),
                        question=question_data.get('question'),
                        description=question_data.get('description'),
                        data=question_data.get('data'),
                    )
                    question.save()

                survey.save()
                serializer = self.get_serializer(survey)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            except Survey.DoesNotExist:
                return Response({'detail': 'No survey with this id, no action taken'}, status=status.HTTP_404_NOT_FOUND)
