import socket
import struct

class Magicq():
  def __init__(self, host:str='127.0.0.1', port:int=6553) -> None:
    """
    Create a MagicQ remote control instance to a specified host and port
    """
    self.address = (host, port)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # add recv functionality?
    self.seq_fwd = 0
    self.seq_bkwd = 0
    self.msg = b''

  def send_command(self) -> None:
    """
    Send the bundled message as a MagicQ PERC packet
    The message buffer is cleared after the message is sent
    """
    meta = struct.pack('<BBH',self.seq_fwd,self.seq_bkwd,len(self.msg))
    self.seq_fwd += 1
    packet = b'CREP\0\0' + meta + self.msg
    print(packet)
    self.socket.sendto(packet, self.address)
    self.msg = b''

  def build_command(self, data:str='') -> None:
    'Append data to the message'
    self.msg += data.encode('ascii')
    
  def activate(self, playback:int) -> None:
    'Activate a playback on the console, 1-10 on PC'
    self.build_command(f'{playback}A')

  def release(self, playback:int) -> None:
    'Release a playback on the console, 1-10 on PC'
    self.build_command(f'{playback}R')

  def test_playback(self, playback:int) -> None:
    'Test a playback (activate with level 100%) on the console'
    self.build_command(f'{playback}T')

  def untest_playback(self, playback:int) -> None:
    'Untest a playback (release with level 0%) on the console'
    self.build_command(f'{playback}U')

  def go(self, playback:int) -> None:
    'Go on the playback on the console'
    self.build_command(f'{playback}G')

  def stop(self, playback:int) -> None:
    'Stop (go back) on the playback on the console'
    self.build_command(f'{playback}S')

  def fast_back(self, playback:int) -> None:
    'Fast back on playback (no fade) on the console'
    self.build_command(f'{playback}B')

  def fast_forward(self, playback:int) -> None:
    'Fast forward on playback (no fade) on the console'
    self.build_command(f'{playback}F')

  def level(self, playback:int, level:int) -> None:
    'Set the fader level of a playback on the console'
    self.build_command(f'{playback},{level}L')

  def jump(self, playback:int, cue:float) -> None:
    'Jump to the Cue ID on the playback'
    try:
      cue_dec=str(cue).split('.')[1]
    except IndexError:
      cue_dec=0
    self.build_command('{},{},{:<02}J'.format(playback,int(cue),cue_dec))

  def page(self, page:int) -> None:
    "Change page of playbacks"
    self.build_command(f'{page}P')

  def channel_level(self, channel:int, level:int) -> None:
    'Set channel intensity to level'
    self.build_command(f'{channel},{level}I')

  def program(self, cmd, args):
    """
    Run a remote programming command on the console
    """
    pass
