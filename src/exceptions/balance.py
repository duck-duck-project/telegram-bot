__all__ = (
    'InsufficientFundsForWithdrawalError',
    'InsufficientFundsForTransferError',
    'InsufficientFundsForBetError',
    'TransactionDoesNotExistError',
    'TransferRollbackExpiredError',
    'TransactionDoesNotBelongToUserError',
    'InsufficientFundsForTransferRollbackError',
)


class InsufficientFundsForWithdrawalError(Exception):

    def __init__(self, amount: int):
        self.amount = amount

    def __str__(self):
        return f'Insufficient funds for withdrawal: {self.amount=}'


class InsufficientFundsForTransferError(Exception):
    pass


class InsufficientFundsForBetError(Exception):
    pass


class TransactionDoesNotExistError(Exception):
    pass


class TransferRollbackExpiredError(Exception):
    pass


class TransactionDoesNotBelongToUserError(Exception):
    pass


class InsufficientFundsForTransferRollbackError(Exception):
    pass
