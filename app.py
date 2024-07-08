from flask import Flask, request, jsonify,redirect
from datetime import datetime,timezone,timedelta

import time
import aiohttp
import os

app=Flask(__name__)

@app.route('/')
def index():
    return redirect("https://github.com/HansHans135/ticket-web")

@app.route('/<user_id>/<date>/<timestamp>')
async def ticket(user_id,date,timestamp):
    if not os.path.isfile(f"html/{user_id}/{date}/{timestamp}.html"):
        return "404",404
    with open(f"html/{user_id}/{date}/{timestamp}.html", "r",encoding="utf-8") as f:
        html = f.read()
    return html

@app.route('/upload', methods=['POST'])
async def upload():
    async with aiohttp.ClientSession(headers={"Authorization": f'Bot {request.form["token"]}'}) as session:
        async with session.get("https://discord.com/api/users/@me") as response:
            data = await response.json()
            print(data)
            if response.status != 200:
                return jsonify({"url":"", "message":data}), response.status
    
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    now = dt2.strftime("%Y-%m-%d")
    now_ts=int(time.time())
    if not os.path.isdir(f"html/{data['id']}/{now}"):
        os.makedirs(f"html/{data['id']}/{now}")
    if len(os.listdir(f"html/{data['id']}/{now}"))>=100:
        return jsonify({"url":"", "message":"已達今天上傳上限"}), 403
    html = request.files["html_log"]
    html.save(f"html/{data['id']}/{now}/{now_ts}.html")
    return jsonify({"url":f"https://ticket.hans0805.me/{data['id']}/{now}/{now_ts}", "message":"上傳成功"}), 200

@app.route('/usage')
async def usage():
    async with aiohttp.ClientSession(headers={"Authorization": f'Bot {request.form["token"]}'}) as session:
        async with session.get("https://discord.com/api/users/@me") as response:
            data = await response.json()
            print(data)
            if response.status != 200:
                return jsonify({"url":"", "message":data}), response.status
    
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    now = dt2.strftime("%Y-%m-%d")
    if not os.path.isdir(f"html/{data['id']}/{now}"):
        return jsonify({"used":0,"remaining":100}), 200
    else:
        u=os.listdir(f'html/{data["id"]}/{now}')
        return jsonify({"used":len(u),"remaining":100-len(u)}), 200
@app.errorhandler(404)
async def error_404(error):
    return jsonify({"url":"","message":error}),404

@app.errorhandler(400)
async def error_400(error):
    return jsonify({"url":"","message":error}),400

@app.errorhandler(500)
async def error_500(error):
    return jsonify({"url":"","message":error}),500

app.run(host="0.0.0.0",port=15873,debug=True)