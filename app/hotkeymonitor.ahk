#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon


global keys := Map(
    "ctrl", false,
    "alt", false,
    "shift", false,
    "lwin", false,
)
global lastState := ""
global waitingForKeyAfterYRelease := false
global prevYState := 0
fnState := "0"


SetTimer WatchKeys, 100
WatchKeys() {
    
    ; ## Remove the “;” below to comment. This part enables Fn detection via fn_ShortCall.ahk, fn_off.ahk, fn_on.ahk
    ;/* 
    fnState := "0"
    atomName := "FnKeyActive"

    if DllCall("GlobalFindAtom", "Str", atomName, "UShort") {
        fnState := "1"
    }
    ;*/


    global keys, lastState, waitingForKeyAfterYRelease, prevYState 
    code := ""
    code .= GetKeyState("Ctrl") ? "1" : "0"
    code .= GetKeyState("Alt") ? "1" : "0"
    code .= GetKeyState("Shift") ? "1" : "0"
    code .= GetKeyState("LWin") || GetKeyState("RWin") ? "1" : "0"
    code .=  fnState 
    code .= GetKeyState("Y") ? "1" : "0"
    if (GetKeyState("CapsLock", "T") && (code = "000000" || code = "000001")) {
        code := "200000"
    }


    ; ## Detect Y release while Ctrl and Alt are pressed
    if (GetKeyState("y") && GetKeyState("Ctrl") && GetKeyState("Alt")) {
        SendToAPI(code)
        Sleep 1000
    }


    if code != lastState {
        lastState := code
        SendToAPI(code)
    }
}

SendToAPI(code) {
    try {
        json := Format('{"code":"{}"}', code)
        HTTP := ComObject("WinHttp.WinHttpRequest.5.1")
        HTTP.Open("POST", "http://127.0.0.1:8765/key_state", false)
        HTTP.SetRequestHeader("Content-Type", "application/json")
        HTTP.Send(json)
        ;ToolTip "Sent: " code 
        ;SetTimer(() => ToolTip(), -1000)
    } catch Error as e {
        ;ToolTip " API sending error : " e.Message
        ExitApp
    }
}
