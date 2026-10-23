import gdb

gdb.execute("set pagination off")
gdb.execute("set confirm off")
gdb.execute("set print thread-events off")

RED, YELLOW, CYAN, BOLD, RESET = "\033[91m", "\033[93m", "\033[96m", "\033[1m", "\033[0m"
SKIP = ("c++", "bits/", "ucrt", "vcruntime")

def on_stop(event):
    if not isinstance(event, gdb.SignalEvent):
        return
    print(f"\n{RED}{BOLD}{'='*50}\n💥 CRASH: {event.stop_signal}\n{'='*50}{RESET}")

    f = gdb.selected_frame()
    user_frame = None
    while f:
        sal = f.find_sal()
        if sal.symtab and not any(t in sal.symtab.filename.lower() for t in SKIP):
            user_frame = f
            break
        f = f.older()

    if user_frame:
        sal = user_frame.find_sal()
        print(f"{YELLOW}File:     {CYAN}{sal.symtab.filename}{RESET}")
        print(f"{YELLOW}Line:     {CYAN}{sal.line}{RESET}")
        print(f"{YELLOW}Function: {CYAN}{user_frame.name()}{RESET}")
    else:
        print(f"{YELLOW}No user source frame found (missing -g?){RESET}")

    print(f"{BOLD}Call Stack:{RESET}")
    gdb.execute("bt")

def on_exit(event):
    code = getattr(event, "exit_code", None)
    print(f"\nProgram exited (code {code}).")
    gdb.execute("quit")

gdb.events.stop.connect(on_stop)
gdb.events.exited.connect(on_exit)

gdb.execute("run < input.txt")
