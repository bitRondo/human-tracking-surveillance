from django.core import mail

def checkEmailConnectivity():
    connection = mail.get_connection()
    try:
        connection.open()
        connection.close()
        return True
    except:
        return False
