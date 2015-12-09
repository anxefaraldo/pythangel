__author__ = 'angel'
import OSC
import threading

#------OSC Server-----------------#
receive_address = 'localhost', 2243

# OSC Server. there are three different types of server.
s = OSC.ThreadingOSCServer(receive_address)

# this registers a 'default' handler (for unmatched messages)
s.addDefaultHandlers()

# define a message-handler function for the server to call.
def default_handler(addr, tags, stuff, source):
    print addr, stuff


s.addMsgHandler("/test", default_handler)
s.addMsgHandler("/dos", default_handler)

def main():
    # Start OSCServer
    print "Starting OSCServer"
    st = threading.Thread(target=s.serve_forever)
    st.start()
    print "windows"
main()