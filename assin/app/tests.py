import pytest
import json
from django.http import JsonResponse
from unittest.mock import Mock, patch
from rest_framework.test import APIRequestFactory
from app.views import translator, fetch_faq
from app.models import FAQ
from django.core.cache import cache

@pytest.fixture
def mock_translator():
    with patch('app.views.Translator') as mock:
        translator_instance = Mock()
        mock.return_value = translator_instance
        yield translator_instance

@pytest.fixture
def factory():
    return APIRequestFactory()

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield

def test_translator_success(mock_translator):
    mock_translator.translate.return_value = Mock(text="Hello")
    result = translator("Hola", "en")
    assert result == "Hello"
    mock_translator.translate.assert_called_once_with("Hola", dest="en")

def test_translator_exception(mock_translator):
    mock_translator.translate.side_effect = Exception("Translation error")
    with pytest.raises(Exception) as exc_info:
        translator("Hello", "es")
    assert str(exc_info.value) == "Translation error"

@pytest.mark.django_db
def test_fetch_faq_english(factory):
    FAQ.objects.create(question="What is Python?", answer="Python is a programming language")
    request = factory.get('/api/faqs/', {'lang': 'en'})
    response = fetch_faq(request)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    data = json.loads(response.content)["data"]
    assert len(data) == 1
    assert data[0]["question"] == "What is Python?"

@pytest.mark.django_db
def test_fetch_faq_translated(factory, mock_translator):
    FAQ.objects.create(question="What is Python?", answer="Python is a programming language")
    request = factory.get('/api/faqs', {'lang': 'hi'})

    def mock_translate(text, dest):
        translations = {
            ("पायथन क्या है?", "en"): Mock(text="What is Python?"),
            ("What is Python?", "hi"): Mock(text="पायथन क्या है?"),
            ("Python is a programming language", "hi"): Mock(text="पाइथन एक प्रोग्रामिंग भाषा है")
        }
        return translations.get((text, dest), Mock(text=text))

    mock_translator.translate.side_effect = mock_translate
    response = fetch_faq(request)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    data = json.loads(response.content)["data"]
    assert len(data) == 1
    assert data[0]["question"] == "पायथन क्या है?"
    assert data[0]["answer"] == "पाइथन एक प्रोग्रामिंग भाषा है"

@pytest.mark.django_db
def test_fetch_faq_error(factory, mock_translator):
    FAQ.objects.create(question="What is Python?", answer="Python is a programming language")
    request = factory.get('/api/faqs/', {'lang': 'es'})
    mock_translator.translate.side_effect = Exception("Translation error")
    response = fetch_faq(request)
    assert isinstance(response, JsonResponse)
    assert response.status_code == 500
    error_data = json.loads(response.content)
    assert "error" in error_data

@pytest.mark.django_db
def test_fetch_faq_caching(factory):
    faq = FAQ.objects.create(question="What is Python?", answer="Python is a programming language")
    request = factory.get('/api/faqs/', {'lang': 'en'})
    response1 = fetch_faq(request)
    data1 = json.loads(response1.content)["data"]
    FAQ.objects.all().delete()
    response2 = fetch_faq(request)
    data2 = json.loads(response2.content)["data"]
    assert data1 == data2
