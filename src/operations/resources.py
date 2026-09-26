"""Portable resource checks that fail before an OOM/disk-full write corrupts a run."""
from __future__ import annotations
import ctypes, os, shutil
from pathlib import Path

GiB=1024**3
def memory_available_bytes():
 try:
  import psutil
  return psutil.virtual_memory().available
 except ImportError:
  if os.name=='nt':
   class M(ctypes.Structure): _fields_=[('dwLength',ctypes.c_ulong),('dwMemoryLoad',ctypes.c_ulong),('ullTotalPhys',ctypes.c_ulonglong),('ullAvailPhys',ctypes.c_ulonglong),('ullTotalPageFile',ctypes.c_ulonglong),('ullAvailPageFile',ctypes.c_ulonglong),('ullTotalVirtual',ctypes.c_ulonglong),('ullAvailVirtual',ctypes.c_ulonglong),('ullAvailExtendedVirtual',ctypes.c_ulonglong)]
   m=M();m.dwLength=ctypes.sizeof(M);ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m));return m.ullAvailPhys
  return os.sysconf('SC_AVPHYS_PAGES')*os.sysconf('SC_PAGE_SIZE')
def resource_snapshot(path='.'):
 disk=shutil.disk_usage(path)
 return {'ram_available_gb':round(memory_available_bytes()/GiB,2),'disk_free_gb':round(disk.free/GiB,2),'disk_total_gb':round(disk.total/GiB,2)}
def assert_capacity(path, resources, estimated_write_gb=0):
 s=resource_snapshot(path); reserve=float(resources.get('disk_reserve_gb',0))+estimated_write_gb
 if s['disk_free_gb'] < reserve: raise RuntimeError(f"insufficient disk: {s['disk_free_gb']} GiB free; require reserve {reserve} GiB")
 hard=float(resources.get('ram_hard_limit_gb',0))
 # A hard limit is a cap on safely usable memory, not a requirement for a machine's free memory.
 if hard and s['ram_available_gb'] < min(4.0,hard*.04): raise RuntimeError(f"insufficient available RAM: {s['ram_available_gb']} GiB; refusing to start")
 return s
