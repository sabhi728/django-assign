from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import FAQ
from .serializer import FaqSerializer

@api_view(['GET'])
def faq(request):
    lang = request.query_params.get("lang")
    question = request.data.get('question')
    faqObj = faq.objects.filter(question__icontains=question)
    data = FaqSerializer(faqObj, many = True)
    if lang == 'En':
        return JsonResponse({'data':data},status=201)
        


    return Response
