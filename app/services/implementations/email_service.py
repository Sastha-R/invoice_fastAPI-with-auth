import logging
import smtplib
from decimal import Decimal
from email.message import EmailMessage
from email.utils import formatdate
from app.core.config import settings


logger = logging.getLogger("invoice_app")


class EmailService:

    def send_invoice_confirmation(
        self,
        customer_email: str,
        customer_name: str,
        invoice_number: str,
        product_name: str,
        quantity: int,
        unit_price: Decimal,
        total_amount: Decimal,
    ) -> bool:

        message = EmailMessage()

        message["Subject"] = f"Invoice Confirmation - {invoice_number}"
        message["From"] = settings.email_address
        message["To"] = customer_email
        message["Date"] = formatdate(localtime=True)

        email_body = f"""
Hello {customer_name},

Your invoice has been created successfully.

Invoice Details

Invoice Number: {invoice_number}
Product: {product_name}
Quantity: {quantity}
Unit Price: {unit_price:.2f}
Total Amount: {total_amount:.2f}

Please keep this email for your records.

Regards,
Invoice Management
"""

        message.set_content(email_body)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
                smtp.login(
                    settings.email_address,
                    settings.email_password,
                )

                smtp.send_message(message)

            logger.info(
                f"Invoice confirmation email sent for invoice {invoice_number}"
            )

            return True

        except (smtplib.SMTPException, OSError) as exc:
            logger.exception(
                f"Failed to send invoice confirmation email for invoice {invoice_number} : {exc}",
            )

            return False