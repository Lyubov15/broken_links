from django.shortcuts import render
from django.http import HttpResponse
from .models import Page, Link, Error
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'analyzer/home.html', {})

def analyze_page(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        # Проверяем, что URL начинается с http:// или https://
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        try:
            page = Page.objects.create(url=url)
            logger.info(f"Начало анализа страницы: {url}")
            
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                is_valid = True
                
                if not soup.find('html') or not soup.find('body'):
                    is_valid = False
                    Error.objects.create(page=page, description="Отсутствует тег <html> или <body>")
                
                page.is_valid_html = is_valid
                page.save()
                
                # Получаем домен текущего URL для сравнения
                base_domain = urlparse(url).netloc
                
                links = soup.find_all('a', href=True)
                logger.info(f"Найдено {len(links)} ссылок на странице")
                
                for link in links:
                    href = link['href']
                    # Преобразуем относительные ссылки в абсолютные
                    absolute_url = urljoin(url, href)
                    
                    # Определяем тип ссылки, сравнивая домены
                    parsed_url = urlparse(absolute_url)
                    link_domain = parsed_url.netloc
                    
                    # Если домены разные или ссылка на внешний ресурс - считаем внешней
                    link_type = 'external' if link_domain and link_domain != base_domain else 'internal'
                    
                    try:
                        # Проверяем только абсолютные URL
                        if absolute_url.startswith(('http://', 'https://')):
                            link_response = requests.head(absolute_url, timeout=5, allow_redirects=True)
                            status = link_response.status_code
                        else:
                            status = 0
                    except Exception as e:
                        logger.warning(f"Ошибка при проверке ссылки {absolute_url}: {str(e)}")
                        status = 0
                    
                    Link.objects.create(page=page, url=absolute_url, link_type=link_type, status_code=status)
                
                context = {'page': page, 'links': page.links.all(), 'errors': page.errors.all()}
                return render(request, 'analyzer/results.html', context)
                
            except requests.RequestException as e:
                Error.objects.create(page=page, description=f"Ошибка запроса: {str(e)}")
                return HttpResponse(f"Ошибка при запросе страницы: {str(e)}")
                
        except Exception as e:
            logger.error(f"Критическая ошибка при анализе {url}: {str(e)}")
            return HttpResponse(f"Ошибка анализа страницы: {str(e)}")
    
    return render(request, 'analyzer/analyze.html', {})

# Create your views here.
