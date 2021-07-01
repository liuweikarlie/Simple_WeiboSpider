
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from fake_useragent import UserAgent


class WeiBo():
  def __init__(self,userid,cookies):
    self.url='https://m.weibo.cn/api/container/getIndex?'
    self.cookies=cookies
    self.header={
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Cookie': self.cookies}
    self.df = pd.DataFrame(columns = ['create_at','url','raw_text','text', 'comment_count', 'attitudes_count'])
    self.userid=userid

    params={
        'type': 'uid',
        'value': self.userid,
    }
    self.userid=userid
    
    
    url1=self.url
    re=requests.get(url=url1,headers=self.header,params=params)
    response_data=re.json()
    print(response_data)
    
    response_data=response_data['data']['tabsInfo']['tabs']
    for i in response_data:
      if i['tab_type']=='weibo':
        self.containerid=i['containerid'] # get the weibo container id for the user
        break

    
    

  def user_post(self,page_num):
    print(str(UserAgent().random))
    self.header={
         'user-agent': str(UserAgent().random),
         'Cookies':self.cookies}
    self.page_num=page_num
    
    url2='https://m.weibo.cn/api/container/getIndex?'
    params={
          'type': 'uid',
          'value': self.userid,
          'containerid': self.containerid,
          'page':self.page_num
      }
    try:
      response=requests.get(url=url2,headers=self.header,params=params)
      response_data=response.json()['data']['cards']
      if page_num%3==0:
        time.sleep(5)
      for i in response_data:
        if "mblog" in str(i):
          mblog=i['mblog']
          post_url=i['scheme']
          raw_text=mblog.get('raw_text')
          text=mblog.get('text')
          create_at=mblog.get('created_at')
          comment_count=mblog.get('comments_count')
          attitute_count=mblog.get('attitudes_count')
          self.df = self.df.append({'create_at':create_at,'url':post_url,'raw_text':raw_text, 'text':text, 'comment_count':comment_count, 'attitudes_count': attitute_count},ignore_index = True)
    except Exception:
      print("detected by the weibo server")
    





if __name__=="__main__": 
  userid_input=input("userid input")
  cookies=input("cookies input")
  a=WeiBo(userid_input,cookies)

  n=int(input("page_num input"))

  for i in range(n):
    a.user_post(i)
    a.df.to_csv(userid_input+".csv")
