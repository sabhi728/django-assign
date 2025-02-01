from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import FAQ
from .serializer import FaqSerializer
from googletrans import Translator
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def translator(text, dest_lang):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=dest_lang)
        return translation.text
    
    except Exception as e:
        print("Exception raised in translator method:",str(e))
        raise e

@api_view(['GET'])
def fetch_faq(request):
    lang = request.query_params.get("lang", 'en')
    question = request.data.get('question', "").strip()
    
    cache_key = f"faq_{lang}_{question}"
    
    cached_response = cache.get(cache_key)
    if cached_response is not None:
        return JsonResponse({'data': cached_response}, status=200)
    
    try:
        if lang != 'en' and len(question) > 0:
            question = translator(question,"en")
        faqObj = FAQ.objects.filter(question__icontains=question)
        data = FaqSerializer(faqObj, many=True).data
        
        if lang == 'en' or not data:
            cache.set(cache_key, data, timeout=CACHE_TTL)
            return JsonResponse({'data': data}, status=200)
        
        for faq in data:
            faq['question'] = translator(text=faq['question'], dest_lang=lang)
            faq['answer'] = translator(text=faq['answer'], dest_lang=lang)
        
        cache.set(cache_key, data, timeout=CACHE_TTL)
        return JsonResponse({'data': data}, status=200)

    except Exception as e:
        print('Exception raised in faq method:', e)
        return JsonResponse({'error': str(e)}, status=500)
