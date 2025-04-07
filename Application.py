import os
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta

from models.Portfolio import Portfolio
from models.StockInfo import StockInfo
from models.UserDataManager import UserDataManager, KEY_MIN_NEWS, KEY_MIN_SCORE, KEY_BUY
from models.forms.UserForm import UserForm
from models.Filters import NegativeRatingFilter, MinMessagesFilter
from models import APIManager, FinnhubAPI, FMPAPI, AzureAPI

app = Flask(__name__)

app.UserDataManager = UserDataManager()
app.Portfolio = Portfolio()
app.config["SECRET_KEY"] = os.environ.get("SECRET")

FMPapi = FMPAPI(os.environ.get("FMP_API_KEY"))
FinnhubApi = FinnhubAPI(os.environ.get("Finnhub_API_KEY"))
app.ApiManager = APIManager([FMPapi], [FinnhubApi])

app.AIClient = AzureAPI(os.environ.get("AZURE_API_KEY"))

app.BeforeFilters = [MinMessagesFilter()]
app.AfterFilters = [NegativeRatingFilter()]

@app.route('/')
def home():
    return render_template("portfolio.html",portfolio=app.Portfolio.get_data())


@app.route('/liststock', methods=['POST'])
def list_stock():
    stock_list = StockInfo.JSONtoList(request.json)
    company_names = StockInfo.getNamesList(stock_list)

    news_from = str(datetime.now().date() - timedelta(days=1))
    news_to = str(datetime.now().date())

    news = app.ApiManager.fetch_news(company_names, news_from, news_to)

    for filter in app.BeforeFilters:
        stock_list = filter.filter(stock_list, news)

    app.AIClient.getSentimentAnalysis(stock_list, news)
    
    for filter in app.AfterFilters:
        stock_list = filter.filter(stock_list)

    return StockInfo.ListToJSON(stock_list) # should send to burza \rating endpoint later


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
        app.UserDataManager.set_value(KEY_BUY, request.form.get('buy stock',form.buy.data))
        app.UserDataManager.save_values()
    return render_template("user_setting.html",form=form)
