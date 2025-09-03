from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import os
from typing import Dict, Optional, List, Any
# from celery import shared_task

logger = logging.getLogger(__name__)

class EmailServices:
    def __init__(self):
        self.from_email = settings.DEFAULT_FROM_EMAIL

    def send_html_email(self,
                        subject:str,
                        # --- text content
                        template_name:str,
                        context:Dict[str, Any],
                        # ---
                        to_emails:List[str],
                        from_email:Optional[str]=None,
                        cc_emails:Optional[List[str]]=None,
                        bcc_emails:Optional[List[str]]=None,
                        attachments:Optional[List[Dict[str, Any]]]=None,
                        reply_to: Optional[List[str]] = None,
                        headers: Optional[Dict[str, str]] = None) -> bool: # return True if email sent successfully, False otherwise
        try:
            html_content = render_to_string(template_name, context)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject=subject,
                # -- is the temp_name and the context together
                body=text_content,
                # ----
                from_email=from_email or self.from_email,
                # not required -->
                to=to_emails,
                cc=cc_emails,
                bcc=bcc_emails,
                reply_to=reply_to,
                headers=headers
            )
            msg.attach_alternative(html_content, 'text/html')

            if attachments:
                for attachment in attachments:
                    if 'file_path' in attachment:
                        msg.attach_file(attachment['file_path'])
                    elif 'content' in attachment:
                        msg.attach(attachment['filename'], attachment['content'], attachment.get('mimetype',  'application/octet-stream'))
            msg.send()
            logger.info(f"Email sent successfully to {', '.join(to_emails)}")
            return True
        except Exception as e:
            logger.error(f"fiald to send email: {str(e)}")
            return False
        
    def send_simple_email(self,
                        subject:str,
                        message:str,
                        to_emails: List[str],
                        from_email: Optional[str]=None,
                        fail_silently: bool= False
                        ):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email or self.from_email,
                recipient_list=to_emails,
                fail_silently=fail_silently
            )
            logger.info(f"Simple email sent to: {', '.join(to_emails)}")

            return True
        except Exception as e:
            logger.error(f"Fiald to send simple email: {str(e)}")
            return False
    
    def send_welcome_email(self, user_email:str, user_name:str):
        context = {
            'user_name': user_name,
            'site_name': 'Car Services',
            'contact_email': self.from_email
        }
        return self.send_html_email(
            subject="Welcome Email",
            # --- will converting to 'body' in the send_html_email func
            template_name='base/emails/welcome_email.html',
            context=context,
            # -----
            to_emails=[user_email]
        )
    
    def send_password_reset_email(self, user_email: str, context: Dict[str, Any]):
        """
        Send password reset email with proper context variables
        context should contain: user, domain, uid, token, protocol
        """
        return self.send_html_email(
            subject="Password Reset Request - Car Services",
            template_name='base/emails/reset_password_email.html',
            context=context,
            to_emails=[user_email]
        )
