#!/usr/bin/env python
# Email Library
# 
# Requires valid SMTP configuration to run!
# 
import mimetypes
import smtplib
import os
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
try:
    # Python 3
    from configparser import ConfigParser, NoSectionError, NoOptionError
except ImportError:
    from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from email.errors import MessageError

EMAIL_CONFIG_FILE = "email_config.ini"

def write_example_email_config():
    """Write an example email config.
    
    Write an example configuration to allow people to edit.
    
    Args:
        None.
    
    Returns:
        Nothing.
    """
    config = ConfigParser()
    config.add_section("email_lib")
    config.set("email_lib", "server", "smtp.example.com")
    config.set("email_lib", "port", "587")
    config.set("email_lib", "username", "USERNAME")
    config.set("email_lib", "password", "PASSWORD")
    with open(EMAIL_CONFIG_FILE, "w") as fh:
        config.write(fh)

def get_email_credentials():
    """Write an example email config.
    
    Write an example configuration to allow people to edit.
    
    Args:
        None.
    
    Returns:
        Tuple with the server hostname (str), server port (int), server
        username (str), server password (str), and from email
        address (str) in that order.
    """
    config = ConfigParser()
    read_files = config.read(EMAIL_CONFIG_FILE)
    
    if len(read_files) == 0:
        write_example_email_config()
        raise Exception("No email configuration file found. A new file, %s, has been created." % EMAIL_CONFIG_FILE)
    
    if config.has_section("email_lib"):
        try:
            server_hostname = config.get("email_lib", "server")
            server_port     = config.get("email_lib", "port")
            server_username = config.get("email_lib", "username")
            server_password = config.get("email_lib", "password")
            email_from      = config.get("email_lib", "from")
        except (NoSectionError, NoOptionError):
            raise Exception("Configuration seems to be missing some fields.")
        
        if not (server_hostname and server_port and server_username
            and server_password and email_from):
            raise Exception("Configuration seems to be have invalid field value(s).")
        
        return server_hostname, int(server_port), server_username, server_password, email_from
    else:
        raise Exception("Configuration seems to be missing some fields and/or is invalid. (Missing emails section!)")

def send_email(from_email = None, to_email = None,
    subject = None, plain_text_email = None,
    html_email = None, attachments = None):
    """Send an email out, given the email specific parameters.
    
    Send an email out.
    
    Args:
        from_email (str): String specifying the email that you are
            sending from. Can either be a simple "person@example.com"
            or "First Last <person@example.com>".
        to_email (str or list): String or list specifying the emails
            that you are sending to. Can either be a simple
            "person@example.com" or "First Last <person@example.com>".
            If you specify a string, emails are separated by comma.
            If you specify a list, each element should be a string.
        subject (str): String specifying the email's subject.
        plain_text_email (str): String specifying the plain text email
            message. If set to None, no plain text email will be sent.
        html_email (str): String specifying the HTML email message. If
            set to None, no HTML email will be sent.
        attachments (list of str or dict): List of strings and/or dicts
            specifying the attachments to send.
            
            For external files that need to be read, specify a string of
            the file name within the list. If you want to send a string
            as a file, specify a dictionary in the following format:
            { "filename" : "DATA" }, e.g. { "cool.txt" : "Cool beans" }.
            
            Multiple filename/data (key/value) pairs can exist within
            this dictionary.
            
            For image attachments, you may reference them with
            src="cid:image-file-name". (Content-ID for image attachments
            is automatically set to the filename.)
    
    Returns:
        bool: boolean specifying whether the email was successfully sent
        or not.
    """
    
    NAME_EMAIL_REGEX = r'<(.*)>'
    NUM_ATTEMPTS = 5
    
    # Fetch email credentials
    server_hostname, server_port, server_username, server_password, email_from = get_email_credentials()
    
    # Check if subject is defined
    if not subject:
        raise Exception("Subject is not specified!")
    
    # Check if plain_text_email or html_email is defined
    if not (plain_text_email or html_email):
        raise Exception("A plain text email or HTML email must be specified!")
    
    # Check if to_email is set
    if not to_email:
        raise Exception("To email is not set!")
    
    # Set from email if it isn't set
    if not from_email:
        from_email = email_from
    
    # Format to_email to the correct parts
    if type(to_email) == str:
        to_email_list = [e.strip() for e in to_email.split(",")]
        to_email_str  = to_email
    elif type(to_email) == list:
        # Ensure that the list is correctly filtered... in case we have
        # names included in the parameters.
        # Format is generally FIRST LAST <email@company.com>
        to_email_list = [re.findall(NAME_EMAIL_REGEX, e.strip())[0] if len(re.findall(NAME_EMAIL_REGEX, e.strip())) > 0 else e.strip() for e in to_email]
        to_email_str  = ", ".join(to_email)
    else:
        raise Exception("Invalid to_email specified! Got %s but requested str/list..." % (str(type(to_email))))
    
    def add_attachment(filename, data):
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        
        maintype, subtype = ctype.split("/", 1)
        
        # http://stackoverflow.com/a/23171609/1094484
        if maintype == "text":
            # Note: we should handle calculating the charset
            if type(data) == bytes:
                data = data.decode("utf-8")
            part = MIMEText(data, _subtype=subtype)
        elif maintype == "image":
            part = MIMEImage(data, _subtype=subtype)
            part.add_header("Content-ID", "<%s>" % filename)
        elif maintype == "audio":
            part = MIMEAudio(data, _subtype=subtype)
        else:
            part = MIMEBase(maintype, subtype)
            part.set_payload(data)
            encoders.encode_base64(part)
        
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(filename))
        msg.attach(part)
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        if plain_text_email:
            msg.attach(MIMEText(plain_text_email, "plain"))
            
        if html_email:
            msg.attach(MIMEText(html_email, "html"))
        
        for attachment in attachments:
            if type(attachment) == str:
                add_attachment(os.path.basename(attachment), open(attachment, "rb").read())
            elif type(attachment) == dict:
                for filename in attachment:
                    add_attachment(filename, attachment[filename])
            else:
                raise Exception("Invalid attachment specified! Got %s but requested str/dict..." % (str(type(attachment))))
        
    except MessageError:
        # This is a dev error, let's raise hell
        raise
    
    # Number of retries
    tries = 0
    successfully_sent = False
    
    while tries < NUM_ATTEMPTS:
        try:
            # SMTP Login
            mailserver = smtplib.SMTP(server_hostname, server_port)
            
            # Identify ourselves to smtp gmail client
            mailserver.ehlo()
            
            # Secure our email with tls encryption
            mailserver.starttls()
            
            # Re-identify ourselves as an encrypted connection
            mailserver.ehlo()
            
            # Actually login with our credentials
            mailserver.login(server_username, server_password)
            
            # Send away!
            mailserver.sendmail(from_email, to_email, msg.as_string())
            
            # If everything is sent, just exit here.
            mailserver.quit()
            
            # Set return value
            successfully_sent = True
            
            break
        except smtplib.SMTPException:
            print("Failed to send email, waiting 5s to retry.")
            time.sleep(5)
        tries += 1
    
    return successfully_sent

