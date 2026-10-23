import gdb

# remove bloat from gdb
gdb.execute("set pagination off")
gdb.execute("set confirm off")
gdb.execute("set print thread-events off")

# ANSI colors
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def on_stop(event):
    if isinstance(event, gdb.SignalEvent):
        print(f"\n{RED}{BOLD}{'='*50}{RESET}")
        print(f"{RED}{BOLD}💥 CRASH DETECTED: {event.stop_signal}{RESET}")
        print(f"{RED}{BOLD}{'='*50}{RESET}")
        
        try:
            frame = gdb.selected_frame()
            sal = frame.find_sal()
            
            if sal.symtab:
                print(f"{YELLOW}File:     {CYAN}{sal.symtab.filename}{RESET}")
                print(f"{YELLOW}Line:     {CYAN}{sal.line}{RESET}")
                print(f"{YELLOW}Function: {CYAN}{frame.name()}{RESET}")
            else:
                print(f"{YELLOW}Crash occurred outside user source code.{RESET}")
                
            print(f"{RED}{'='*50}{RESET}")
            print(f"{BOLD}Call Stack:{RESET}")
            gdb.execute("bt")
        except Exception as e:
            print(f"Could not extract frame details: {e}")
            
        print(f"{RED}{'='*50}{RESET}")
        print(f"{YELLOW}👉 Entering interactive GDB session for debugging...\n{RESET}")

gdb.events.stop.connect(on_stop)

print()

# execute the prog.
gdb.execute("run < input.txt", to_string = True)

print()

# exit cleanly
gdb.execute("quit")