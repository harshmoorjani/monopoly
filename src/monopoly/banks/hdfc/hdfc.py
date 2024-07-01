import logging

from monopoly.config import CreditStatementConfig, passwords
from monopoly.constants import (
    BankNames,
    CreditTransactionPatterns,
    StatementBalancePatterns, SubTextIdentifier,
)
from ..base import BankBase

logger = logging.getLogger(__name__)


class Hdfc(BankBase):
    credit_config = CreditStatementConfig(
        bank_name=BankNames.HDFC,
        statement_date_pattern=r"Statement\sDate:(\d{2}/\d{2}/\d{4})",
        transaction_pattern=CreditTransactionPatterns.HDFC,
        prev_balance_pattern=StatementBalancePatterns.HDFC,
        only_one_previous_balance=True,
        round_off_final_due=True,
        transaction_date_contains_year=True
    )

    identifiers = [
        SubTextIdentifier(text="HDFC")
    ]

    passwords = passwords.hdfc_pdf_passwords
