"""
title: 自动分页模拟模型
author: ChatGPT
version: 0.1.0
required_open_webui_version: 0.4.3
license: MIT
"""

from typing import List, Union, Iterator
from pydantic import BaseModel, Field
import json

class Pipeline:
    class Valves(BaseModel):
        PAGE_SIZE: int = Field(default=50, description="每页消息条数")

    def __init__(self):
        self.id = "auto_pagination_model"
        self.name = "自动分页模拟模型"
        self.type = "manifold"
        self.valves = self.Valves()

    def pipes(self) -> List[dict]:
        return [{"id": self.id, "name": self.name}]

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict
    ) -> Union[str, Iterator[str]]:
        try:
            limit = self.valves.PAGE_SIZE
            before = body.get("before", None)

            # 模拟从已有历史中“分页提取”
            paged = messages[-limit:] if len(messages) > limit else messages

            result = {
                "summary": f"当前总消息数：{len(messages)}，本页返回：{len(paged)}条",
                "分页游标（模拟before）": messages[-(limit+1)]["id"] if len(messages) > limit else None,
                "本页内容": paged
            }
            return json.dumps(result, ensure_ascii=False, indent=2)

        except Exception as e:
            return f"发生错误: {e}"
