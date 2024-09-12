from exceptions.base import ApplicationError

__all__ = (
    'InsufficientFundsForWithdrawalError',
    'InsufficientFundsForTransferError',
    'InsufficientFundsForBetError',
    'TransactionDoesNotExistError',
    'TransferRollbackExpiredError',
    'TransactionDoesNotBelongToUserError',
    'InsufficientFundsForTransferRollbackError',
)


class InsufficientFundsForWithdrawalError(ApplicationError):

    def __init__(self, detail: str, amount: int):
        super().__init__(detail)
        self.amount = amount


class InsufficientFundsForTransferError(ApplicationError):
    pass


class InsufficientFundsForBetError(ApplicationError):
    pass


class TransactionDoesNotExistError(ApplicationError):
    pass


class TransferRollbackExpiredError(ApplicationError):
    pass


class TransactionDoesNotBelongToUserError(ApplicationError):
    pass


class InsufficientFundsForTransferRollbackError(ApplicationError):
    pass
