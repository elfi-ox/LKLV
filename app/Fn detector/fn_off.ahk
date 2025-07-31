; #Requires AutoHotkey v2.0
atom := DllCall("GlobalFindAtom", "Str", "FnKeyActive", "UShort")
if atom {
    DllCall("GlobalDeleteAtom", "UShort", atom)
}

