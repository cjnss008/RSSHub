"""
title: 自动分页 Auto Pagination Filter
author: your_name_or_team
version: 0.1.0
required_open_webui_version: 0.4.3
license: MIT
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = Field(
            default=["*"],
            description="应用该分页过滤器的 pipeline 列表，* 表示全部适用"
        )
        PAGE_SIZE: int = Field(
            default=50,
            description="每次拉取的历史消息条数"
        )

    def __init__(self):
        self.id = "auto_pagination"
        self.name = "自动分页"
        self.type = "filter"
        self.valves = self.Valves()

    async def on_startup(self):
        # 可选：服务启动时执行
        pass

    async def on_shutdown(self):
        # 可选：服务关闭时执行
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """
        在请求发送到模型前注入 limit、before 参数
        """
        if body.get("endpoint", "").endswith("/chat/completions"):
            payload = body.setdefault("json", {})
            payload["limit"] = self.valves.PAGE_SIZE
            payload.setdefault("before", None)
        return body

    async def outlet(self, response: dict, user: Optional[dict] = None) -> dict:
        """
        在模型响应中追加分页游标（next_before）
        """
        msgs = response.get("messages", [])
        if msgs:
            next_before = msgs[0].get("id") or msgs[0].get("timestamp")
            response.setdefault("pagination", {})["next_before"] = next_before
        return response
