import json
import sys
from datetime import datetime,date,timedelta
from pathlib import Path
import argparse

DATA = Path("data.json")

args = sys.argv[1:]

def Stat():

    with open("data.json", "r", encoding="utf-8") as f:
            res = json.load(f)

    parser = argparse.ArgumentParser(description="在stat后面分别输入年月日，单次则检查单日，多次则遍历始末")
    parser.add_argument("start_year",type=int,help="起始年份")
    parser.add_argument("start_month",type=int,help="起始月份")
    parser.add_argument("start_day",type=int,help="起始日期")
    if len(args) == 7:
        parser.add_argument("end_year",type=int,help="结束年份")
        parser.add_argument("end_month",type=int,help="结束月份")
        parser.add_argument("end_day",type=int,help="结束日期")

    stat_args = parser.parse_args(args[1:])
    
    try:
        start_date = date(stat_args.start_year,stat_args.start_month,stat_args.start_day)
        if len(args) == 7 :
            end_date = date(stat_args.end_year,stat_args.end_month,stat_args.end_day)
    except ValueError:
        print("数值初始化失败，请检查输入与提示是否一致")

    real_total = 0

    summary = {}
    line = "-"*80

    if len(args) == 4:

        for r in res :
            if r['date'] == str(start_date) :
                summary[r['kind']] = summary.get(r['kind'],0) + r['amount']     
        total_amount = sum(summary.values())

        if total_amount > 0:
        
            print(f"在{start_date}总共花费{total_amount}\n{line}")

            for kind,amount in summary.items():
                ratio = (amount / total_amount)*100
                print(f"{kind}   ￥ {amount:>8.2f}   {ratio:.2f}%")
        else :
            print ("总金额计算失败，请检查数据")
            return
    elif len(args) == 7 :

        if end_date < start_date :
                print("起始日期大于结束日期，无法计算")
                return
        current = start_date
        while current <= end_date :
            for r in res :
                if r['date'] == str(current):
                    summary[r['kind']] = summary.get(r['kind'],0) + r['amount']     
            total_amount = sum(summary.values())
            if total_amount > 0:
                print(f"在{current}总共花费{total_amount}\n{line}")


                for kind,amount in summary.items():
                    ratio = (amount / total_amount)*100
                    print(f"{kind}   ￥ {amount:>8.2f}   {ratio:.2f}%")
            else :
                print ("当前无记录")
            current += timedelta(days=1)
            summary = {}
            real_total += total_amount
        
        
        print(f"{line}\n在这段时间内总花费 ￥： {real_total}")

























def List():
    with open ("data.json","r",encoding="utf-8") as f:
        res = json.load(f)

    total =0

    for  i in range(len(res)):
        total += res[i]['amount']
        print (f"{res[i]['date']}  {res[i]['category']}       ￥  {res[i]['amount']:>8.2f}  {res[i]['note']}  [{res[i]['kind']}]")
    print("-"*80)

    print(f"共计{len(res)}笔，合计 ￥{total}")
    





















    
def bookkeeping(record) :
    

    with open("data.json","r",encoding="utf-8") as f:
                    check = json.load(f)
                    check.append(record)

    with open("data.json","w",encoding="utf-8") as f:
        json.dump(check,f,ensure_ascii=False,indent=4)

    print(f"已记账:日期：{record['date']},金额：{record['amount']},类别:{record['category']},注释：{record['note']},性质：{record['kind']}")




def initialize () :
    try:
        amount = float(args[1])
    except ValueError:
        print("金额无法转换为浮点,请重新输入")
        return
    
    kind = "消费"
    if "--kind" in args:
        i = args.index("--kind")
        if i + 1< len(args):
            kind = args [i + 1]
            del args[i:i+2]


    category = args[2]
    note = args[3]

    record = {
    "date":datetime.now().strftime("%Y-%m-%d"),
    "amount":amount,
    "category":category,
    "note": note,
    "kind": kind,
}

    if not DATA.exists():
        
        print("检测到无对应账本，本次程序从生成账本开始，请在生成记账本后重新输入数据")
        check  = []
        with open("data.json","w",encoding="utf-8") as f:
            json.dump(check,f)

    return record















def main ():
    if not args:
        print ("使用方法:若要记账则在命令终端里第一位输入add,若要查看账本请在第一位输入list,然后依次输入金额，支出类型，标注，（若有需要可以用--kind补充性质）")
        return
    
    elif args[0] == "list":
            List()
            return
    
    elif args[0] == "stat":
            Stat()
            return

    elif len(args) < 4:
        print ("注意:依次输入金额，支出类型，标注，（若有需要可以用--kind补充性质）")
        return    

    elif args[0] == "add" :
        bookkeeping(initialize())
        return


    else :
        print ("使用方法:若要记账则在命令终端里第一位输入add,若要查看账本请在第一位输入list,然后依次输入金额，支出类型，标注，（若有需要可以补充性质）")
        return
    











if __name__ == "__main__" :
    main()
    