![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# Youkube 
> Youtube -> Youku

订阅youtube频道或者个人，将视频转移到youku

## 环境 Environment
- python 2.7

## 依赖 Dependence

```shell
pip install -r requirements.txt
```
## 配置 Configuration

配置文件存放于 main.py 同一级目录，默认名为 `config.json`.

**配置项示例**

```json
{
  "sqlite3_file": "/root/sqlite3.db", // sqlite 数据库文件路径
  "thumbnail_dir": "/root/thumbnail", // 视频封面图存放路径 
  "items": [ // 订阅项
    {
      "type": "user", // 类型 user 用户 channel 频道
      "category": "科技", // 优酷视频分类
      "channel_name": "GreateScoot", // 频道名用于记录 可不填
      "desc": "模拟电路数字电路 视频来自youtube实时同步", // 优酷视频描述
      "user": "greatscottlab", // 用户跟 type 对应，填写用户名
      "youku_prefix": "GreateScoot - " // 上传优酷时添加的视频标题前缀
    },
    {
      "type": "user",
      "category": "游戏",
      "channel_name": "Dota2 WTF",
      "desc": "Dota2 WTF 视频来自youtube实时同步",
      "user": "DarduinMyMenlon",
      "youku_prefix": "Dota2视频 - "
    },
    {
      "type": "user",
      "category": "搞笑",
      "channel_name": "Larva ",
      "desc": "红虫黄虫 视频来自youtube实时同步",
      "user": "Larva2011ani",
      "youku_prefix": "Lavra - "
    },
    { 
      "type": "channel",
      "category": "汽车",
      "channel_name": "CarCrashVideos ",
      "desc": "交通事故视频 请重视交通安全 视频来自youtube实时同步",
      "channel": "UCWmZgjXV9gnoIDwgMh6U5Rg",
      "youku_prefix": "交通事故合辑 - "
    },
    {
      "type": "user",
      "category": "汽车",
      "channel_name": "Car Crash Compilation ",
      "desc": "交通事故视频 请重视交通安全 视频来自youtube实时同步",
      "user": "CarCrashCompilation",
      "youku_prefix": "交通事故合辑 - "
    },
    {
      "type": "user",
      "category": "游戏",
      "channel_name": "DotaCinema",
      "desc": "DotaCinema dota2 fails dota2 headshot 众多dota2视频 视频来自youtube实时同步",
      "user": "DotaCinema",
      "youku_prefix": "Dota2视频 - "
    },
    {
      "type": "user",
      "category": "搞笑",
      "channel_name": "failarmy",
      "desc": "failarmy 搞笑视频 视频来自youtube实时同步",
      "user": "failarmy",
      "youku_prefix": "failarmy - "
    }
  ],
  "video_dir": "/root/", // 视频存放路径
  "youku_access_token": "xxxx", // youku app access_token
  "youku_client_id": "xxxx" // youku app client id
}
```


### 运行 / Run



```shell
cd youkube
python youkube/main.py
```

