"""
title: Auto Pagination Filter
author: YourName
version: 0.1.0
required_open_webui_version: 0.4.3
license: MIT
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class Pipeline:
    class Valves(BaseModel):
        PAGE_SIZE: int = Field(
            default=50,
            description="每页请求的历史消息数量"
        )
        pipelines: List[str] = Field(
            default=["*"],
            description="应用该过滤器的 pipeline 名称列表，* 表示全部"
        )

    def __init__(self):
        self.id = "auto_pagination"
        self.name = "自动分页"
        self.type = "filter"  # ✅ 使用 filter 而不是 manifold
        self.valves = self.Valves()

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        if body.get("endpoint", "").endswith("/chat/completions"):
            payload = body.setdefault("json", {})
            payload["limit"] = self.valves.PAGE_SIZE
            payload.setdefault("before", None)
        return body

    async def outlet(self, response: dict, user: Optional[dict] = None) -> dict:
        msgs = response.get("messages", [])
        if msgs:
            next_before = msgs[0].get("id") or msgs[0].get("timestamp")
            response.setdefault("pagination", {})["next_before"] = next_before
        return response
