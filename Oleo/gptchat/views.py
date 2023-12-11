from django.http import HttpResponse
from django.shortcuts import render
from openai import OpenAI
import requests

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import DishSerializer, IngredientSerializer
from .models import Dish  # Предположим, что у вас есть модель для блюд
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from urllib.parse import urlparse
from django.core.files.storage import default_storage
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
import os





client = OpenAI(
    api_key='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'
)



class DishCreateView(APIView):
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = IngredientSerializer(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['products']

            chat_completion = client.chat.completions.create(
                model='gpt-3.5-turbo-1106',
                messages=[
                    {
                        'role': 'system',
                        'content': "tell me a dish that can be prepared from these products",
                    },
                    {
                        'role': 'user',
                        'content': input_text,
                    },
                ],
                temperature=1,
                max_tokens=1000
            )

            response_data = {'text': chat_completion.choices[0].message.content}
            imagestr = str(response_data)
            response = client.images.generate(
                model="dall-e-3",
                prompt=imagestr,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            filename = os.path.basename(urlparse(image_url).path)

            # Сохраняем изображение в папку media
            file_path = os.path.join('media', filename)
            with default_storage.open(file_path, 'wb') as destination:
                response = requests.get(image_url, stream=True)
                for chunk in response.iter_content(chunk_size=128):
                    destination.write(chunk)

            dish = Dish(user=request.user, recipe=response_data, image=image_url)
            dish.save()

            # Возвращаем Response с данными о созданном блюде
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Возвращаем Response с ошибками валидации
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DishSerializer
    queryset = Dish.objects.all()


class FoodDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DishSerializer
    queryset = Dish.objects.all()


class ImageView(APIView):
    def get(self, image_url):
        try:
            # Загружаем изображение по URL
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            # Возвращаем изображение как HttpResponse
            return HttpResponse(response.content, content_type=response.headers['Content-Type'])
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Error: {str(e)}", status=500)