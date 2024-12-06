import sys
import json
import asyncio
from os import path
from bleak import BleakScanner
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from typing import Optional

from .manager import start_tskin, load_tskin, stop_tskin, get_tskin

from ..socketio import get_socket_app

from ...config import app_config
from ...models import BASE_PATH, TSkinModel, VoiceConfig, TSkinConfig, Hand, GestureConfig

if sys.platform != "darwin":
    from ...models import TSpeechObject, TSpeech, HotWord

from ...utils.extensions import stop_apps
from ...utils.request_utils import get_from_request

bp = Blueprint('tskin', __name__, url_prefix="/tskin", template_folder="templates")

@bp.before_request
def manage():
    stop_apps()

@bp.route("add", methods=["GET"])
def add():
    return render_template("tskin/add.jinja")

if sys.platform == "darwin":
    @bp.route("scan", methods=["GET"])
    def scan():
        async def find_devices():
            devices = await BleakScanner.discover(cb=dict(use_bdaddr=True))
            return filter(lambda d: str(d.name).startswith("TSKIN") or str(d.name).startswith("TACTI"), devices)

        devices = asyncio.run(find_devices())
        tskins = [{"name": d.name, "id": d.address, "address": str(d.details[0].identifier())} for d in devices]
        
        return json.dumps(tskins)
else:
    @bp.route("scan", methods=["GET"])
    def scan():
        async def find_devices():
            devices = await BleakScanner.discover()
            return filter(lambda d: str(d.name).startswith("TSKIN") , devices)

        devices = asyncio.run(find_devices())
        tskins = [{"name": d.name, "id": d.address, "address": d.address} for d in devices]

        return json.dumps(tskins)

@bp.route("hand", methods=["POST"])
def hand():
    tskin_name = get_from_request("tskin_name")
    tskin_mac = get_from_request("tskin_mac")

    if not (tskin_mac and tskin_name):
        flash("You need to select a Tactigon Skin to proceed", category="danger")
        return redirect(url_for("tskin.add"))

    return render_template("tskin/hand.jinja", tskin_name=tskin_name, tskin_mac=tskin_mac)

@bp.route("model", methods=["POST"])
def model():
    tskin_name = get_from_request("tskin_name")
    tskin_mac = get_from_request("tskin_mac")

    if not tskin_name or not tskin_mac:
        return redirect(url_for("tskin.add"))

    hand = get_from_request("hand")

    if not hand:
        flash("Please select a hand", "danger")
        return redirect(url_for("tskin.add"))

    models = list(filter(lambda m: m.hand.value==hand, app_config.MODELS))

    if len(models) == 1:
        return redirect(url_for("tskin.save", tskin_name=tskin_name, tskin_mac=tskin_mac, hand=hand, model=models[0].name), code=307)

    return render_template("tskin/model.jinja", tskin_name=tskin_name, tskin_mac=tskin_mac, hand=hand, models=models)

@bp.route("/remove", methods=["GET"])
def remove():
    socket_app = get_socket_app()

    tskin = get_tskin()

    if tskin is None:
        flash(F"Tactigon skin {hand} not configured!", "danger")
        return redirect(url_for("main.index"))

    if socket_app:
        socket_app.stop()
    
    stop_tskin()

    app_config.TSKIN = None
    app_config.TSKIN_VOICE = None
    
    app_config.save()
    current_app.config.from_object(app_config)

    if socket_app:
        socket_app.init_app(current_app)

    return redirect(url_for("main.index"))

@bp.route("save", methods=["POST"])
def save():
    socket_app = get_socket_app()

    tskin_name = get_from_request("name")
    tskin_mac = get_from_request("mac")

    if not tskin_name or not tskin_mac:
        flash("Please select a Tactigon Skin", "danger")
        return {"error": "name or mac error"}, 500

    hand = get_from_request("hand")
    
    if not hand:
        flash("Please select a hand", "danger")
        return {"error": "hand error"}, 500

    # if not model_name:
    #     flash("Please select a model", "danger")
    #     return redirect(url_for("tskin.add", tskin_name=tskin_name, tskin_mac=tskin_mac, hand=hand), code=307)
        
    hand = Hand(hand)
    model_name = "MODEL_01_" + hand.name[0]

    current_model: Optional[TSkinModel] = None

    for model in app_config.MODELS:
        if model.name == model_name:
            current_model = model
            break

    if current_model is None:
        flash("Error MODEL", "danger")
        return {"error": "model error"}, 500
        # return redirect(url_for("tskin.add"))
    
    gesture_config = GestureConfig(
        path.join(BASE_PATH, "models", current_model.name, "model.pickle"),
        path.join(BASE_PATH, "models", current_model.name, "encoder.pickle"),
        current_model.name,
        current_model.date,
        [g.gesture for g in current_model.gestures]
    )

    tskin_config = TSkinConfig(
        tskin_mac,
        hand,
        tskin_name,
        gesture_config
    )

    if sys.platform != "darwin":
        voice_config = VoiceConfig(
            path.join(BASE_PATH, "speech", "deepspeech-0.9.3-models.tflite"),
            path.join(BASE_PATH, "speech", "tos.scorer"),
            vad_padding_ms=800,
            vad_frame=20,
            voice_timeout=3,
            silence_timeout=3,
            voice_commands_notification=path.join(BASE_PATH, "config", "audio", "trigger.wav"),
            voice_commands=TSpeechObject(
                [
                    TSpeech(
                        [HotWord("start"), HotWord("stop")],
                        TSpeechObject(
                            [
                                TSpeech(
                                    [HotWord("application"), HotWord("program")],
                                ),
                                TSpeech(
                                    [HotWord("voice"), HotWord("gesture"), HotWord("touch")],
                                    TSpeechObject(
                                        [
                                            TSpeech(
                                                [HotWord("tutorial")],
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ),
                    TSpeech(
                        [HotWord("enter"), HotWord("exit")],
                        TSpeechObject(
                            [
                                TSpeech([HotWord("application"), HotWord("program")])
                            ]
                        )
                    ),
                ]
            )
        )

        voice_config.stop_hotword = None
    else:
        voice_config = None

    if socket_app:
        socket_app.stop()

    stop_tskin()
    app_config.TSKIN = tskin_config
    app_config.TSKIN_VOICE = voice_config

    app_config.save()
    current_app.config.from_object(app_config)

    load_tskin(tskin_config, voice_config)
    tskin = start_tskin()

    if socket_app and tskin:
        socket_app.setTSkin(tskin)

    return json.dumps(tskin_config.toJSON()), 200

if sys.platform != "darwin":
    @bp.route("play", methods=["POST"])
    def play(base_path = ""):
        tskin = get_tskin()

        if not tskin:
            return "Error: TSkin not present"
        
        data = request.get_json(force=True)

        if not data:
            return "Error: No JSON in request"
        
        audio_file = data.get("audio_file")

        if not audio_file:
            return "Error: No audio_file in JSON"
        
        base_path = data.get("base_path")

        if base_path:
            audio_file = path.join(base_path, audio_file)

        tskin.play(audio_file)

        return "Ok"
else:
    @bp.route("play", methods=["POST"])
    def play(base_path = ""):
        return "Not Implemented", 500