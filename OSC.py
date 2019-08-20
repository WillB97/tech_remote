class OSC():
  def __init__(self, host='127.0.0.1',port=53000, server=None):
    'Create OSC instance for communicating with a host using the local and remote ports'
    # import only done at instantiation to improve loading times
    from pythonosc import udp_client as osc_client
    from pythonosc import osc_server,dispatcher

    self.client = osc_client.SimpleUDPClient(host,port)
    self.reply = ("","")
    if type(server) == int:
      disp = dispatcher.Dispatcher()
      disp.set_default_handler(self.process_reply)
      server = osc_server.ThreadingOSCUDPServer((host,server),disp)
      server.timeout = 3
    self.server = server
    
  def send_command(self, uri, val):
    self.client.send_message(uri,val)
    if self.server:
      self.server.handle_request()
    return self.reply
 
  def process_reply(self, address, *args):
    self.reply = (address,args)