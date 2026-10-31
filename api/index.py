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
    rewritten destination paths, or stripped prefixes.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            
            # Check for Vercel matched path header
            matched_path = headers.get(b"x-matched-path", b"").decode("utf-8")
            if not matched_path:
                matched_path = headers.get(b"x-rewrite-url", b"").decode("utf-8")
            
            if matched_path:
                # Strip query params
                clean_path = matched_path.split("?")[0]
                for prefix in ["/api/index.py", "/index.py"]:
                    if clean_path.startswith(prefix):
                        clean_path = clean_path[len(prefix):]
                        if not clean_path.startswith("/"):
                            clean_path = "/" + clean_path
                        break
                if clean_path:
                    scope["path"] = clean_path
            else:
                path = scope.get("path", "")
                for prefix in ["/api/index.py", "/index.py"]:
                    if path.startswith(prefix):
                        clean_path = path[len(prefix):]
                        if not clean_path.startswith("/"):
                            clean_path = "/" + clean_path
                        scope["path"] = clean_path
                        break
                        
        await self.app(scope, receive, send)

app = VercelPathFixMiddleware(fastapi_app)
