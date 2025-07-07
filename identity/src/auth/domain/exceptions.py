class AuthCertificateLoadException(Exception):
    pass


class AuthError(Exception):
    pass


class AuthAccessTokenInvalid(AuthError):
    pass

class AuthAccessTokenExpired(AuthError):
    pass