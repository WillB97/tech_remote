#! /usr/bin/env python3

import sys
import cmd
from Magicq import Magicq
from OSC import OSC
from typing import List

class MagiqShell(cmd.Cmd):
  intro = 'MagicQ shell.  Type help or ? to list commands.\n'
  prompt = '(magicq) '
  completekey = 'Tab'
  stdout = sys.stdout
  stdin = sys.stdin
  cmdqueue = []
  
  def __init__(self,magicq: Magicq) -> None:
    self.magicq = magicq
    
  def do_activate(self,arg):
    'Activate playback 1-10 on the console, activate <playback>'
    try:
      self.magicq.activate(int(arg.split()[0]))
      self.magicq.send_command()
      print('Activating playback ' + arg.split()[0])
    except:
      pass
  def do_release(self,arg):
    'Release playback 1-10 on the console, release <playback>'
    try:
      self.magicq.release(int(arg.split()[0]))
      self.magicq.send_command()
      print('Releasing playback ' + arg.split()[0])
    except:
      pass
  def do_test(self,arg):
    'Test playback 1-10 (activate with level 100%), test <playback>'
    try:
      self.magicq.test_playback(int(arg.split()[0]))
      self.magicq.send_command()
      print('Testing playback ' + arg.split()[0])
    except:
      pass
  def do_untest(self,arg):
    'Un-test playback 1-10 (release with level 0%), untest <playback>'
    try:
      self.magicq.untest_playback(int(arg.split()[0]))
      self.magicq.send_command()
      print('Untesting playback ' + arg.split()[0])
    except:
      pass
  def do_go(self,arg):
    'Go on playback 1-10, go <playback>'
    try:
      self.magicq.go(int(arg.split()[0]))
      self.magicq.send_command()
      print('Go on playback ' + arg.split()[0])
    except:
      pass
  def do_stop(self,arg):
    'Stop (go back) on playback 1-10, stop <playback>'
    try:
      self.magicq.stop(int(arg.split()[0]))
      self.magicq.send_command()
      print('Stop playback ' + arg.split()[0])
    except:
      pass
  def do_back(self,arg):
    'Fast back on playback 1-10 (no fade), back <playback>'
    try:
      self.magicq.fast_back(int(arg.split()[0]))
      self.magicq.send_command()
      print('Fast back playback ' + arg.split()[0])
    except:
      pass
  def do_forward(self,arg):
    'Fast forward on playback 1-10 (no fade), forward <playback>'
    try:
      self.magicq.fast_forward(int(arg.split()[0]))
      self.magicq.send_command()
      print('Fast forward playback ' + arg.split()[0])
    except:
      pass
  def do_level(self,arg):
    'Set playback fader level, level <playback> <level>'
    try:
      self.magicq.level(int(arg.split()[0]),int(arg.split()[1]))
      self.magicq.send_command()
      print('Set playback ' + arg.split()[0] + ' to ' +  arg.split()[1])
    except:
      pass
  def do_jump(self,arg):
    'Jump to Cue Id on playback, jump <playback> <cue>'
    try:
      self.magicq.jump(int(arg.split()[0]),float(arg.split()[1]))
      self.magicq.send_command()
      print('Jump to cue ' + arg.split()[1] + ' on playback ' +  arg.split()[0])
    except:
      pass
  def do_page(self,arg):
    'Change page, page <page no>'
    try:
      self.magicq.page(int(arg.split()[0]))
      self.magicq.send_command()
      print('Change page to ' + arg.split()[0])
    except:
      pass
  def do_channel(self,arg):
    'Set intensity channel to level, channel <channel> <level>'
    try:
      print(type(arg))
      self.magicq.channel_level(int(arg.split()[0]),int(arg.split()[1]))
      self.magicq.send_command()
      print('Set channel ' + arg.split()[0] + ' to ' +  arg.split()[1])
    except:
      pass
  def do_program(self,arg):
    'Remote programming command mode'
    self.magicq.program(arg.split()[0],arg.split()[1:])

class TUI():
  def __init__(self, args:List[str]) -> None:
    if len(args) < 1:
      self.usage()
      return
    try:
      scheme,path = args[0].split('//',1)
      addr,uri = path.split('/',1)
      host_info = addr.split(':')
      if len(host_info) < 1:
        raise IndexError
    except (ValueError,IndexError):
      print("Invalid format")
      self.usage()
      return
    if scheme == 'osc:':
      client = OSC(host=host_info[0],port=int(host_info[1]) if len(host_info) > 1 else 53000, server=int(host_info[2]) if len(host_info) > 2 else None)
      self.OSC_process(client, uri=uri, args=args[1:])
    elif scheme == 'magicq:':
      client = Magicq(host=host_info[0],port=host_info[1] if len(host_info) > 1 else 6553)
      self.magicq_process(client, ['+' + uri] + args[1:])
    else:
      self.usage()
  
  def magicq_process(self, client:Magicq, args:List[str]=None):
    if args[0] == '+shell':
      try:
        MagiqShell(client).cmdloop()
      except:
        return
    cmd = args[0][1:]
    arg_list = []
    for arg in args[1:]:
      if not arg.startswith('+'):
        arg_list.append(arg)
      else:
        self.magicq_cmd(client, cmd, arg_list)
        arg_list = []
        cmd = arg[1:]
    self.magicq_cmd(client, cmd, arg_list)
    client.send_command()

  def magicq_cmd(self, client:Magicq, arg:str, cmd_line:List[str]=[]):
    if arg == 'activate':
      client.activate(int(cmd_line[0]))
    elif arg == 'release':
      client.release(int(cmd_line[0]))
    elif arg == 'test':
      client.test_playback(int(cmd_line[0]))
    elif arg == 'untest':
      client.untest_playback(int(cmd_line[0]))
    elif arg == 'go':
      client.go(int(cmd_line[0]))
    elif arg == 'stop':
      client.stop(int(cmd_line[0]))
    elif arg == 'back':
      client.fast_back(int(cmd_line[0]))
    elif arg == 'forward':
      client.fast_forward(int(cmd_line[0]))
    elif arg == 'level':
      client.level(int(cmd_line[0]),int(cmd_line[1]))
    elif arg == 'jump':
      client.jump(int(cmd_line[0]),float(cmd_line[1]))
    elif arg == 'page':
      client.page(int(cmd_line[0]))
    elif arg == 'channel':
      client.channel_level(int(cmd_line[0]),int(cmd_line[1]))
    elif arg == 'program':
      client.program(cmd_line[0],cmd_line[1:])
  
  def OSC_process(self, client:OSC, uri:str, args:List[str]):
    print(client.send_command('/'+uri,args))

  def usage(self):
    print('Usage:')
    print('\t ./cli.py osc://host:tx_port[:rx_port]/uri <arg> ...')
    print('\t ./cli.py magicq://host:port/cmd <arg> ... [+<cmd> <arg> ...]')

if __name__ == '__main__':
  TUI(sys.argv[1:])