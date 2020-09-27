## 1 环境配置
### 1.1 配置 host:
* 打开Chrome的 F12：
* 浏览器访问一次：https://api.huobi.pro/market/history/kline?symbol=dacusdt&size=500&period=15min
* 在 Network 的请求抓包中，找到 Headers -> General -> Remote Address，复制该 IP 地址（104.16.230.188）。
* 将该 IP 地址配置到 host 中 ```104.16.230.188 api.huobi.pro```。
