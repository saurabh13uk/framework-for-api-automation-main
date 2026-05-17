import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class ApiExecutionReporter:
    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []

    def record(
        self,
        *,
        name: str,
        method: str,
        url: str,
        status_code: int,
        response_time_seconds: float,
        request_body: Optional[Dict[str, Any]],
        response_body: Any,
        logs: Optional[List[str]] = None,
    ) -> None:
        self.records.append(
            {
                "name": name,
                "method": method,
                "url": url,
                "status_code": status_code,
                "response_time_seconds": round(response_time_seconds, 3),
                "request_body": request_body,
                "response_body": self._friendly_body(response_body),
                "logs": logs or [],
            }
        )

    def write_reports(self, output_dir: str = "reports") -> None:
        report_dir = Path(output_dir)
        report_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_api_calls": len(self.records),
            "api_calls": self.records,
        }
        (report_dir / "api_execution_report.json").write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )
        (report_dir / "api_execution_report.html").write_text(
            self._render_html(payload),
            encoding="utf-8",
        )

    @staticmethod
    def _friendly_body(body: Any) -> Any:
        if isinstance(body, list):
            return {
                "type": "array",
                "total_items": len(body),
                "sample_items": body[:5],
            }
        return body

    @staticmethod
    def _render_html(payload: Dict[str, Any]) -> str:
        rows = []
        for item in payload["api_calls"]:
            request_body = html.escape(json.dumps(item["request_body"], indent=2))
            response_body = html.escape(json.dumps(item["response_body"], indent=2))
            logs = html.escape("\n".join(item.get("logs", [])))
            rows.append(
                "<section class='call'>"
                f"<h2>{html.escape(item['name'])}</h2>"
                "<div class='meta'>"
                f"<span>{html.escape(item['method'])}</span>"
                f"<span>{html.escape(item['url'])}</span>"
                f"<span>Status: {item['status_code']}</span>"
                f"<span>Time: {item['response_time_seconds']}s</span>"
                "</div><div class='grid'>"
                f"<div><h3>Request</h3><pre>{request_body}</pre></div>"
                f"<div><h3>Response</h3><pre>{response_body}</pre></div>"
                f"<div><h3>Logs</h3><pre>{logs}</pre></div>"
                "</div></section>"
            )
        page = """<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<title>API Execution Report</title>
<style>
body { font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }
h1 { margin-bottom: 4px; }
.summary { margin-bottom: 24px; color: #475569; }
.call { background: #ffffff; border: 1px solid #d8dee9; border-radius: 8px; padding: 18px; margin-bottom: 18px; }
.call h2 { margin: 0 0 12px; font-size: 20px; }
.meta { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; }
.meta span { background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 999px; padding: 6px 10px; font-size: 13px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
h3 { margin: 0 0 8px; font-size: 15px; }
pre { white-space: pre-wrap; overflow-x: auto; background: #0f172a; color: #e2e8f0; padding: 12px; border-radius: 6px; font-size: 12px; line-height: 1.45; }
</style>
</head>
<body>
<h1>API Execution Report</h1>
<p class='summary'>Generated at __GENERATED_AT__. Total API calls: __TOTAL_API_CALLS__.</p>
__ROWS__
</body>
</html>
"""
        return (
            page.replace("__GENERATED_AT__", html.escape(payload["generated_at"]))
            .replace("__TOTAL_API_CALLS__", str(payload["total_api_calls"]))
            .replace("__ROWS__", "".join(rows))
        )