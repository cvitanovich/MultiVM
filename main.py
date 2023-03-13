# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from multiprocessing import Process
import subprocess
import textwrap
import time

class QEMU():
    _cmd = "qemu-system-x86_64"
    _drive = ""
    _memory = 2048
    _net = "nic"
    _port = 2222
    _smp = 2
    _cpu_host = True
    _q35 = True
    _ovmf = False
    _ovmf_path = '/usr/share/edk2/x64/OVMF.fd'

    def __init__(self):
        pass

    def config(self, drive, mem=2048, net="nic", port=2222, cores=2):
        self._drive = drive
        self._net = net
        self._memory = mem
        self._port = port
        self._smp = cores
        self._kvm = True

    def add_dev(self):
        pass

    def print(self):
        self.run(execute=False)

    def run(self, execute=True):
        qemu = [self._cmd, '-drive', f'file={self._drive},format=raw', '-net', self._net, '-net', f'user,hostfwd=tcp::{self._port}-:22']
        if self._kvm:
            qemu.append('-enable-kvm')
        if self._cpu_host:
            qemu.append('-cpu')
            qemu.append('host')
        if self._q35:
            qemu.append('-machine')
            qemu.append('q35')
        if self._ovmf:
            qemu.append('-drive')
            qemu.append(f'if=pflash,format=raw,file={self._ovmf_path}')
        if execute:
            subprocess.run(qemu)
        else:
            out = " ".join(qemu)
            print(textwrap.fill(out, width=80))


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def ls(path='/home/andrew/'):
    print(f"Start with {path}")
    #subprocess.run(['ls',path])
    time.sleep(5)
    print()
    proc1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'python'], stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    print('out: {0}'.format(out))
    print('err: {0}'.format(err))

    print(f"Done with {path}")


if __name__ == "__main__":
    #qcow = "CentOS-7-x86_64-GenericCloud.qcow2"
    qcow = "Fedora-Cloud-Base-37-1.7.x86_64.raw"
    path = "/home/andrew/images/"
    q = QEMU()
    img = path + qcow
    print(img)
    q.config(img, port=2201)
    #q.print()
    #q.run()
    dirs = ['/home/','/opt/','/home/andrew/']
    procs = []
    for d in dirs:
        proc = Process(target=ls, args=(d,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    print("Andrew")
