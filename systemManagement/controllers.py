from django.core import mail

def checkEmailConnectivity():
    connection = mail.get_connection()
    print(connection)
    try:
        connection.open()
        print("Opened")
        connection.close()
        return True
    except:
        return False
