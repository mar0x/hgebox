on run dst
  tell application "Mail"

    set sel to selection
    set c to (1)
    repeat with msg in sel

      set src to (source of msg)
      set cs to c as string
      set fname to dst & ":" & cs & ".eml" as string
      -- log fname

      set fd to open for access fname with write permission
      write src to fd starting at eof
      close access fd

      set c to (c + 1)
    end repeat
  end tell

  return

end run
