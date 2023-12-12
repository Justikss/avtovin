class NonExistentIdException(BaseException):
    pass

class NonExistentTariffException(BaseException):
    pass

class TariffHasClientsException(BaseException):
    pass

class TariffExpiredException(BaseException):
    pass

class SellerWithoutTariffException(BaseException):
    pass

class UserExistsError(BaseException):
    pass

class CarExistsError(BaseException):
    pass

class SubtractLastFeedback(BaseException):
    pass