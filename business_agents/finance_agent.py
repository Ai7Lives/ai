from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TransactionType(Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'
    INVESTMENT = 'investment'

@dataclass
class FinancialTransaction:
    transaction_id: str
    type: TransactionType
    amount: float
    currency: str
    account: str
    timestamp: str
    verified: bool = False

class FinanceAgent:
    """Autonomous financial operations agent."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.accounts: Dict[str, float] = {}
        self.transactions: List[FinancialTransaction] = []
        self.budget_allocations: Dict[str, float] = {}
        self.spending_limits: Dict[str, float] = {}
    
    def create_account(self, account_id: str, initial_balance: float = 0.0) -> bool:
        """Create financial account."""
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = initial_balance
        return True
    
    def record_transaction(self, transaction: FinancialTransaction) -> bool:
        """Record financial transaction."""
        if transaction.account not in self.accounts:
            return False
        
        if transaction.type == TransactionType.EXPENSE:
            if self.accounts[transaction.account] < transaction.amount:
                return False
            self.accounts[transaction.account] -= transaction.amount
        elif transaction.type == TransactionType.INCOME:
            self.accounts[transaction.account] += transaction.amount
        
        transaction.verified = True
        transaction.timestamp = datetime.utcnow().isoformat()
        self.transactions.append(transaction)
        return True
    
    def get_financial_report(self) -> Dict[str, Any]:
        """Generate financial report."""
        total_assets = sum(self.accounts.values())
        return {
            'total_assets': total_assets,
            'accounts': self.accounts,
            'transactions': len(self.transactions)
        }
