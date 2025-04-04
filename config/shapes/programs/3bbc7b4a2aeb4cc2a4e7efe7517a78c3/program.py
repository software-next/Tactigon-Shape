from numbers import Number

tap_hold = None
tap_hold_counter = None

import time
from datetime import datetime
from tactigon_shapes.modules.shapes.extension import ShapesPostAction, LoggingQueue
from tactigon_shapes.modules.braccio.extension import BraccioInterface, CommandStatus, Wrist, Gripper
from tactigon_shapes.modules.tskin.models import TSkin, Gesture, Touch, OneFingerGesture, TwoFingerGesture, HotWord, TSpeechObject, TSpeech
from pynput.keyboard import Controller as KeyboardController, HotKey, KeyCode
from typing import List, Optional, Union


tap_hold = False
tap_hold_counter = 0

# This is the main function that runs your code. Any
# code blocks you add to this section will be executed.

def check_gesture(gesture: Optional[Gesture], gesture_to_find: str) -> bool:
    if not gesture:
        return False

    return gesture.gesture == gesture_to_find

def check_touch(touch: Optional[Touch], finger_gesture: str, actions: List[ShapesPostAction]) -> bool:
    if not touch:
        return False
    _g_one = None
    try:
        _g_one = OneFingerGesture[finger_gesture]
        if touch.one_finger == _g_one:
            return True
    except:
        pass
    _g_two = None
    try:
        _g_two = TwoFingerGesture[finger_gesture]
        if touch.two_finger == _g_two:
            return True
    except:
        pass
    return False

def check_speech(tskin: TSkin, logging_queue: LoggingQueue, hotwords: List[Union[HotWord, List[HotWord]]]):
    def build_tspeech(hws: List[Union[HotWord, List[HotWord]]]) -> Optional[TSpeechObject]:
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
        debug(logging_queue, f"Waiting for command...")
        r = tskin.listen(tspeech)
        if r:
            debug(logging_queue, "Listening....")
            text_so_far = ""
            t = None
            while True:
                t = tskin.transcription

                if t:
                    break

                if text_so_far != tskin.text_so_far:
                    text_so_far = tskin.text_so_far
                    debug(logging_queue, f"Listening: {text_so_far}")
                time.sleep(tskin.TICK)

            if t and t.path is not None:
                debug(logging_queue, f"Command found: {[hw.word for hw in t.path]}")
                return [hw.word for hw in t.path]

    debug(logging_queue, "Cannot listen...")
    return []

def keyboard_press(keyboard: KeyboardController, commands: List[KeyCode]):
    for k in commands:
        _k = k.char if isinstance(k, KeyCode) and k.char else k
        keyboard.press(_k)
    for k in commands[::-1]:
        _k = k.char if isinstance(k, KeyCode) and k.char else k
        keyboard.release(_k)

def braccio_move(braccio: Optional[BraccioInterface], logging_queue: LoggingQueue, x: float, y: float, z: float):
    if braccio:
        res = braccio.move(x, y, z)
        if res:
            if res[0]:
                debug(logging_queue, f"Braccio command executed in {round(res[2], 2)}s.")
            else:
                debug(logging_queue, f"Braccio command error: {res[1].name}")
        else:
            debug(logging_queue, "Braccio not connected")
    else:
        debug(logging_queue, "Braccio not configured")

def braccio_wrist(braccio: Optional[BraccioInterface], logging_queue: LoggingQueue, wrist: Wrist):
    if braccio:
        res = braccio.wrist(wrist)
        if res:
            if res[0]:
                debug(logging_queue, f"Braccio command executed in {round(res[2], 2)}s.")
            else:
                debug(logging_queue, f"Braccio command error: {res[1].name}")
        else:
            debug(logging_queue, "Braccio not connected")
    else:
        debug(logging_queue, "Braccio not configured")

def braccio_gripper(braccio: Optional[BraccioInterface], logging_queue: LoggingQueue, gripper: Gripper):
    if braccio:
        res = braccio.gripper(gripper)
        if res:
            if res[0]:
                debug(logging_queue, f"Braccio command executed in {round(res[2], 2)}s.")
            else:
                debug(logging_queue, f"Braccio command error: {res[1].name}")
        else:
            debug(logging_queue, "Braccio not connected")
    else:
        debug(logging_queue, "Braccio not configured")

def debug(logging_queue: LoggingQueue, msg: str):
    logging_queue.debug(msg)

def reset_touch(tskin: TSkin):
        if tskin.touch_preserve:
            _ = tskin.touch

# This is the main function that runs your code. Any
# code blocks you add to this section will be executed.
def app(tskin: TSkin, keyboard: KeyboardController, braccio: Optional[BraccioInterface], actions: List[ShapesPostAction], logging_queue: LoggingQueue):
    global tap_hold
    global tap_hold_counter

    gesture = tskin.gesture
    touch = tskin.touch
    if check_touch(touch, "TAP_AND_HOLD", actions):
        if tap_hold == False:
            tap_hold = True
            keyboard_press(keyboard, HotKey.parse('<f5>'))
            debug(logging_queue, 'Toggle presentation')
    elif check_touch(touch, "SINGLE_TAP", actions):
        keyboard_press(keyboard, HotKey.parse('p'))
        debug(logging_queue, 'Prev slide')
    else:
        tap_hold_counter = (tap_hold_counter if isinstance(tap_hold_counter, Number) else 0) + 1
        if tap_hold_counter >= 5:
            tap_hold = False
            tap_hold_counter = 0
    if check_gesture(gesture, "twist"):
        keyboard_press(keyboard, HotKey.parse('n'))
        debug(logging_queue, 'Next slide')
