import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from fake_useragent import UserAgent


class WeiBo():
  # in this userpost.py, the main purpose is to get the specific user weibo post for specific page number,
  # you should input the userid, your cookies, and the number of page you want to get.
  # the output is the csv file to show the information about the post date, post url, text, and comment count, like count.
  
  def __init__(self,cookies,url_container):
    self.url='https://m.weibo.cn/comments/hotflow?'
    self.container_id=url_container
    self.cookies=cookies
    self.header={
         'user-agent': str(UserAgent().random)}
  

  def search(self): # from the writer post to get the user comment (mobile version)
    param={
        'id':self.container_id,
        'mid':self.container_id,
        'max_id_type':0

    }
    df = pd.DataFrame(columns = ['id', 'Text', 'Like'])
    res=requests.get(url=self.url,params=param,headers=self.header)
    ac=res.json()
   
    for i in ac['data']['data']:
      name=i['user']['id']
      text=i['text']
      like=i['like_count']
      df=df.append({'id' : name, 'Text' : text, 'Like' : like}, ignore_index = True)
    print(df.head)
    df.to_csv("doc.csv")



if __name__=='__main__':
  cookies=input("input your cookies")
  #example for the url: https://m.weibo.cn/comments/hotflow?id=4652003252765987&mid=4652003252765987&max_id_type=0
  url_container=input("input post containerid")
  w=WeiBo(cookies,url_container)
  w.search()
  
