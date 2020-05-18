import struct
import sys
import threading
import queue as Queue

try:
    import tkinter as Tkinter
    # import tkMessageBox
except ImportError:
    Tkinter = None

# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
# PY3K = sys.version_info >= (3,0)
# if PY3K:
#     source = sys.stdin.buffer
# else:
#         # Python 2 on Windows opens sys.stdin in text mode, and
#     # binary data that read from it becomes corrupted on \r\n
#     if sys.platform == "win32":
#         # set sys.stdin to binary mode
#         import os, msvcrt
#         msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
#     source = sys.stdin
if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

# Helper function that sends a message to the webapp.
def send_message(message):
    # write message size:
    # sys.stdout.write(struct.pack('I', len(message)))
    sys.stdout.write(str(len(message)))
    # write the message itself.
    sys.stdout.write(message)
    sys.stdout.flush()

# Thread that reads message from the webapp.
def read_thread_func(queue):
    message_number = 0
    while True:
        #read the message length (first 4 bytes).
        text_length_bytes = sys.stdin.read(4)

        if len(text_length_bytes) == 0:
            if queue:
                queue.put(None)
            sys.eixt(0)

        # Unpack message length as 4 byte integer.
        text_length = struct.unpack('i', text_length_bytes)[0]

        # Read the text (JSON object) of the message.
        text = sys.stdin.read(text_length).decode('utf-8')

        if queue:
            queue.put(text)
        else:
            # In headless mode just send an message.
            send_message('{msg:WJJDKDKKDKK}')


if Tkinter:
  class NativeMessagingWindow(Tkinter.Frame):
    def __init__(self, queue):
      self.queue = queue

      Tkinter.Frame.__init__(self)
      self.pack()

      self.text = Tkinter.Text(self)
      self.text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
      self.text.config(state=Tkinter.DISABLED, height=10, width=40)

      self.messageContent = Tkinter.StringVar()
      self.sendEntry = Tkinter.Entry(self, textvariable=self.messageContent)
      self.sendEntry.grid(row=1, column=0, padx=10, pady=10)

      self.sendButton = Tkinter.Button(self, text="Send", command=self.onSend)
      self.sendButton.grid(row=1, column=1, padx=10, pady=10)

      self.after(100, self.processMessages)

    def processMessages(self):
      while not self.queue.empty():
        message = self.queue.get_nowait()
        if message == None:
          self.quit()
          return
        self.log("Received %s" % message)

      self.after(100, self.processMessages)

    def onSend(self):
      text = '{"text": "' + self.messageContent.get() + '"}'
      self.log('Sending %s' % text)
      try:
        send_message(text)
      except IOError:
        tkinter.messagebox.showinfo('Native Messaging Example',
                              'Failed to send message.')
        sys.exit(1)

    def log(self, message):
      self.text.config(state=Tkinter.NORMAL)
      self.text.insert(Tkinter.END, message + "\n")
      self.text.config(state=Tkinter.DISABLED)


def Main():
  if not Tkinter:
    send_message('"Tkinter python module wasn\'t found. Running in headless ' +
                 'mode. Please consider installing Tkinter."')
    read_thread_func(None)
    sys.exit(0)

  queue = Queue.Queue()

  main_window = NativeMessagingWindow(queue)
  main_window.master.title('Native Messaging Example')

  thread = threading.Thread(target=read_thread_func, args=(queue,))
  thread.daemon = True
  thread.start()

  main_window.mainloop()

  sys.exit(0)


if __name__ == '__main__':
  Main()
