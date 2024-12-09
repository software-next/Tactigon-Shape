can_move = None
pos_x = None
pos_z = None
pos_wrist = None
pos_gripper = None
pos_y = None

import time
from datetime import datetime
from queue import Queue
from tactigon_shapes.modules.shapes.extension import ShapesPostAction
from tactigon_shapes.modules.braccio.extension import BraccioInterface, CommandStatus, Wrist, Gripper
from tactigon_shapes.modules.tskin.models import TSkin, OneFingerGesture, TwoFingerGesture, HotWord, TSpeechObject, TSpeech
from pynput.keyboard import Controller as KeyboardController, HotKey, KeyCode
from typing import List, Optional


can_move = True
pos_x = 0
pos_y = 50
pos_z = 100
pos_wrist = True
pos_gripper = True

# This is the main function that runs your code. Any
# code blocks you add to this section will be executed.

def check_gesture(tskin: TSkin, gesture: str) -> bool:
    g = tskin.gesture_preserve
    if not g:
        return False
    if g.gesture == gesture:
        _ = tskin.gesture
        return True
    return False

def check_touch(tskin: TSkin, finger_gesture: str, actions: List[ShapesPostAction]) -> bool:
    touch = tskin.touch_preserve
    if not touch:
        return False
    _g_one = None
    try:
        _g_one = OneFingerGesture[finger_gesture]
        if touch.one_finger == _g_one:
            _ = tskin.touch
            return True
    except:
        pass
    _g_two = None
    try:
        _g_two = TwoFingerGesture[finger_gesture]
        if touch.two_finger == _g_two:
            _ = tskin.touch
            return True
    except:
        pass
    return False

def check_speech(tskin: TSkin, debug_queue: Queue, hotwords: List[HotWord]):
    def build_tspeech(hws: List[HotWord]) -> Optional[TSpeechObject]:
        if not hws:
            return None

        hw, *rest = hws

        return TSpeechObject(
            [
                TSpeech(hw, build_tspeech(rest))
            ]
        )

    tspeech = build_tspeech(hotwords)

    if tspeech and tskin.can_listen:
        debug(debug_queue, f"Waiting for commands: {', '.join([hw.word for hw in hotwords])}")
        r = tskin.listen(tspeech)
        if r:
            debug(debug_queue, "Listening....")
            text_so_far = ""
            while tskin.is_listening:
                if text_so_far != tskin.text_so_far:
                    text_so_far = tskin.text_so_far
                    debug(debug_queue, f"Listening: {text_so_far}")
                time.sleep(0.1)

            t = tskin.transcription
            if t and t.path is not None:
                for hw in hotwords:
                    if hw not in t.path:
                        debug(debug_queue, f"Incomplete command... Only got {', '.join([hw.word for hw in t.path])}")
                        return False

                debug(debug_queue, f"Command found!")
                return True

    debug(debug_queue, "Cannot listen...")
    return False

def keyboard_press(keyboard: KeyboardController, commands: List[KeyCode]):
    for k in commands:
        _k = k.char if isinstance(k, KeyCode) and k.char else k
        keyboard.press(_k)
    for k in commands[::-1]:
        _k = k.char if isinstance(k, KeyCode) and k.char else k
        keyboard.release(_k)

def braccio_move(braccio: Optional[BraccioInterface], debug_queue: Queue, x: float, y: float, z: float):
    if braccio:
        res = braccio.move(x, y, z)
        if res:
            if res[0]:
                debug(debug_queue, f"Braccio command executed in {round(res[2], 2)}s.")
            else:
                debug(debug_queue, f"Braccio command error: {res[1].name}")
        else:
            debug(debug_queue, "Braccio not connected")
    else:
        debug(debug_queue, "Braccio not configured")

def braccio_wrist(braccio: Optional[BraccioInterface], debug_queue: Queue, wrist: Wrist):
    if braccio:
        res = braccio.wrist(wrist)
        if res:
            if res[0]:
                debug(debug_queue, f"Braccio command executed in {round(res[2], 2)}s.")
            else:
                debug(debug_queue, f"Braccio command error: {res[1].name}")
        else:
            debug(debug_queue, "Braccio not connected")
    else:
        debug(debug_queue, "Braccio not configured")

def braccio_gripper(braccio: Optional[BraccioInterface], debug_queue: Queue, gripper: Gripper):
    if braccio:
        res = braccio.gripper(gripper)
        if res:
            if res[0]:
                debug(debug_queue, f"Braccio command executed in {round(res[2], 2)}s.")
            else:
                debug(debug_queue, f"Braccio command error: {res[1].name}")
        else:
            debug(debug_queue, "Braccio not connected")
    else:
        debug(debug_queue, "Braccio not configured")

def debug(debug_queue: Queue, msg: str):
    debug_queue.put(F"[{datetime.now().isoformat()}] {msg}")

def reset_touch(tskin: TSkin):
        if tskin.touch_preserve:
            _ = tskin.touch

# This is the main function that runs your code. Any
# code blocks you add to this section will be executed.
def app(tskin: TSkin, keyboard: KeyboardController, braccio: Optional[BraccioInterface], actions: List[ShapesPostAction], debug_queue: Queue):
    global pos_x
    global pos_y
    global pos_z
    global can_move
    global pos_wrist
    global pos_gripper
    if check_gesture(tskin, "up"):
        pos_z = 100
        can_move = True
    elif check_gesture(tskin, "down"):
        pos_z = -20
        can_move = True
    elif check_gesture(tskin, "twist"):
        pos_wrist = not pos_wrist
        if pos_wrist:
            braccio_wrist(braccio, debug_queue, Wrist['HORIZONTAL'])
        else:
            braccio_wrist(braccio, debug_queue, Wrist['VERTICAL'])
    elif check_touch(tskin, "SINGLE_TAP", actions):
        pos_gripper = not pos_gripper
        if pos_gripper:
            braccio_gripper(braccio, debug_queue, Gripper['OPEN'])
        else:
            braccio_gripper(braccio, debug_queue, Gripper['CLOSE'])
    if can_move:
        braccio_move(braccio, debug_queue, pos_x, pos_y, pos_z)
        can_move = False
