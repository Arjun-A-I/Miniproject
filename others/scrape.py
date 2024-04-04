import requests
from bs4 import BeautifulSoup

url='https://www.railyatri.in/booking/trains-between-stations?src=sa_search&device_type_id=6&user_id=-1712167866&doj=04-04-2024&from_code=tvc&from_name=trivandrum+central&from_stn=TVC+%7C+Trivandrum+Central&to_code=pgt&to_name=palakkad&to_stn=PGT+%7C+Palakkad'
# Here to get data about spesific trains at specific dates edit the url link , since its a string
result=requests.get(url)
content=result.text

soup=BeautifulSoup(content,'html.parser')
title_box=soup.find('div',class_='col-xs-9 lft-space')
destination_title=title_box.find('h1').get_text()
# print(box.encode('utf-8'))
print(destination_title)

details_box=soup.find('div',class_='Result_Section')
# print(details_box.encode('utf-8'))
train_details=details_box.find_all('div',class_='Result_Info_Box-main')
print(len(train_details))
for i in train_details:
    train_name=i.find('div',class_='TrainInFo-block').get_text()
    train_number=i.find('div',class_='SA_Section').get_text()
    # train_time=i.find('div',class_='Result_Train_Time').get_text()
    print(train_name)
    print('-----------------------------------')     
    # print(i.encode('utf-8'))