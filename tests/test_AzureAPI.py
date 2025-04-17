import pytest
import unittest
import requests
from unittest.mock import patch, MagicMock
from models import AzureAPI, News, StockInfo
from models.CompanySymbolMapper import CompanySymbolMapper

class TestAzureAIBatching(unittest.TestCase):

    def test_batching_logic_with_small_limit(self):
        mock_response = {
            "documents": [
                {
                    "id": "1",
                    "sentiment": "positive",
                    "confidenceScores": {
                        "positive": 0.8,
                        "neutral": 0.2,
                        "negative": 0.0
                    }
                },
                {
                    "id": "2",
                    "sentiment": "negative",
                    "confidenceScores": {
                        "positive": 0.1,
                        "neutral": 0.3,
                        "negative": 0.6
                    }
                }
            ]
        }

        with patch('requests.post') as mock_post:
            mock_post.return_value = MagicMock(status_code=200, json=MagicMock(return_value=mock_response))
            
            news = News(["CompanyA", "CompanyB"], CompanySymbolMapper())
            news.addArticle("CompanyA", "Positive News", "Everything is great!")
            news.addArticle("CompanyB", "Negative News", "Something went wrong!")

            stock_list = [StockInfo("CompanyA", 123456789, 2, 0), StockInfo("CompanyB", 123456789, 2, 0)]

            azure_ai = AzureAPI(azure_key="api_key")

            azure_ai.getSentimentAnalysis(news, stock_list)

            assert stock_list[0].rating == 8
            assert stock_list[1].rating == -5

    def test_batching_logic_with_small_limit(self):
        articles = [f"Article {i}" for i in range(7)]

        azure = AzureAPI("api_key", max_documents_per_request=3)

        with patch.object(azure, '_getSentimentBatch', return_value=[0]*3) as mock_batch:
            results = azure._getSentimentsForAll(articles)

            self.assertEqual(mock_batch.call_count, 3)

            calls = mock_batch.call_args_list
            self.assertEqual(len(calls[0][0][0]), 3)
            self.assertEqual(len(calls[1][0][0]), 3)
            self.assertEqual(len(calls[2][0][0]), 1)

            self.assertEqual(len(results), 9)

    def test_get_sentiment_batch_error_handling(self):
        mock_response = MagicMock(status_code=500, text="Internal Server Error")
        
        with patch.object(requests, 'post', return_value=mock_response):
            azure_ai = AzureAPI(azure_key="api_key")

            with pytest.raises(Exception) as exc_info:
                azure_ai._getSentimentBatch(["Article 1", "Article 2"])

            assert "Error from Azure API: 500" in str(exc_info.value)

    def test_no_articles(self):
        mock_response = {
            "documents": []
        }
        
        with patch.object(requests, 'post', return_value=MagicMock(status_code=200, json=MagicMock(return_value=mock_response))):
            news = News(["CompanyA"], CompanySymbolMapper())
            stock_list = [StockInfo("CompanyA", 123456789, 2, 0)]

            azure_ai = AzureAPI(azure_key="api_key")

            azure_ai.getSentimentAnalysis(news, stock_list)

            assert stock_list[0].rating == 0

    def test_one_company_multiple_articles(self):
        mock_response = {
            "documents": [
                {
                    "id": "1",
                    "sentiment": "positive",
                    "confidenceScores": {
                        "positive": 0.8,
                        "neutral": 0.2,
                        "negative": 0.0
                    }
                },
                {
                    "id": "2",
                    "sentiment": "positive",
                    "confidenceScores": {
                        "positive": 0.6,
                        "neutral": 0.3,
                        "negative": 0.2
                    }
                }
            ]
        }

        with patch('requests.post') as mock_post:
            mock_post.return_value = MagicMock(status_code=200, json=MagicMock(return_value=mock_response))

            news = News(["CompanyA"], CompanySymbolMapper())
            news.addArticle("CompanyA", "Positive News 1", "Everything is great!")
            news.addArticle("CompanyA", "Positive News 2", "Still great news!")

            stock_list = [StockInfo("CompanyA", 123456789, 2, 0)]

            azure_ai = AzureAPI(azure_key="api_key")

            azure_ai.getSentimentAnalysis(news, stock_list)

            assert stock_list[0].rating == 6
