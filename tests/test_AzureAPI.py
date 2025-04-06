import unittest
from unittest.mock import patch, MagicMock
from models import AzureAPI, News, StockInfo


class TestAzureAI(unittest.TestCase):
    def __init__(self):
        self.mock_response = {
            "results": {
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
        }

    def run_test(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = MagicMock(status_code=200, json=MagicMock(return_value=self.mock_response))
            
            news = News(["CompanyA", "CompanyB"])
            news.add_article("CompanyA", "Positive News", "Everything is great!")
            news.add_article("CompanyB", "Negative News", "Something went wrong!")

            stock_list = [StockInfo("CompanyA", 123456789, 2, 0), StockInfo("CompanyB", 123456789, 2, 0)]

            azure_ai = AzureAPI(azure_key="api_key")

            azure_ai.getSentimentAnalysis(news, stock_list)

            assert stock_list[0].rating == 8
            assert stock_list[1].rating == -5