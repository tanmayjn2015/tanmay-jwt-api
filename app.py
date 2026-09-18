API_KEY = "TANMAY_JWT_API"

import time
import json
import base64
import re

import httpx
from flask import Flask, request, jsonify
from flask_cors import CORS
from Crypto.Cipher import AES

from google.protobuf import json_format
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf.message import Message


# ============================================================
#  PART 1 — FreeFire_pb2 (inlined)
# ============================================================

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 6, 30, 0, "", "FreeFire.proto",
)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x46reeFire.proto"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t'
    b'\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d '
    b'\x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t"]\n\x10\x42lacklist'
    b'InfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n'
    b'\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 '
    b'\x01(\r"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12'
    b'\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18'
    b'\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08"\xa0\x03\n\x08'
    b'LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region'
    b'\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_'
    b'region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t'
    b'\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_'
    b'regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl'
    b'\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mul'
    b'ator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.'
    b'BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueue'
    b'Info\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18'
    b'\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city'
    b'\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n'
    b'\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17'
    b'\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_'
    b'REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n'
    b'\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME'
    b'_AUTO_NEW\x10\xf6\x07\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "FreeFire_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_BANREASON"]._serialized_start = 738
    _globals["_BANREASON"]._serialized_end = 906
    _globals["_LOGINREQ"]._serialized_start = 18
    _globals["_LOGINREQ"]._serialized_end = 117
    _globals["_BLACKLISTINFORES"]._serialized_start = 119
    _globals["_BLACKLISTINFORES"]._serialized_end = 212
    _globals["_LOGINQUEUEINFO"]._serialized_start = 214
    _globals["_LOGINQUEUEINFO"]._serialized_end = 316
    _globals["_LOGINRES"]._serialized_start = 319
    _globals["_LOGINRES"]._serialized_end = 735

LoginReq = _globals["LoginReq"]
LoginRes = _globals["LoginRes"]


# ============================================================
#  PART 2 — Settings
# ============================================================

MAIN_KEY = base64.b64decode("WWcmdGMlREV1aDYlWmNeOA==")
MAIN_IV = base64.b64decode("Nm95WkRyMjJFM3ljaGpNJQ==")
RELEASEVERSION = "OB55"
USERAGENT = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"
LOGIN_URL = "https://loginbp.ppmainecoonghj.com/"

# Fast HTTP client (connection pooling + keep-alive)
HTTP_LIMITS = httpx.Limits(max_keepalive_connections=20, max_connections=50)
HTTP_TIMEOUT = httpx.Timeout(15.0, connect=5.0)
_http_client = httpx.Client(limits=HTTP_LIMITS, timeout=HTTP_TIMEOUT)


# ============================================================
#  PART 3 — Flask App
# ============================================================

app = Flask(__name__, template_folder="templates")
CORS(app)


# ============================================================
#  PART 4 — Helpers
# ============================================================

def pad(text: bytes) -> bytes:
    padding_length = AES.block_size - (len(text) % AES.block_size)
    return text + bytes([padding_length] * padding_length)


def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(plaintext))


def json_to_proto(json_data: str, proto_message: Message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)
    return proto_message.SerializeToString()


def try_parse_login_res(data: bytes):
    try:
        msg = LoginRes()
        msg.ParseFromString(data)
        if msg.account_id and msg.account_id > 0:
            return json.loads(json_format.MessageToJson(msg))
    except Exception:
        pass
    return None


def extract_login_res(raw: bytes) -> dict:
    # Attempt 1: from index 0
    parsed = try_parse_login_res(raw)
    if parsed:
        return parsed

    # Attempt 2: scan each \x08
    idx = 0
    while True:
        idx = raw.find(b"\x08", idx)
        if idx == -1:
            break
        parsed = try_parse_login_res(raw[idx:])
        if parsed:
            return parsed
        idx += 1

    # Attempt 3: JWT marker prefix
    jwt_marker = raw.find(b"eyJhbGciOiJIUzI1NiIs")
    if jwt_marker != -1:
        for i in range(jwt_marker - 1, max(jwt_marker - 300, -1), -1):
            if raw[i] == 0x42:
                parsed = try_parse_login_res(raw[i:])
                if parsed:
                    return parsed
                break

    raise Exception(f"Could not parse LoginRes. Raw: {raw[:200]}")


def get_access_token(account: str):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = (
        account
        + "&response_type=token&client_type=2"
        + "&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
        + "&client_id=100067"
    )
    headers = {
        "User-Agent": USERAGENT,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    resp = _http_client.post(url, data=payload, headers=headers)
    data = resp.json()
    return data.get("access_token", "0"), data.get("open_id", "0")


def generate_jwt_token(uid: str, password: str):
    start_time = time.time()

    token_val, open_id = get_access_token(f"uid={uid}&password={password}")
    if token_val == "0" or open_id == "0":
        raise Exception("Invalid UID or Password — access token not received")

    body = json.dumps({
        "open_id": open_id,
        "open_id_type": "4",
        "login_token": token_val,
        "orign_platform_type": "4",
    })
    proto_bytes = json_to_proto(body, LoginReq())
    payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)

    headers = {
        "User-Agent": USERAGENT,
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "X-Ga-Sv": "1789534056",
        "Authorization": "Bearer",
        "X-Ga": "v1 1",
        "Releaseversion": RELEASEVERSION,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.12f1",
        "PlAy_VeR": "1.132.1",
        "Ob_VeR": RELEASEVERSION,
    }

    resp = _http_client.post(f"{LOGIN_URL}MajorLogin", data=payload, headers=headers)
    msg = extract_login_res(resp.content)

    elapsed = time.time() - start_time

    return {
        "access_token": token_val,
        "open_id": open_id,
        "real_uid": str(msg.get("accountId", "")),
        "status": "success",
        "time": f"{elapsed:.2f}s",
        "token": f"{msg.get('token', '')}",
    }



# ============================================================
#  PART 5 — Admin/User Panel + Control API
# ============================================================

from functools import wraps
from datetime import datetime, timezone
import sqlite3
from flask import session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash

# Direct configuration: no environment-file setup is required.
app.secret_key = "TANMAY_JWT_SESSION_SECRET_2026"
DB_PATH = "tanmay_jwt.db"
ADMIN_USER = "tanmay"
ADMIN_PASSWORD = "2015"
OWNER_ID = 8317791404
BOT_API_URL = "https://78.154.103.43:10154"
BOT_API_KEY = "TANMAY_JWT_API"

def bot_request(method, path, payload=None):
    if not BOT_API_URL or "YOUR-WISPBYTE-BOT-DOMAIN" in BOT_API_URL:
        raise RuntimeError("BOT_API_URL is not configured")
    headers = {"X-Bot-API-Key": BOT_API_KEY, "Content-Type": "application/json"}
    url = BOT_API_URL.rstrip("/") + path
    response = _http_client.request(method, url, json=payload, headers=headers)
    try:
        body = response.json()
    except Exception:
        body = {"status": "error", "error": response.text[:1000]}
    return body, response.status_code

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        action TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    if not conn.execute("SELECT 1 FROM users WHERE username=?", (ADMIN_USER,)).fetchone():
        conn.execute(
            "INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?)",
            (ADMIN_USER, generate_password_hash(ADMIN_PASSWORD), "admin",
             datetime.now(timezone.utc).isoformat())
        )
    conn.commit()
    conn.close()

def audit(action):
    try:
        conn = db()
        conn.execute(
            "INSERT INTO audit(username,action,created_at) VALUES(?,?,?)",
            (session.get("username"), action, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"status":"error","error":"Authentication required"}), 401
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped

def admin_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            return jsonify({"status":"error","error":"Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapped

def owner_only_telegram(data):
    """Allow Telegram control only when the incoming Telegram user/chat is the owner."""
    try:
        sender = data.get("message", {}).get("from", {}) or {}
        chat = data.get("message", {}).get("chat", {}) or {}
        return int(sender.get("id", -1)) == OWNER_ID or int(chat.get("id", -1)) == OWNER_ID
    except (TypeError, ValueError):
        return False

def render_panel(content=None, role=None):
    role = role or session.get("role")
    if role == "admin":
        return render_template_string(content or "", username=session.get("username"),
                                      role=role, user_count=0, telegram_status="bot bridge configured" if BOT_API_URL and "YOUR-WISPBYTE-BOT-DOMAIN" not in BOT_API_URL else "bot bridge URL required")
    return render_template_string(content or "", username=session.get("username"), role=role)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u=request.form.get("username","").strip()
        pw=request.form.get("password","")
        conn=db()
        row=conn.execute(
            "SELECT * FROM users WHERE username=? AND active=1",(u,)
        ).fetchone()
        conn.close()
        if row and check_password_hash(row["password_hash"],pw):
            session.clear()
            session["username"]=row["username"]
            session["role"]=row["role"]
            audit("login")
            return redirect(url_for("panel"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    audit("logout")
    session.clear()
    return redirect(url_for("login"))

@app.route("/panel")
@login_required
def panel():
    if session.get("role") == "admin":
        return redirect(url_for("admin_users"))
    return render_template("user.html", username=session["username"], role=session["role"])

@app.route("/admin/users", methods=["GET","POST"])
@login_required
@admin_required
def admin_users():
    conn=db()
    if request.method=="POST":
        u=request.form.get("username","").strip()
        pw=request.form.get("password","")
        if u and pw:
            try:
                conn.execute("INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?)",
                    (u,generate_password_hash(pw),"user",datetime.now(timezone.utc).isoformat()))
                conn.commit()
                audit(f"created user {u}")
            except sqlite3.IntegrityError:
                pass
    users=conn.execute("SELECT username,role,active,created_at FROM users ORDER BY id").fetchall()
    user_count=len(users)
    conn.close()
    rows="".join(f"<tr><td>{x['username']}</td><td>{x['role']}</td><td>{'active' if x['active'] else 'disabled'}</td><td>{x['created_at']}</td></tr>" for x in users)
    telegram_status = "bot bridge configured" if BOT_API_URL and "YOUR-WISPBYTE-BOT-DOMAIN" not in BOT_API_URL else "bot bridge URL required"
    return render_template("admin.html", username=session["username"], user_count=user_count,
                           telegram_status=telegram_status, rows=rows)

@app.route("/admin/audit")
@login_required
@admin_required
def admin_audit():
    conn=db()
    rows=conn.execute("SELECT username,action,created_at FROM audit ORDER BY id DESC LIMIT 200").fetchall()
    conn.close()
    body="".join(f"<tr><td>{r['username']}</td><td>{r['action']}</td><td>{r['created_at']}</td></tr>" for r in rows)
    return render_template("audit.html", rows=body)

@app.route("/api/status")
@login_required
def api_status():
    return jsonify({
        "status":"ok","version":"3.0.0",
        "features":["admin-panel","user-panel","audit-log",
                    "telegram-control","token-api"]
    })

# Telegram credentials are kept ONLY in wispbyte_bot/bot.py.\n# The Vercel API talks to the bot over its authenticated HTTP bridge.\n\n# ============================================================
#  PART 6 — Wispbyte Telegram Bot Data Bridge
# ============================================================

def data_api_authorized():
    # Accept either the existing web-panel session or the API key.
    return ("username" in session) or (request.headers.get("X-API-Key") == BOT_API_KEY)

@app.route("/api/data", methods=["POST"])
def api_data_store():
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    body = request.get_json(silent=True) or {}
    code = body.get("code", 0)
    data = body.get("data")
    record_id = body.get("id")
    if code not in (0, 1):
        return jsonify({"code":0,"error":"code must be 0 or 1"}), 400
    if data is None:
        return jsonify({"code":0,"error":"data is required"}), 400
    try:
        result, status = bot_request("POST", "/api/data", {"id": record_id, "code": code, "data": data})
        if status < 400 and isinstance(result, dict):
            # Public API response requested: {code, secret_code}
            result = {"code": 1, "secret_code": result.get("secret_code")}
        if "username" in session:
            audit(f"data store code={code}")
        return jsonify(result), status
    except Exception as e:
        return jsonify({"code":0,"error":str(e)}), 502

@app.route("/api/data", methods=["GET"])
def api_data_get():
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    record_id = request.args.get("id")
    code = request.args.get("code")
    limit = request.args.get("limit", "50")
    secret_code = request.args.get("secret_code")
    try:
        params = []
        if record_id: params.append(f"id={record_id}")
        if code is not None: params.append(f"code={code}")
        if secret_code: params.append(f"secret_code={secret_code}")
        params.append(f"limit={limit}")
        path = "/api/data" + ("?" + "&".join(params) if params else "")
        result, status = bot_request("GET", path)
        if "username" in session:
            audit("data get")
        return jsonify(result), status
    except Exception as e:
        return jsonify({"code":0,"error":str(e)}), 502

@app.route("/api/data/secret/<secret_code>", methods=["GET"])
def api_data_secret(secret_code):
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    if not re.fullmatch(r"\d{20}", secret_code):
        return jsonify({"code":0}), 400
    try:
        result, status = bot_request("GET", "/api/data?secret_code=" + secret_code)
        return jsonify(result), status
    except Exception:
        return jsonify({"code":0}), 502

@app.route("/api/data/<int:record_id>", methods=["DELETE"])
def api_data_delete(record_id):
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    try:
        result, status = bot_request("DELETE", f"/api/data/{record_id}")
        if "username" in session:
            audit(f"data delete id={record_id}")
        return jsonify(result), status
    except Exception as e:
        return jsonify({"code":0,"error":str(e)}), 502

@app.route("/api/bot-control/status", methods=["GET"])
def bot_control_status():
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    try:
        result, status = bot_request("GET", "/api/control/status")
        return jsonify(result), status
    except Exception as e:
        return jsonify({"code":0,"error":str(e)}), 502


@app.route("/api/bot-control/store", methods=["POST"])
def bot_control_store():
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    body = request.get_json(silent=True) or {}
    if "data" not in body:
        return jsonify({"code":0,"error":"data is required"}), 400
    try:
        result, status = bot_request("POST", "/api/control/store", body)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"code":0,"error":str(e)}), 502


@app.route("/api/bot-control/get/<secret_code>", methods=["GET"])
def bot_control_get(secret_code):
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    if not re.fullmatch(r"\d{20}", secret_code):
        return jsonify({"code":0}), 400
    try:
        result, status = bot_request("GET", "/api/control/get/" + secret_code)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"code":0,"error":str(e)}), 502


@app.route("/api/bot-control/delete/<int:record_id>", methods=["DELETE"])
def bot_control_delete(record_id):
    if not data_api_authorized():
        return jsonify({"code":0,"error":"Unauthorized"}), 401
    try:
        result, status = bot_request("DELETE", f"/api/control/delete/{record_id}")
        return jsonify(result), status
    except Exception as e:
        return jsonify({"code":0,"error":str(e)}), 502

# Existing token functionality is retained, with authentication added.
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/token", methods=["GET"])
@login_required
def get_jwt_token():
    uid=request.args.get("uid")
    password=request.args.get("password")
    if not uid or not password:
        return jsonify({
            "status":"error",
            "error":"Both uid and password parameters are required"
        }),400
    try:
        token_data=generate_jwt_token(uid,password)
        audit("token generation")
        return jsonify(token_data),200
    except Exception as e:
        return jsonify({
            "status":"error",
            "error":f"Failed to generate token: {str(e)}"
        }),500

init_db()

# ============================================================
#  ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0",
            port=8080,
            debug=False)
