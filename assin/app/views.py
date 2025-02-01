from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import FAQ
from .serializer import FaqSerializer
from googletrans import Translator

def translator(text, dest_lang):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    return translation.text

@api_view(['GET'])
def faq(request):
    try:
        lang = request.query_params.get("lang",'en')
        question = request.data.get('question')
        faqObj = faq.objects.filter(question__icontains=question)
        data = FaqSerializer(faqObj, many = True)
        if lang == 'en':
            return JsonResponse({'data':data},status=201)
        else:
            for index in len(data):
                faq = data[index]
                data[index]['question'] = translator(text=faq.question,dest_lang=lang)
                data[index]['answer'] = translator(text=faq.answer, dest_lang=lang)
            return JsonResponse({'data':data},status=201)
    except Exception as e:
        print('Exception raised at methode faq',e)
        return JsonResponse({'error':str(e)},status=401)
