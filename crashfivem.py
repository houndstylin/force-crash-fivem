import ctypes
import psutil

def crash_fivem():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'FiveM.exe':
            pid = proc.info['pid']
            print(f"[+] Found FiveM with PID {pid}")

            # open the process handle
            PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
            process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            
            if not process_handle:
                print(f"Failed to open process: {ctypes.windll.kernel32.GetLastError()}")
                return False
            
            # create a remote thread that points to an invalid addres
            THREADFUNC = ctypes.WINFUNCTYPE(ctypes.c_ulong)
            pThreadFunc = THREADFUNC(0xDEADBEEF)

            thread_id = ctypes.c_ulong(0)
            if not ctypes.windll.kernel32.CreateRemoteThread(process_handle, None, 0, pThreadFunc, None, 0, ctypes.byref(thread_id)):
                print(f"[-] Failed to create remote thread: {ctypes.windll.kernel32.GetLastError()}")
                ctypes.windll.kernel32.CloseHandle(process_handle)
                return False
            
            print("[+] Crashed Fivem")
            
            # close the process handle
            ctypes.windll.kernel32.CloseHandle(process_handle)
            return True
    
    print("FiveM.exe process not found.")
    return False

if __name__ == "__main__":
    crash_fivem()