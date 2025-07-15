"""
title: 自动分页 Filter
author: OpenWebUI Contributor
version: 0.1.0
description: 在请求中注入分页参数，响应中附加游标，实现对话自动分页。
required_open_webui_version: 0.4.3
license: MIT
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = Field(
            default=["*"],
            description="适用于哪些 pipeline（模型）；* 表示全部"
        )
        PAGE_SIZE: int = Field(
            default=50,
            description="每次拉取的消息数"
        )

    class UserValves(BaseModel):
        pass  # 无用户侧配置

    def __init__(self):
        self.id = "auto_pagination"
        self.name = "自动分页"
        self.type = "filter"
        self.valves = self.Valves()

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        if body.get("endpoint", "").endswith("/chat/completions"):
            payload = body.setdefault("json", {})
            payload["limit"] = self.valves.PAGE_SIZE
            payload.setdefault("before", None)
        return body

    async def outlet(self, response: dict, user: Optional[dict] = None) -> dict:
        messages = response.get("messages", [])
        if messages:
            cursor = messages[0].get("id") or messages[0].get("timestamp")
            if cursor:
                response.setdefault("pagination", {})["next_before"] = cursor
        return response
