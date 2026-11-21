from flask import Flask,render_template
import json
app = Flask(__name__)



@app.route("/")
def home():
    with open("data.json","r",encoding="UTF-8") as f:
        Data = json.load(f)

    total_money = sum(Data[i]['amount'] for i in range(len(Data)))

    print(f"已读取{len(Data)}条数据")

    return render_template("index.html",data_list = Data,total_amount=total_money)

@app.route("/hi/<name>")
def hi(name):
    return f"hi{name}"


if __name__  == "__main__":
    app.run(debug=True)