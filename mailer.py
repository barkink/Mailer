#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import sys
import re

def prompt(prompt):
    return raw_input(prompt).strip()

if len(sys.argv) < 3:
        print "Usage: " + sys.argv[0] + " <host> <port>"
        print "Or Usage: " + sys.argv[0] + " <host> <port> <fromaddr> <toaddr> <subject>"
        print "Or Usage: " + sys.argv[0] + " <host> <port> <fromaddr> <toaddr> <subject> [msg file path]"
        print "Or Usage: " + sys.argv[0] + " <host> <port> <fromaddr> <to addrs file> <subject> [msg file path]"
        print "Or Usage: " + sys.argv[0] + " <host> <port> <headers file> <to addr> [msg file path]"
        print "Or Usage: " + sys.argv[0] + " <host> <port> <headers file> <to addrs file> [msg file path]"
        sys.exit(0)
elif len(sys.argv) > 3:
        if "@" in sys.argv[3]:
            if "+" in sys.argv[3]:
                    fromaddrs = sys.argv[3].split('+')
                    fromaddr = fromaddrs[1]
                    fromname = fromaddrs[0]
            else:
                    fromaddr = sys.argv[3]
            if "@" in sys.argv[4]:
                    toaddrs  = sys.argv[4]
                    toaddrs = toaddrs.split()
            else:
                    with open(sys.argv[4]) as x:
                            toaddrs = x.readlines()
            subject  = sys.argv[5]
            if len(sys.argv) == 7:
                    with open(sys.argv[6]) as f:
                            msg1 = f.readlines()
        else:
            with open(sys.argv[3]) as h:
                    headers = h.readlines()
            for header in headers:
                if re.match("(.*)(F|f)(r|R)(o|O)(m|M)(.*)", header):
                    fromaddrs1 = header.split(' ',1)
                    #print fromaddrs1
                    if "+" in fromaddrs1[1]:
                        fromaddrs = fromaddrs1[1].split('+')
                        fromaddr = fromaddrs[1].strip("\n \"\'")
                        fromname = fromaddrs[0].strip("\n \"\'")
                    else:
                        fromaddr = fromaddrs1[1].strip("\n \"\'")
                elif re.match("(.*)(S|s)(u|U)(b|B)(j|J)(e|E)(c|C)(t|T)(.*)", header):
                    subject1 = header.split(' ',1)
                    #print subject1
                    subject = subject1[1].strip("\n \"\'")
            if "@" in sys.argv[4]:
                    toaddrs  = sys.argv[4]
                    toaddrs = toaddrs.split()
            else:
                    with open(sys.argv[4]) as x:
                            toaddrs = x.readlines()
            with open(sys.argv[5]) as m:
                msg1 = m.readlines()

else:
        fromaddr = prompt("From: ")
        toaddrs  = prompt("To: ")
        subject  = prompt("Subject: ")
for toaddr1 in toaddrs:
        toaddr = toaddr1.rstrip()
        try:
                cop = msg1
        except NameError:
                print "Enter message, end with ^D (Unix) or ^Z (Windows):"
                print fromaddr, toaddr
                msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
                        % (fromaddr, toaddr, subject))
                text = sys.stdin.readlines()
        else:
                try:
                        cop = fromname
                except NameError:
                        msg = ("From: \"%s\" <%s>\r\nTo: \"%s\" <%s>\r\nMIME-Version: 1.0\r\nContent-Type: text/html; charset=\"utf-8\"\r\nSubject: %s\r\n\r\n"
                                % (fromaddr.split("@")[0], fromaddr, toaddr.split("@")[0], toaddr, subject))
                else:
                        msg = ("From: \"%s\" <%s>\r\nTo: \"%s\" <%s>\r\nMIME-Version: 1.0\r\nContent-Type: text/html; charset=\"utf-8\"\r\nSubject: %s\r\n\r\n"
                                % (fromname, fromaddr, toaddr.split("@")[0], toaddr, subject))
                msg1 = ''.join(msg1)
                text = msg1

        msg = msg + ''.join(text)
        #print "Message length is " + repr(len(msg))
#       print msg + "\n\n"
#        print fromname + " " + fromaddr + " " + subject
#        print "Kabul?"
#        dogrulama = sys.stdin.read(1)
#        if not re.match("(y|Y)",dogrulama):
#                exit()
        try:
                server = smtplib.SMTP(sys.argv[1],sys.argv[2])
#               server.set_debuglevel(1)
                server.sendmail(fromaddr, toaddr, msg)
        except Exception as eks:
                print eks
        finally:
                server.quit()
                print "%s adresine mail basari ile gonderildi\n" % (toaddr)

