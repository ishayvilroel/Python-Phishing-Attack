#!/usr/bin/env python

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT 
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.

import smtpd
import smtplib
import asyncore
import dns.resolver

port = 2525
debug = False

def get_mx_record(domain):
    records = dns.resolver.query(domain, 'MX')
    return str(records[0].exchange)


class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        for rcptto in rcpttos:
            print '[*] Sending message to {0}.'.format(rcptto)

            domain = rcptto.split('@')[1]
            mx = get_mx_record(domain)
            
            try:
                server = smtplib.SMTP(mx, 25)
                if debug:
                    server.set_debuglevel(True)
                server.sendmail(mailfrom, rcptto, data)

            except smtplib.SMTPDataError as e:
                print '[-] {0}'.format(str(e[1]))

            except smtplib.SMTPServerDisconnected as e:
                print '[-] {0}'.format(str(e))

            except smtplib.SMTPConnectError as e:
                print '[-] {0}'.format(str(e[1]))


server = CustomSMTPServer(('127.0.0.1', port), None)
print '[+] Server listening on port {0}'.format(port)
asyncore.loop()
