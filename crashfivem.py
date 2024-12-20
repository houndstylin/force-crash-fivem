import ctypes
import psutil

def crash_fivem():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'FiveM.exe':
            pid = proc.info['pid']
            print(f"[+] Found FiveM process [{pid}]")
            PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF) # open the process handle
            process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            
            if not process_handle:
                print(f"could not open process: {ctypes.windll.kernel32.GetLastError()}")
                return False
            THREADFUNC = ctypes.WINFUNCTYPE(ctypes.c_ulong) # create a remote thread that points to an invalid addres
            pThreadFunc = THREADFUNC(0xDEADBEEF)

            thread_id = ctypes.c_ulong(0)
            if not ctypes.windll.kernel32.CreateRemoteThread(process_handle, None, 0, pThreadFunc, None, 0, ctypes.byref(thread_id)):
                print(f"[-] Failed: {ctypes.windll.kernel32.GetLastError()}")
                ctypes.windll.kernel32.CloseHandle(process_handle)
                return False
            
            print("[+] Crashed Fivem")
            ctypes.windll.kernel32.CloseHandle(process_handle) # close the process handle
            return True
    
    print("[-] Couldnt find FiveM.")
    return False

if __name__ == "__main__":
    crash_fivem()
