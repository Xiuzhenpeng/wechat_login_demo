from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from wechat_config import WECHAT_APPID, WECHAT_SECRET
import httpx
import time
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

qr_scene_map = {}  # 保存 scene_id 和 openid 的绑定


# 获取 access_token
async def get_access_token():
    url = (
        f"https://api.weixin.qq.com/cgi-bin/token"
        f"?grant_type=client_credential&appid={WECHAT_APPID}&secret={WECHAT_SECRET}"
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.json().get("access_token")


# 获取带 scene_id 的临时二维码 URL
async def create_wechat_qr(scene_id: str):
    access_token = await get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}"
    payload = {
        "expire_seconds": 300,
        "action_name": "QR_SCENE",
        "action_info": {"scene": {"scene_id": int(scene_id)}}
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        ticket = resp.json().get("ticket")
        if ticket:
            qr_url = f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}"
            return qr_url
        return None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    scene_id = str(int(time.time()))  # 可改为 uuid 或用户 session_id 映射
    qr_url = await create_wechat_qr(scene_id)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "scene_id": scene_id,
        "qr_url": qr_url
    })


@app.post("/wechat/callback")
async def wechat_callback(request: Request):
    body = await request.body()
    import xml.etree.ElementTree as ET
    root = ET.fromstring(body.decode("utf-8"))
    event = root.findtext("Event")
    from_user = root.findtext("FromUserName")
    event_key = root.findtext("EventKey")

    if event in ["subscribe", "SCAN"]:
        if event_key.startswith("qrscene_"):
            event_key = event_key.replace("qrscene_", "")
        qr_scene_map[event_key] = from_user
        print(f"[扫码成功] scene_id={event_key} openid={from_user}")

    return Response(content="success", media_type="text/plain")


@app.get("/check_login")
async def check_login(scene_id: str):
    if scene_id in qr_scene_map:
        return {"status": "success", "openid": qr_scene_map[scene_id]}
    return {"status": "waiting"}


@app.get("/success", response_class=HTMLResponse)
async def success(request: Request, openid: str = ""):
    return templates.TemplateResponse("success.html", {
        "request": request,
        "openid": openid
    })