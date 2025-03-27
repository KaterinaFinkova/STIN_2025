from flask import Flask, request, jsonify, render_template

# load configuration from file

class Application:

    def __init__(self):
        self.app = Flask(__name__)
        # self.portfolio = Portfolio()

        self._register_routes()

    # nová složka controllers ?
    def _register_routes(self):

        @self.app.route('/')
        def home():
            return render_template("portfolio.html")
        
        """
        # kde může selhat - kontrola jednotlivých kroků - nevalidní data, prázdný seznam
        @self.app.route('/liststock', methods=['POST'])
        def list_stock():
            stock_list = StockInfo.JSONtoList(request.json)
            news = self.NewsAPIManager.get_news(stock_list)
            stock_list = self.MinMessageFilter.filter(stock_list, news)
            stock_list = self.AIAPIClient.process_news(stock_list, news)
            stock_list = self.NegativeRatingFilter.filter(stock_list)
            return StockInfo.ListToJSON(stock_list)

        @self.app.route('/salestock', methods=['POST'])
        def sale_stock():
            stock_list = StockInfo.JSONtoList(request.json)
            self.portfolio.update(stock_list)
            return jsonify({"status": "Portfolio updated"})

        """
        

    def run(self):
        self.app.run(debug=True, host='localhost', port=8000)


if __name__ == '__main__':
    app_instance = Application()
    app_instance.run()