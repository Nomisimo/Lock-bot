# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 23:43:06 2025

@author: kolja
"""
from enum import Enum

# from https://api.nuki.io/#/Smartlock/SmartlockResource_get_get
# from https://api.nuki.io/#/SmartlockLog

class DEVICE_TYPE(Enum):
    """ The device type, used by /smartlock, /log 
        0 .. keyturner, 1 .. box, 
        2 .. opener,    3 .. smartdoor, 
        4 .. smartlock 3.0/4. Gen
    """
    keyturner = 0
    nukbox = 1
    opener = 2
    smartdoor = 3
    smartlock = 4
    
    unknown = 255 # added manually
    
class DOOR_STATE(Enum):
    """ The door state, used by /smartlock, /logs
        0 .. unavailable/not paired, 
        1 .. deactivated, 
        2 .. door closed, 
        3 .. door opened, 
        4 .. door state unknown, 
        5 .. calibrating, 
        16 .. uncalibrated, 
        240 .. removed,
        255 .. unknown
    """
    unavailable = 0
    deactivated = 1
    door_closed = 2
    door_opened = 3
    door_unknown = 4
    calibration = 5
    
    uncalibrated = 16
    removed = 240
    unknown = 255
    
    
class TRIGGER(Enum):
    """ The action trigger, used by /smartlock, /log.
    The state trigger: 
        0 .. system, 
        1 .. manual, 
        2 .. button, 
        3 .. automatic, 
        4 .. web (type=1 only), 
        5 .. app (type=1 only), 
        6 .. continuous mode (type=2 only), 
        7 .. accessory (type=3 only)
        255 .. keypad
    """
    system = 0
    manual = 1
    button = 2
    automatic = 3
    web = 4
    app = 5
    auto_lock = 6
    accessory = 7
    keypad = 255
    
    unknown = 99
    
class ACTION(Enum):
    """ The action, used by /smartlock (1-5), /logs (1-255)
        1 .. unlock, 
        2 .. lock, 
        3 .. unlatch, 
        4 .. lock'n'go, 
        5.. lock'n'go with unlatch, 
        
        208 .. door warning ajar, 
        209 door warning status mismatch, 
        224 .. doorbell recognition (only Opener), 
        240 .. door opened, 
        241 .. door closed, 
        242 .. door sensor jammed, 
        243 .. firmware update, 
        250 .. door log enabled, 
        251 .. door log disabled, 
        252 .. initialization, 
        253 .. calibration, 
        254 .. log enabled, 
        255 .. log disabled
    """
    unknown = 0 # added 
    unlock  = 1
    lock    = 2
    unlatch = 3
    lockngo = 4
    lockngo_unlatch = 5

    door_warning_ajar = 208
    door_warning_mismatch = 209
    doorbell_recognition = 224
    
    door_opened = 240
    door_closed = 241
    door_jammed = 242
    
    door_log_enabled = 250
    door_log_disabled = 251
    initialization = 252
    log_enabled = 254
    log_disabled = 255
      
class LOCK_MODE(Enum):
    """ The smartlock mode, used by /smartlock
        0 .. uninitialized, 1 .. pairing, 
        2 .. door(default), 3 .. continuous (type=2 only), 
        4 .. maintenance,   5 .. off-door charging.
    """
    uninitialized = 0
    pairing = 1
    door = 2
    continous = 3
    maintenance = 4
    offdoor_charging = 5

class LOCK_STATE(Enum):
    """ The smartlock state, used by /smartlock: 
        type=0/3/4: 
            0 .. uncalibrated, 
            1 .. locked, 
            2 .. unlocking, 
            3 .. unlocked, 
            4 .. locking, 
            5 .. unlatched, 
            6 .. unlocked (lock 'n' go), 
            7 .. unlatching, 
            224 .. Error wrong entry code, 
            225 .. Error wrong Fingerprint, 
            254 .. motor blocked, 
            255 .. undefined; 
        type=2: 
            0 .. untrained, 1 .. online, 
            3 .. ring to open active, 
            5 .. open, 7 .. opening, 
            253 .. boot run, 
            255 .. undefined
    """
    uncalibrated = 1
    locked = 1
    unlocking = 2
    unlocked = 3
    locking = 4
    unlatched = 5
    unlocked_lockngo = 6
    unlatching = 7
    
    error_wrong_code = 224
    error_wrong_finger = 225
    motor_blocked = 254
    undefined = 255
    
class SERVER_STATE(Enum):
    """ used by /smartlock,
    The server state: 
        0 .. ok, 
        1 .. unregistered, 
        2 .. auth uuid invalid, 
        3 .. auth invalid, 
        4 .. offline
    """
    ok = 0
    unregistered = 1
    auth_uuid_invalid = 2
    auth_invalid = 3
    offline = 4
        
class ADMINPIN_STATE(Enum):
    """ used by /smartlock,
    The admin pin state: 0 .. ok, 1 .. missing, 2 .. invalid
    """
    ok = 0
    missing = 1
    invalid = 2
    
class LOG_STATE(Enum):
    """ The completion state: used by /log
        0 .. Success,           1 .. Motor blocked, 
        2 .. Canceled,          3 .. Too recent, 
        4 .. Busy,              5 .. Low motor voltage, 
        6 .. Clutch failure,    7 .. Motor power failure, 
        8 .. Incomplete,        9 .. Rejected, 
        10 .. Rejected night mode, 
        254 .. Other error,     255 .. Unknown error
    """
    success         = 0
    motor_blocked   = 1
    canceled        = 2
    too_recent      = 3
    busy            = 4
    low_motor_voltage = 5
    clutch_failure  = 6
    motor_power_failure = 7
    incomplete      = 8
    rejected        = 9
    rejected_night_mode = 10
    other_error     = 254
    unknown_error   = 255
    
class LOG_SOURCE(Enum):
    """ The source of action, used by /log
    1 .. Keypad code, 2 .. Fingerprint, 0 .. Default
    """    
    keypad = 1
    fingerprint = 2
    default = 0

    unknown = 255
    