import os 
import subprocess
import threading

def starting_playright_mcp():
    print("STARTING MCP SERVER....")

    command = "npx @playwright/mcp@latest"

    process = subprocess.Popen(
        command, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True, 
        shell=True,
    )


    

    

    return process


try : 
    mcp_server = starting_playright_mcp()
    print("MCP SERVER HAS STARTED (press Enter to stop)")
    
    # Print stdout in a background thread
    def read_output():
        for line in mcp_server.stdout:
            print("[SERVER SAID]    :", line, end="")
    
    t = threading.Thread(target=read_output, daemon=True)
    t.start()
    
    input()  # Block until user presses Enter
    mcp_server.kill()
    print("MCP SERVER STOPPED")

except Exception as error: 
    print("ERROR IN MCP SERVER:" , error)