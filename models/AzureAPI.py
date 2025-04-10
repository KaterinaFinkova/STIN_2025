import requests
from statistics import mean
from .StockInfo import StockInfo
from .News import News
from typing import List

class AzureAPI:
    def __init__(self, azure_key: str):
        self.azure_key = azure_key
        self.azure_endpoint = "https://stocknews.cognitiveservices.azure.com/text/analytics/v3.0/sentiment"
        self.max_documents_per_request = 500

    def _getScoresFromDocuments(sentiment_data):
        scores = []
        
        for document in sentiment_data['results']['documents']:
            positive_score = document['confidenceScores']['positive']
            negative_score = document['confidenceScores']['negative']
            
            score = (positive_score - negative_score) * 10
            
            scores.append(score)
        
        return scores

    def _getSentimentBatch(self, articles: List[str]) -> dict:
        headers = {
            "Ocp-Apim-Subscription-Key": self.azure_key,
            "Content-Type": "application/json"
        }
        
        documents = [{"id": str(i + 1), "language": "en", "text": article} for i, article in enumerate(articles)]
        payload = {"documents": documents}

        response = requests.post(self.azure_endpoint, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise Exception(f"Error from Azure API: {response.status_code}, {response.text}")
        
        return self._getScoresFromDocuments(response.json())
    
    def _getSentimentsForAll(self, articles: List[str]) -> List[dict]:
        all_results = []
        
        for i in range(0, len(articles), self.max_documents_per_request):
            batch = articles[i:i + self.max_documents_per_request]
            result = self._getSentimentBatch(batch)
            all_results.extend(result)
        
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
            
            if company_sentiment_scores == [] :
                score = 0
            else :
                score = mean(sentiment_scores[idx:idx + indices[i]])
            
            new_rating = int(max(-10, min(10, score)))
            stock_info.rating = new_rating
            idx += indices[i]
