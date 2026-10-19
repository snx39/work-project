from pydantic import BaseModel, Field


# 预测请求输入
class HouseFeatures(BaseModel):
    area: float = Field(gt=0,description = "房屋面积，必须大于0，单位平方米")
    bedrooms: int = Field(ge=1,le=20,description = "卧室数量，1~20之间")
    bathrooms: int = Field(ge=0,le=10,description = "卫生间数量")
    year_built:int = Field(ge=1900,le=2026,description = "建造年份")

    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "area":120.0,
                    "bedrooms":3,
                    "bathrooms":2,
                    "year_built":2000
                }
            ]
        }
    }

# 预测响应输出
class HousePredictResponse(BaseModel):
    predicted_price: float
    unit: str = "CNY"