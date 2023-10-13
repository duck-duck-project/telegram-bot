from dataclasses import dataclass

__all__ = (
    'InsufficientFundsForWithdrawalError',
    'InsufficientFundsForTransferError',
    'InsufficientFundsForBetError',
)


@dataclass(frozen=True, slots=True)
class InsufficientFundsForWithdrawalError(Exception):
    amount: int

    def __str__(self):
        return f'Insufficient funds for withdrawal: {self.amount=}'


class InsufficientFundsForTransferError(Exception):
    pass


class InsufficientFundsForBetError(Exception):
    pass
