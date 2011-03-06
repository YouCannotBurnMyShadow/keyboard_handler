import wx

from windows import WindowsKeyboardHandler
from main import KeyboardHandler

__all__ = ['WXKeyboardHandler', 'WXControlKeyboardHandler']

class WXKeyboardHandler(WindowsKeyboardHandler):

 def __init__ (self, parent):
  super(WXKeyboardHandler, self).__init__()
  self.parent = parent
  self.key_ids = {}

 def register_key(self, key, function):
  super(WXKeyboardHandler, self).register_key(key, function)
  key_id = wx.NewId()
  parsed = self.parse_key(key)
  self.parent.RegisterHotKey(key_id, *parsed)
  self.parent.Bind(wx.EVT_HOTKEY, lambda evt: self.process_key(evt, key_id), id=key_id)
  self.key_ids[key] = key_id

 def unregister_key (self, key, function):
  super(WXKeyboardHandler, self).unregister_key(key, function)
  key_id = self.key_ids[key]
  answer = self.parent.UnregisterHotKey(key_id)
  self.parent.Unbind(wx.EVT_HOTKEY, id=key_id)
  del(self.key_ids[key])

 def process_key (self, evt, id):
  evt.Skip()
  for i in self.key_ids:
   if self.key_ids[i] == id:
    self.handle_key(i)

class WXControlKeyboardHandler(wx.StaticText, KeyboardHandler):

 def __init__(self, *a, **k):
  wx.StaticText.__init__(self, *a, **k)
  KeyboardHandler.__init__(self)
  self.wx_replacements = {}
  for i in [d for d in dir(wx) if d.startswith('WXK_')]:
   self.wx_replacements[getattr(wx, i)] = i[4:].lower()
  self.Bind(wx.EVT_KEY_DOWN, self.process_key, self)
  self.SetFocus()

 def process_key(self, evt):
  keycode = evt.GetKeyCode()
  keyname = self.wx_replacements.get(keycode, None)
  modifiers = ""
  replacements = (   (evt.ControlDown(), 'control+'),
   (evt.AltDown(),     'alt+'),
   (evt.ShiftDown(),   'shift+'),
   (evt.MetaDown(),    'win+')
  )
  for mod, ch in (replacements):
   if mod:
    modifiers += ch
  if keyname is None:
   if 27 < keycode < 256:
    keyname = chr(keycode).lower()
   else:
    keyname = "(%s)unknown" % keycode
  key = modifiers + keyname
  self.handle_key(key)
