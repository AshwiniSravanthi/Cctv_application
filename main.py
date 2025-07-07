from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from neondb import insert_enquiry, create_enquiry_table
import os

app = FastAPI()

# ✅ Secure CORS config — allow your real domain only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://snapsecuretechnologies.com",     # your production domain
        "https://www.snapsecuretechnologies.com", # include www if applicable
        "https://snapsecure.vercel.app"           # fallback if using Vercel preview
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Pydantic schema
class Enquiry(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    message: str

# (Optional) Serve home.html if still needed
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    return FileResponse("static/home.html")

@app.on_event("startup")
def startup_event():
    create_enquiry_table()

@app.post("/enquiry")
def submit_enquiry(enquiry: Enquiry):
    print("📩 Received enquiry:", enquiry)
    insert_enquiry(
        name=enquiry.name,
        email=enquiry.email,
        phone=enquiry.phone_number,
        message=enquiry.message
    )
    return {"message": "✅ Enquiry submitted successfully"}
