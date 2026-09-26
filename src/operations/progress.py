"""Small dependency-free progress display for interactive and redirected consoles."""
from __future__ import annotations
import shutil, sys, time
from .resources import resource_snapshot

class PipelineProgress:
 def __init__(self, experiment, artifacts='artifacts'):
  self.experiment=experiment; self.artifacts=artifacts; self.live=sys.stdout.isatty(); self.started=time.monotonic(); self.state={}; self.times={}; self.frames='|/-\\'; self.frame=0
  self.stages=('Dataset Preparation','Candidate Generation','Feature Extraction','Model Training','Validation','Inference','Output Writing')
  for s in self.stages:self.state[s]='Pending'
  if self.live: print(f'ML Challenge | Experiment: {experiment}')
 def update(self, stage, state, done=None, total=None):
  self.state[stage]=state
  if state=='Running' and stage not in self.times: self.times[stage]=time.monotonic()
  if self.live:
   width=max(20,min(32,shutil.get_terminal_size((100,20)).columns-58)); known=total is not None and total>0
   pct=(done/total if known else 0) if state!='Completed' else 1
   bar='#'*round(width*pct)+'-'*(width-round(width*pct)); count=f' | {done}/{total}' if known else ''
   progress=f'{pct:>4.0%}' if known or state=='Completed' else f' {self.frames[self.frame%4]}  '
   label='Running...' if state=='Running' and not known else state
   eta=''
   if known and state=='Running' and done and done>0:
    elapsed=time.monotonic()-self.times.get(stage,time.monotonic()); remaining=max(0,(total-done)*(elapsed/done)); eta=f' | ETA {int(remaining//60):02d}:{int(remaining%60):02d}'
   self.frame+=1
   print(f'\r{stage:<20} [{bar}] {progress}{count} | {label:<9}{eta}',end='',flush=True)
  elif state in ('Running','Completed','Failed','Skipped'):
   print(f'[{stage}] {state}' + (f' ({done}/{total})' if total is not None else ''))
 def resource_line(self):
  s=resource_snapshot(self.artifacts); print(f'RAM available: {s["ram_available_gb"]:.2f} GiB | Disk free: {s["disk_free_gb"]:.2f} GiB')
 def finish(self, failures=()):
  if self.live: print()
  completed=[s for s,v in self.state.items() if v=='Completed']
  print(f'Experiment {self.experiment}: completed={len(completed)}/{len(self.stages)}; failures={len(tuple(failures))}')
