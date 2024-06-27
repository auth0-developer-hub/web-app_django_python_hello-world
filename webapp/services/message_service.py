class MessageService():

    def public_message(self):
        return {
            'text': 'This is a public message.'
        }

    def protected_message(self):
        return {
            'text': 'This is a protected message.'
        }

    def admin_message(self):
        return {
            'text': 'This is an admin message.'
        }
