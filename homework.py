from calendar import month
from cgi import print_arguments
import datetime as dt
import math
from distutils.command.build_scripts import first_line_re
from itertools import count
from pickle import TRUE
import re
from xmlrpc.client import TRANSPORT_ERROR
import random
FORMAT = '%d.%m.%Y'

class Record:
    def __init__(self,amount,comment,date=None) -> None:
        self.amount=amount
        self.comment=comment
        if(date is None):
            moment_date=dt.datetime.now()
            self.date=moment_date.date()
            
        else:
            moment=dt.datetime.strptime(date,FORMAT)
            self.date=moment.date()
            



class Calculator:
    def __init__(self, limit) -> None:
        self.limit=limit
        self.records=list()
        

    def add_record(self,record):
        self.records.append(record)
        

    def get_today_stats(self):
        sum=0
        date_today=dt.datetime.now().date()
        print(date_today)
        for record in self.records:
            offset=date_today-record.date
            if offset.days==0:
                sum+=record.amount
        return sum

    def get_week_stats(self):
        sum=0
        date_today=dt.datetime.now().date()
        period=dt.timedelta(days=7)
        seven_days_ago=date_today-period
        for record in self.records:
            date=record.date
            past_date=date-seven_days_ago
            if(past_date.days<=7 and past_date.days>=0):
                sum+=record.amount
          
        return sum

    



class CaloriesCalculator(Calculator):
    def __init__(self, limit) -> None:
        super().__init__(limit)

    def get_calories_remained(self):
        calories=self.limit-self.get_today_stats()
        if calories==0 or calories<0:
            return 'Хватит есть!'
        else:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories} кКал'
    

    def get_today_stats(self):
        return super().get_today_stats()

    def get_week_stats(self):
        return super().get_week_stats()
    



class CashCalculator(Calculator):
    def __init__(self, limit) -> None:
        super().__init__(limit)
        
    USD_RATE=59.33
    EURO_RATE=65.34   
   
    def get_today_cash_remained(self,currency):
        cash_rub=self.limit-self.get_today_stats()
        if currency=='usd':
            cash_usd=cash_rub/self.USD_RATE
            if cash_usd>0:
                return f'На сегодня осталось {cash_usd:.2f} USD'
            elif cash_usd<0:
                return f'Денег нет, держись: твой долг - {abs(cash_usd):.2f} USD' 
            else:
                return f'Денег нет, держись'
        
        elif currency=='eur':
            cash_eur=cash_rub/self.EURO_RATE
            if cash_eur>0:
                return f'На сегодня осталось {cash_eur:.2f} Euro'
            elif cash_eur<0:
                return f'Денег нет, держись: твой долг - {abs(cash_eur):.2f} Euro'
            else:
                return f'Денег нет, держись'

        elif currency=='rub':
            if cash_rub>0:
                return f'На сегодня осталось {cash_rub:.2f} руб'
            elif cash_rub<0:
                return f'Денег нет, держись: твой долг - {abs(cash_rub):.2f} руб'
            else:
                return f'Денег нет, держись'
        else:
            return 'Ошибка'

     


    def get_today_stats(self):
        return super().get_today_stats()

            
            

    def get_week_stats(self):
        return super().get_week_stats()
        
    
                

cash_calculator = CashCalculator(2500)




def data_records():
    amount = 150
    count = random.randint(30, 40)    
    today_count = random.randint(5, 10)
    week_count = random.randint(5, 10) + today_count
    future_count = random.randint(5, 10)
    data = []
    for idx, _ in enumerate(range(count)):
        if idx < today_count:
            date = dt.datetime.now()
        elif idx < week_count:
            date = dt.datetime.now() - dt.timedelta(days=random.randint(1, 6))
        elif idx < future_count + week_count:
            date = dt.datetime.now() + dt.timedelta(days=random.randint(1, 6))
        else:
            date = dt.datetime(2019, 9, 1)
        data.append(Record(amount=amount, comment=f'Test {idx}', date=date.strftime('%d.%m.%Y')))
    random.shuffle(data)
    return data, today_count * amount, week_count * amount

list=data_records()



print(cash_calculator.get_week_stats())
print(cash_calculator.get_today_stats())



