import unittest
from unittest.mock import patch, MagicMock
from models import AzureAPI, News, StockInfo

class TestAzureAIBatching:
    def test_batching_logic_with_small_limit(self):
        mock_response = {
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

        with patch('requests.post') as mock_post:
            mock_post.return_value = MagicMock(status_code=200, json=MagicMock(return_value=mock_response))
            
            news = News(["CompanyA", "CompanyB"])
            news.add_article("CompanyA", "Positive News", "Everything is great!")
            news.add_article("CompanyB", "Negative News", "Something went wrong!")

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