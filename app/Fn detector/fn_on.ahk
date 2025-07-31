#Requires AutoHotkey v2.0
#SingleInstance Ignore
atomName := "FnKeyActive"

existing := DllCall("GlobalFindAtom", "Str", atomName, "UShort")
if (existing = 0) {
    DllCall("GlobalAddAtom", "Str", atomName, "UShort")
}
ExitApp


