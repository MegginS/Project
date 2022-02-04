import requests
import re



def news_api_results():
    news_payload = {
                'q': 'Palm Oil deforestation',
                'from': '2022-01-15',
                'apiKey': '7873c5eaa73d4b5d935a47b3422c93ca',
                'sortBy': 'relevancy',
                'pageSize': '10'
                }

    news_search = requests.get('https://newsapi.org/v2/everything', params = news_payload )
    news_result = news_search.json()

    articles = news_result['articles']

    all_articles=[]
    for i in range(len(articles)):
        news_source = news_result['articles'][i].get('source').get('name')
        author = news_result['articles'][i].get('author')
        title = news_result['articles'][i].get('title')
        description = news_result['articles'][i].get('description')
        url = news_result['articles'][i].get('url')
        urlimage = news_result['articles'][i].get('urlToImage')

        article = {"news_source": news_source, "author": author, "title": title, "description": description, "url": url, "urlimage": urlimage}
        all_articles.append(article)

    return all_articles
   