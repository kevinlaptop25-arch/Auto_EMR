from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os

from app.api.routes_patients import router as patients_router
from app.api.routes_clinical import router as clinical_router
from app.api.routes_labs import router as labs_router
from app.api.routes_pacs import router as pacs_router
from app.api.routes_abdm import router as abdm_router
from app.api.routes_audit import router as audit_router
from app.api.routes_emergency import router as emergency_router
from app.api.routes_pharmacy import router as pharmacy_router
from app.api.routes_billing import router as billing_router
from app.api.routes_bloodbank import router as bloodbank_router

app = FastAPI(
    title="East Point Hospital - Automated EMR Engine & NMC Audit Simulator",
    description="Functional POC demonstrating structurally accurate synthetic patient records, strict clinical logic rules, live timeline logic, digitized PDF/PACS audit trails, full Pharmacy, Billing, Blood Bank, Emergency modules, and ABDM M1/M2/M3 workflows.",
    version="2.0.0",
    redirect_slashes=False
)

# Enable CORS for frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers with /api prefix
app.include_router(patients_router, prefix="/api")
app.include_router(clinical_router, prefix="/api")
app.include_router(labs_router, prefix="/api")
app.include_router(pacs_router, prefix="/api")
app.include_router(abdm_router, prefix="/api")
app.include_router(audit_router, prefix="/api")
app.include_router(emergency_router, prefix="/api")
app.include_router(pharmacy_router, prefix="/api")
app.include_router(billing_router, prefix="/api")
app.include_router(bloodbank_router, prefix="/api")

# Also include API Routers without /api prefix for flexible serverless path resolution
app.include_router(patients_router)
app.include_router(clinical_router)
app.include_router(labs_router)
app.include_router(pacs_router)
app.include_router(abdm_router)
app.include_router(audit_router)
app.include_router(emergency_router)
app.include_router(pharmacy_router)
app.include_router(billing_router)
app.include_router(bloodbank_router)

@app.get("/api/ping")
@app.get("/ping")
def ping():
    return {
        "status": "online",
        "service": "East Point Hospital EMR POC Backend",
        "compliance": ["NMC 2025", "ABDM M1/M2/M3", "NABH"]
    }

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

# SPA fallback handler: return index.html for browser routes, JSON 404 for missing /api routes
@app.exception_handler(404)
async def spa_404_handler(request: Request, exc):
    path = request.url.path
    if path.startswith("/api"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    
    # If a JS or CSS asset with a mismatched hash is requested, fallback to the latest asset bundle
    # instead of serving HTML which breaks module script loading
    if path.startswith("/assets/"):
        assets_dir = os.path.join(frontend_dist, "assets")
        if os.path.exists(assets_dir):
            if path.endswith(".js"):
                js_files = [f for f in os.listdir(assets_dir) if f.endswith(".js")]
                if js_files:
                    latest_js = os.path.join(assets_dir, sorted(js_files)[-1])
                    return FileResponse(latest_js, media_type="text/javascript")
            elif path.endswith(".css"):
                css_files = [f for f in os.listdir(assets_dir) if f.endswith(".css")]
                if css_files:
                    latest_css = os.path.join(assets_dir, sorted(css_files)[-1])
                    return FileResponse(latest_css, media_type="text/css")
        return JSONResponse(status_code=404, content={"detail": "Asset Not Found"})
        
    index_file = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_file):
        return FileResponse(
            index_file,
            media_type="text/html",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

# Serve frontend build if present
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
else:
    @app.get("/")
    def root():
        return {
            "hospital": "East Point Hospital & Research Centre",
            "system": "Automated Electronic Medical Record (EMR) Engine",
            "compliance": ["NMC 2025 Audit Standard", "ABDM M1/M2/M3", "NABH Indian Hospital Formats"],
            "docs_url": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
