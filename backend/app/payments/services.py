from app.extensions import db
from app.payments.models import Payment

class PaymentService:
    @staticmethod
    def get_my_payments(user_id):
        return Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).all()

    @staticmethod
    def handle_webhook(transaction_id, status, reference_id, payment_type):
        """
        Mock webhook handler. 
        In reality, the webhook would provide a signature we must verify, 
        and the transaction_id or our internal payment_id to find the record.
        For this mock, we'll just find or create a payment record for demonstration.
        """
        # Let's see if we have a payment for this reference (e.g. booking id)
        payment = Payment.query.filter_by(
            reference_id=reference_id, 
            payment_type=payment_type
        ).first()

        if payment:
            payment.status = status
            payment.gateway_transaction_id = transaction_id
        else:
            # If no pending payment was created previously, create one now 
            # (assuming user_id could be inferred, but we'll use a dummy 1 for mock purposes if it doesn't exist)
            payment = Payment(
                user_id=1, # Mock fallback
                amount=0.0,
                payment_type=payment_type,
                reference_id=reference_id,
                status=status,
                gateway_transaction_id=transaction_id
            )
            db.session.add(payment)
            
        db.session.commit()
        return True
