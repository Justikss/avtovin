from database.db_connect import manager
# from database.tables.payment_transaction import UzumTransaction, PayTransactionOperation
# import uzum_payments

# uzum_payments.client.ApiClient.Async()

class PaymentManager:
    def __init__(self):
        pass
        # self.transaction_operations = PayTransactionOperation
        # self.uzum_transactions = UzumTransaction

    async def insert_uzum(self, data: dict):
        pass
        # return await manager.create(self.uzum_transactions, **data)

    async def insert_operation_state(self, data: dict):
        pass
        # return await manager.create(self.transaction_operations, **data)

payments_manager = PaymentManager()