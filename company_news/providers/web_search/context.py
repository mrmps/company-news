from __future__ import annotations

import os
from typing import Any

from company_news.models import Case, Hit
from company_news.providers.base import hit

from .common import WebAdapter


def _parse(payload: Any) -> list[Hit]:
    output: list[Hit] = []
    for row in payload.get("results") or []:
        item = hit(row.get("url"), row.get("title"), row.get("description"))
        if item:
            output.append(item)
    return output


def _build(case: Case):
    return (
        "POST", "https://api.context.dev/v1/web/search",
        {"Authorization": f"Bearer {os.environ['CONTEXT_API_KEY']}", "Content-Type": "application/json"},
        {"query": case.question, "numResults": 10, "highlightsOptions": {"enabled": False}},
        None, 90,
    )


ADAPTERS = [WebAdapter(
    "context", "https://docs.context.dev/api-reference/web-scraping/search",
    ("CONTEXT_API_KEY",), _build, _parse,
)]
