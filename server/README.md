# OPEN-TUBE's server

![image-20190724221206658](http://ww4.sinaimg.cn/large/006tNc79gy1g5b8kqgfmuj30gi0bzjs0.jpg)

```
.
├── Dockerfile
├── README.md
├── api
│   ├── __init__.py
│   ├── common
│   │   └── __init__.py
│   └── v1
│       ├── __init__.py
│       ├── index.py
│       └── service
│           ├── __init__.py
│           └── index.py
├── app.py
├── config.py
├── requirements.txt
└── src
```

`docker build . --tag=rest-flask`

`docker run -p 5000:5000 rest-flask &`


