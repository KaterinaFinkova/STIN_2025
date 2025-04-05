import os
from flask import Flask, request, jsonify, render_template
from models import UserDataManager, FinnhubAPI, APIManager, StockInfo, MinMessagesFilter, NegativeRatingFilter

app = Flask(__name__)

finnhubApiKey = os.getenv("FINNHUB_API_KEY")
newsdataApiKey = os.getenv("NEWSDATA_API_KEY")

finnhubApi = FinnhubAPI(api_key=finnhubApiKey)
apiManager = APIManager(finnhub_api=finnhubApi)

userDataManager = UserDataManager()


@app.route('/')
def home():
    return render_template("portfolio.html")

@app.route('/liststock', methods=['POST'])
def list_stock():
    stock_list = StockInfo.JSONtoList(request.json)
    news = apiManager.fetch_news(stock_list)
    #stock_list = minMessageFilter.filter(stock_list, news)
    #stock_list = self.AIAPIClient.process_news(stock_list, news)
    #stock_list = negativeRatingFilter.filter(stock_list)
    #update time stocklist ?
    return StockInfo.ListToJSON(stock_list)

"""
@app.route('/salestock', methods=['POST'])
def sale_stock():
    stock_list = StockInfo.JSONtoList(request.json)
    self.portfolio.update(stock_list)
    return jsonify({"status": "Portfolio updated"})
"""

@app.route("/user", methods=['GET','POST'])
def set_user_values():
    if request.method == 'POST':
        userDataManager.set_value('min_score',request.form.get('min_score',None))
        userDataManager.set_value('min_news', request.form.get('min_news',None))
        userDataManager.save_values()
    return render_template("user_setting.html",data=userDataManager.data)
            
"""
    def __init__(self):
        self.app = Flask(__name__)
        self.UserDataManager = UserDataManager()

        self._register_routes()
"""
