# from peewee import IntegerField, CharField, DateTimeField
#
# from database.db_connect import BaseModel
# from utils.payments.UzumPay.init_system import UzumTransactionOperationTypeEnum, UzumTransactionOperationStateEnum, \
#     UzumTransactionStatusEnum
#
#
# class PayTransactionOperation(BaseModel):
#     id = IntegerField(primary_key=True)
#     operation_id = CharField(null=False)
#     merchant_operation_id = CharField(null=False)
#     start_at = DateTimeField(null=False)
#     done_at = DateTimeField(null=True)
#     operation_type = CharField(choices=UzumTransactionOperationTypeEnum,
#                                default=UzumTransactionOperationTypeEnum.AUTHORIZE)
#     state = CharField(choices=UzumTransactionOperationStateEnum, default=UzumTransactionOperationStateEnum.IN_PROGRESS)
#     rrn = CharField()
#     action_code_description = CharField()
#     payment_system_name = CharField()
#
# class UzumTransaction(BaseModel):
#     id = IntegerField(primary_key=True)
#     order_id = CharField(null=False)
#     status = CharField(choices=UzumTransactionStatusEnum,
#                        default=UzumTransactionStatusEnum.REGISTERED)
#     action_code = IntegerField()
#     merchant_order_id = CharField()
#     amount = IntegerField()
#     total_amount = IntegerField(null=True)
#     completed_amount = IntegerField(null=True)
#     refunded_amount = IntegerField(null=True)
#     reversed_amount = IntegerField(null=True)
#
