#Requires AutoHotkey v2.0
#SingleInstance Ignore  ; Empêche plusieurs exécutions simultanées

atomName := "FnKeyActive"
existing := DllCall("GlobalFindAtom", "Str", atomName, "UShort")

if (existing = 0) {
    ; Crée l'atome uniquement s'il n'existe pas déjà
    DllCall("GlobalAddAtom", "Str", atomName, "UShort")
}

Sleep 3000

atom := DllCall("GlobalFindAtom", "Str", "FnKeyActive", "UShort")
if atom {
    DllCall("GlobalDeleteAtom", "UShort", atom)
}

ExitApp
