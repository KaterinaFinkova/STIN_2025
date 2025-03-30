from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("portfolio.html")

"""
@app.route('/liststock', methods=['POST'])
def list_stock():
    stock_list = StockInfo.JSONtoList(request.json)
    news = self.NewsAPIManager.get_news(stock_list)
    stock_list = self.MinMessageFilter.filter(stock_list, news)
    stock_list = self.AIAPIClient.process_news(stock_list, news)
    stock_list = self.NegativeRatingFilter.filter(stock_list)
    return StockInfo.ListToJSON(stock_list)

@app.route('/salestock', methods=['POST'])
def sale_stock():
    stock_list = StockInfo.JSONtoList(request.json)
    self.portfolio.update(stock_list)
    return jsonify({"status": "Portfolio updated"})
"""