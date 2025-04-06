import os

from flask import Flask, request, jsonify, render_template

from models.Portfolio import Portfolio
from models.StockInfo import StockInfo
from models.UserDataManager import UserDataManager, KEY_MIN_NEWS, KEY_MIN_SCORE, KEY_BUY
from models.forms.UserForm import UserForm

app = Flask(__name__)

app.UserDataManager = UserDataManager()
app.Portfolio = Portfolio()
app.config["SECRET_KEY"]=os.environ.get("SECRET","dev")

@app.route('/')
def home():
    return render_template("portfolio.html",portfolio=app.Portfolio.get_data())

"""
@app.route('/liststock', methods=['POST'])
def list_stock():
    stock_list = StockInfo.JSONtoList(request.json)
    news = self.NewsAPIManager.get_news(stock_list)
    stock_list = self.MinMessageFilter.filter(stock_list, news)
    stock_list = self.AIAPIClient.process_news(stock_list, news)
    stock_list = self.NegativeRatingFilter.filter(stock_list)
    return StockInfo.ListToJSON(stock_list)
"""
@app.route('/salestock', methods=['POST'])
def sale_stock():
    try:
        stock_list = StockInfo.JSONtoList(request.get_data(as_text=True))
        pass
    except Exception as e:
        return jsonify({"error": str(e)}),415
    for stock_info in stock_list:
        print(stock_info)
        app.Portfolio.buy_or_sell(stock_info)
    app.Portfolio.save()
    return jsonify({"error":""}),200



    
@app.route("/user", methods=['GET','POST'])
def set_user_values():
    form = UserForm(min_message=app.UserDataManager.get_value(KEY_MIN_NEWS),
                    min_rating=app.UserDataManager.get_value(KEY_MIN_SCORE),
                    buy=app.UserDataManager.get_value(KEY_BUY))
    if form.validate_on_submit():
        app.UserDataManager.set_value(KEY_MIN_SCORE,request.form.get('min_score',form.min_rating.data))
        app.UserDataManager.set_value(KEY_MIN_NEWS, request.form.get('min_news',form.min_message.data))
        app.UserDataManager.set_value(KEY_BUY, request.form.get('min_news',form.buy.data))
        app.UserDataManager.save_values()
    return render_template("user_setting.html",form=form)
