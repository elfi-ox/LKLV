#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon


; Liste des touches à surveiller
global keys := Map(
    "ctrl", false,
    "alt", false,
    "shift", false,
    "lwin", false,
    "ralt", false  ; ralt est souvent AltGr
)

global lastState := ""
global waitingForKeyAfterYRelease := false
global prevYState := 0

; Timer pour surveiller les touches toutes les 100 ms
SetTimer WatchKeys, 100

WatchKeys() {
    global keys, lastState, waitingForKeyAfterYRelease, prevYState

    code := ""
    code .= GetKeyState("Ctrl") ? "1" : "0"
    code .= GetKeyState("Alt") ? "1" : "0"
    code .= GetKeyState("Shift") ? "1" : "0"
    code .= GetKeyState("LWin") || GetKeyState("RWin") ? "1" : "0"
    code .= "0" ; réservé pour Fn
    code .= GetKeyState("Y") ? "1" : "0"

    send_code := code
    if (GetKeyState("CapsLock", "T") && (code = "000000" || code = "000001")) {
        send_code := "200000"
    }

    ; Detect Y release while Ctrl and Alt are pressed
    if (GetKeyState("y") && GetKeyState("Ctrl") && GetKeyState("Alt")) {
        SendToAPI(send_code)
        Sleep 1000
    }


    if send_code != lastState {
        lastState := send_code
        SendToAPI(send_code)
    }
    
}

SendToAPI(code) {
    try {
        json := Format('{"code":"{}"}', code)  ; Construction propre du JSON

        HTTP := ComObject("WinHttp.WinHttpRequest.5.1")
        HTTP.Open("POST", "http://127.0.0.1:8765/key_state", false)
        HTTP.SetRequestHeader("Content-Type", "application/json")
        HTTP.Send(json)
        ;ToolTip "Envoi: " code 
        ;SetTimer(() => ToolTip(), -1000)
    } catch Error as e {
        ; ToolTip "Erreur d’envoi API : " e.Message
        ExitApp
    }
}
