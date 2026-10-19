\## API 接口文档

\### 健康检查

`GET /health`

返回服务状态，mock\_mode = true代表当前使用模拟模型





\### 房价预测接口

`POST /predict`

请求体JSON示例:

```json

{

&#x09;"area":100.0,

&#x09;"bedroom":3,

&#x09;"bathrooms":2,

&#x09;"year\_built":2010

}



