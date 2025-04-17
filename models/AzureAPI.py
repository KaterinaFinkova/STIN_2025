import time
import requests
from statistics import mean
from .StockInfo import StockInfo
from .News import News
from typing import List

class AzureAPI:
    def __init__(self, azure_key: str, max_documents_per_request: int = 10):
        self.azure_key = azure_key
        self.azure_endpoint = "https://stocknews.cognitiveservices.azure.com/text/analytics/v3.0/sentiment"
        self.max_documents_per_request = max_documents_per_request

    def _getScoresFromDocuments(self, sentiment_data):
        scores = []
        
        for document in sentiment_data['documents']:
            positive_score = document['confidenceScores']['positive']
            negative_score = document['confidenceScores']['negative']
            

            score = (positive_score - negative_score) * 10
            
            scores.append(score)
        
        return scores

    def _getSentimentBatch(self, articles: List[str], retry_time=10) -> dict:
        headers = {
            "Ocp-Apim-Subscription-Key": self.azure_key,
            "Content-Type": "application/json"
        }
        
        documents = [{"id": str(i + 1), "language": "en", "text": article} for i, article in enumerate(articles)]
        payload = {"documents": documents}

        response = requests.post(self.azure_endpoint, headers=headers, json=payload)
        
        retry = 0
        if response.status_code != 200 :
            if response.status_code == 449 :
                retry = 1
                print(f"Rate limit exceeded. Retrying after {retry_time} seconds...")
                time.sleep(retry_time)
            
            if response.status_code != 200 :
                raise Exception(f"Error from Azure API: {response.status_code}, {response.text}")
        
        return retry, self._getScoresFromDocuments(response.json())
    
    def _getSentimentsForAll(self, articles: List[str], max_retries=10) -> List[dict]:
        all_results = []
        
        retries = 0
        for i in range(0, len(articles), self.max_documents_per_request):
            batch = articles[i:i + self.max_documents_per_request]
            retry, result = self._getSentimentBatch(batch)
            all_results.extend(result)
            retries += retry

            if retries > max_retries :
                raise Exception(f"Error from Azure API: too many retries")
        
        return all_results
    
    def getSentimentAnalysis(self, news: News, stockList: List[StockInfo]):
        indices = []
        all_articles = []
        
        for stock_info in stockList:
            company_name = stock_info.get_name()
            company_articles = [article.getText() for article in news.getArticles(company_name)]
            all_articles.extend(company_articles)
            indices.append(len(company_articles))
        
        sentiment_scores = self._getSentimentsForAll(all_articles)
        
        idx = 0
        for i, stock_info in enumerate(stockList):
            company_name = stock_info.get_name()
            company_sentiment_scores = sentiment_scores[idx:idx + indices[i]]

            print(f"Found {indices[i]} articles about company {company_name}")
            print(f"Sentiment analysis for {company_name}:")
            print(company_sentiment_scores)
            
            if company_sentiment_scores == [] :
                score = 0
            else :
                score = mean(sentiment_scores[idx:idx + indices[i]]) * 3
            
            new_rating = int(max(-10, min(10, round(score))))
            stock_info.rating = new_rating
            idx += indices[i]
