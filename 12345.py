from pysendpulse.pysendpulse import PySendPulse

if __name__ == "__main__":
    TOKEN_STORAGE = 'memcached'
    SPApiProxy = PySendPulse(REST_API_ID, REST_API_SECRET, TOKEN_STORAGE)
    email = {
        'subject': 'This is the test task from REST API',
        'html': '<p>This is a test task from https://sendpulse.com/api REST API!</p>',
        'text': 'This is a test task from https://sendpulse.com/api REST API!',
        'from': {'name': 'SigaretNet.by', 'email': 'sigaretnetbymail@gmail.com'},
        'to': [
            {'name': 'Kirill', 'email': 'mr.mcdi.576@gmail.com'}
        ]
    }
    SPApiProxy.smtp_send_mail(email)