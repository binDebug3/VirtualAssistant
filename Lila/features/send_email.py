import smtplib

def mail(sender, password, receiver, message):
    try:
        # dallin I should figure out how this works
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender, password)
        mail.sendmail(sender, receiver, message)
        mail.close()
        return True
    except Exception as ex:
        print(ex)
        return False


# dallin look for a gmail api
# dallin implement reading emails
# implement ML program to check email for me