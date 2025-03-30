from flask import Flask, request, jsonify, render_template

from models.UserDataManager import UserDataManager


# load configuration from file

class Application:

    def __init__(self):
        self.app = Flask(__name__)
        self.UserDataManager = UserDataManager()

        self._register_routes()

    # nová složka controllers ?
    def _register_routes(self):

        @self.app.route('/',methods=['GET'])
        def home():
            return render_template("portfolio.html")

        @self.app.route("/user", methods=['GET','POST'])
        def set_user_values():
            if request.method == 'POST':
                self.UserDataManager.set_value('min_score',request.form.get('min_score',None))
                self.UserDataManager.set_value('min_news', request.form.get('min_news',None))
                self.UserDataManager.save_values()
            return render_template("user_setting.html",data=self.UserDataManager.data)

        
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