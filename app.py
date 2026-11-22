from flask import Flask,render_template,request,redirect,url_for,flash
import json
import datetime

app = Flask(__name__)
app.secret_key = "tang_jun_lang_de_key"


@app.route("/")
def home():
    with open("data.json","r",encoding="UTF-8") as f:
        Data = json.load(f)

    total_money = sum(Data[i]['amount'] for i in range(len(Data)))


    return render_template("index.html",data_list = Data,total_amount=total_money)















@app.route("/hi/<name>")
def hi(name):
    return f"hi{name}"











@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == "GET":
        return render_template("add.html")

    elif request.method == "POST":

        amount = request.form.get('amount')
        category = request.form.get('category')
        note = request.form.get('note')
        kind = request.form.get('kind') or "消费"

        print (f"{amount}{category}{note}{kind}")

        if not amount or not category or not note :
            flash("金额，分类，备注不能为空")
            return redirect(url_for('add'))


        try:
            amount_test = float(amount)
            if amount_test <0:
                flash ("该记账本仅支持正数")
                return redirect(url_for('add'))
        except ValueError:
            flash("金额必须是数字")
            return redirect(url_for('add'))


        date = datetime.datetime.now().strftime("%Y-%m-%d")

        new_records = {
            "date" : date,
            "amount" : float(amount),
            "category" : category,
            "note" : note,
            "kind" : kind
        }
        
        with open ("data.json","r",encoding= "utf-8") as f:
            apd = json.load(f)

        apd.append(new_records)

        with open ("data.json","w",encoding = "utf-8") as f:
            json.dump(apd,f,ensure_ascii=False,indent = 4)

        print ("保存成功")

    
    return redirect(url_for('home'))





















if __name__  == "__main__":
    app.run(debug=True)