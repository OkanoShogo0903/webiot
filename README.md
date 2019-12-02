## Install
```
$ pip install Flask
$ pip install flask_api
```

## 使い方

- サーバをたてる
```
$ python scripts/server.py
```

- サーバに行ってほしいグリッドの座標を送る
```
$ make <Tab>
or
$ curl -X POST -H "Content-Type: application/json" -d '{"x":10, "y":20}
```

