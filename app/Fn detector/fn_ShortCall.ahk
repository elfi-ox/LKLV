#Requires AutoHotkey v2.0
#SingleInstance Ignore
atomName := "FnKeyActive"
existing := DllCall("GlobalFindAtom", "Str", atomName, "UShort")


if (existing = 0) {
    DllCall("GlobalAddAtom", "Str", atomName, "UShort")
}


Sleep 3000 ; timer


atom := DllCall("GlobalFindAtom", "Str", "FnKeyActive", "UShort")
if atom {
    DllCall("GlobalDeleteAtom", "UShort", atom)
}


ExitApp