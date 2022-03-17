
class UserHelper:
    def __init__(self, configFile="users.conf"):
        with open(configFile) as file:
            self.userIds = file.readlines()
        print(self.userIds)

    def validUser(self, update):
        try:
            return str(update.message.from_user['id']) in self.userIds
        except:
            return False