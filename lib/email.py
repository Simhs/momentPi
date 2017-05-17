# -*- coding:utf-8 -*- 
import os, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import time 
import datetime 
import random 

gmail_username="Moment Pi"
gmail_user="tlsghdwo90@gmail.com" 
gmail_pwd="cjfrnjs501"
attach_file="/home/pi/Desktop/moment/testlapse100.mp4" 

def send_gmail(to, subject, text, attach): 
	msg=MIMEMultipart('alternative') 
	msg['From']=gmail_username
	msg['To']=to 	
	msg['Subject']=subject
	msg.attach(MIMEText(text, 'plain', 'utf-8'))

	part=MIMEBase('application','octet-stream') 
	part.set_payload(open(attach, 'rb').read()) 
	Encoders.encode_base64(part) 
	part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(attach))
	msg.attach(part) 

	mailServer=smtplib.SMTP("smtp.gmail.com",587)
	mailServer.ehlo() 
	ret,m = mailServer.starttls()
	mailServer.ehlo() 
	ret,m = mailServer.login(gmail_user,gmail_pwd)
	if (ret!=235):
		print("login fail")
		return
	mailServer.sendmail(gmail_user, to, msg.as_string())
	mailServer.close() 

def mainLoop(): 
	title = "Moment Pi"
	email = "qra0428@naver.com"
	message = str(datetime.datetime.now())
	print "Program Ready"
	print "----------------------" 
	print "[" + str(datetime.datetime.now()) + "] Sending email to " + email + "..."

	send_gmail(email,title,message,attach_file) 

	print "Mails have just been sent. The program is going to end." 

if __name__ == "__main__": 
	mainLoop()
