from fastapi import FastAPI, Form,Query,Header,HTTPException,Request,BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse,RedirectResponse
import pymysql

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request,exc):
    return RedirectResponse("/errorpage")#重定向

@app.get("/errorpage") #处理get类型
async def errorpage():
    return {"errorpage":"wo y can not see it"} #出现错误会跳转到errorpage页面

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):

    return templates.TemplateResponse("login/login1.html", {"request": request})

@app.post("/login",response_class=HTMLResponse)
async def login(request: Request,username: str = Form(...), password: str = Form(...),):
    # 打开数据库
    db = pymysql.connect(host="localhost", user="root", password="roottoor", db="haha")
    # 创建游标对象
    cursor = db.cursor()
    # sql语句
    sql = "select * from table1"
    # 执行sql
    cursor.execute(sql)
    # 确认
    db.commit()
    list1 = []
    for i in range(4):
        data = cursor.fetchone()
        # 取出来的是元组，可以转化为列表
        li = list(data)
        list1.append(li)
        # 在这里处理登录逻辑，例如验证用户名和密码
    if username == list1[0][1] and password == list1[0][2]:
        return templates.TemplateResponse("login/loginsuccess.html",{"request":request,"username":username})
    return templates.TemplateResponse("login/wrong1.html",{"request":request})

if __name__ == '__main__':
    uvicorn.run(app="main:app",host="127.0.0.1",port=8080,reload=True)