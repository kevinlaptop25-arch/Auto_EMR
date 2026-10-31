import os
import sys

# Ensure backend directory is in python search path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.main import app as fastapi_app

class VercelPathFixMiddleware:
    """
    Middleware to ensure Vercel Serverless Function rewrites correctly map
    to FastAPI routes regardless of whether Vercel passes x-matched-path,
    rewritten destination paths (/api/index.py/$1), or root calls.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            headers = dict(scope.get("headers", []))
            
            # 1. Handle Vercel matched path header if provided
            matched_path = headers.get(b"x-matched-path", b"").decode("utf-8")
            if not matched_path:
                matched_path = headers.get(b"x-rewrite-url", b"").decode("utf-8")
                
            if matched_path and not matched_path.startswith("/api/index.py"):
                path = matched_path.split("?")[0]
            
            # 2. Strip /api/index.py or /index.py prefix if present in invocation path
            for prefix in ["/api/index.py", "/index.py"]:
                if path.startswith(prefix):
                    remainder = path[len(prefix):]
                    path = remainder if remainder.startswith("/") else ("/" + remainder if remainder else "/")
                    break
                    
            if not path:
                path = "/"
                
            scope["path"] = path
                        
        await self.app(scope, receive, send)

app = VercelPathFixMiddleware(fastapi_app)
