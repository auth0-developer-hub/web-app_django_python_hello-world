class Profile:
    nickname: str
    name: str
    picture: str
    updated_at: str
    email: str
    email_verified: bool
    sub: str

    def __init__(self,
                 nickname: str,
                 name: str,
                 picture: str,
                 updated_at: str,
                 email: str,
                 email_verified: bool,
                 sub: str
                 ):
        self.nickname = nickname
        self.name = name
        self.picture = picture
        self.updated_at = updated_at
        self.email = email
        self.email_verified = email_verified
        self.sub = sub
