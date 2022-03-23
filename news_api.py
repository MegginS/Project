import requests

with open('news_key.txt') as f:
    api_key = f.readline().strip()

def news_api_results():
    news_payload = {
                'q': 'palm oil deforestation',
                'from': '2022-02-28',
                'apiKey': api_key,
                'sortBy': 'relevancy',
                'pageSize': '30'
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
        if article["news_source"] != "Reuters":
            if "palm oil" in description or "deforestation" in description:
                all_articles.append(article)

    return all_articles
   