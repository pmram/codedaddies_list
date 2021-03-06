import requests
import lxml
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import Search

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"

# Create your views here.
def home(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search = search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='lxml')
    post_listings = soup.find_all('li',{'class':'result-row'})

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url =  post.find('a').get('href')
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = "https://idsb.tmgrup.com.tr/ly/uploads/images/2020/03/12/24934.jpg"
        node = post.find(class_='result-price')
        if node is not None:
            post_price = node.text
        else:
            post_price = 'N/A'

        final_postings.append((post_title,post_url,post_price,post_image_url))


    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'new_search.html',context=stuff_for_frontend)
