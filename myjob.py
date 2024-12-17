要将这个程序改成只调用一次，你需要移除 `threading.Timer` 相关的代码，并且确保 `getFilstList` 函数只被调用一次。以下是修改后的代码：

```python
import requests
import json

s = requests.session()
headers = {
    'Content-Type': 'application/json'
}
preList = []
newList = []

def getFilstList():
    global newList
    global preList
    # 这里value填你想要的人的UID
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=7191676856&containerid=1076037191676856&since_id'

    res = s.get(url)
    r = json.loads(res.text)
    preList = newList
    newList = r['data']['cards']
    preIds = []
    newIds = []
    for item in preList:
        if item['mblog']:
            preIds.append(item['mblog']['id'])

    for item in newList:
        if item['mblog']:
            newIds.append(item['mblog']['id'])
    if len(newIds) and len(preIds):
        new_id = set(newIds).difference(set(preIds))
        for item in list(new_id):
            getLongText(item)

# 获取微博内容
def getLongText(id):
    url = 'https://m.weibo.cn/statuses/extend?id={}'.format(id)
    res = s.get(url)
    try:
        r = json.loads(res.text)
        send(r['data']['longTextContent'])
        print('推送成功，{}'.format(url))
    except:
        print('获取全文出错，跳过···{}'.format(url))

def send(content):
    url = 'http://wxpusher.zjiecode.com/api/send/message'
    data = {
      "appToken": "AT_wKEnvFjF8JOEjUh7W5DoPiYYZLAKJc0G",  # 填自己在wxpusher申请的token
      "content": content,
      "summary": "温馨提示",  # 消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度100，可以不传，不传默认截取content前面的内容。
      "contentType": 2,  # 内容类型 1表示文字 2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown
      "topicIds": [],  # 发送目标的topicId，是一个数组！！！，也就是群发，使用uids单发的时候， 可以不传。
      "uids": [  # 发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。
          # 想推送给谁，UID在wxpusher后台看，如果推送的人比较多可以用官方的获取用户接口
          "UID_lHkwrUO9kpc8V6VSCvioglnUx8u1"
      ],
      "url": "https://m.weibo.cn/statuses/extend?id=4755736296948252"  # 原文链接，可选参数
    }
    res = s.post(url, data=json.dumps(data), headers=headers)
    print(res.text)

if __name__ == '__main__':
    getFilstList()
