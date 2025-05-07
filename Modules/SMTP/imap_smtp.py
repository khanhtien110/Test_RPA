from RPA.Email.ImapSmtp import ImapSmtp, AttachmentPosition


class ImapSMTP:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create it
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_data, rpa_tracker):
        if not hasattr(self, "initialized"):
            self.initialized = True  # Mark the object as initialized
            self.rpa_tracker = rpa_tracker
            self.data = config_data
            self.email_account = config_data["email_account"]
            self.email_password = config_data["email_password"]
            self.mail_server = None
            self.default_body = config_data["default_body"]

            self.is_authorize = False

            self.create_mail_server(
                config_data["smtp_server"], config_data["smtp_port"]
            )

            self.authorize_email(self.email_account, self.email_password)

    def create_mail_server(self, server, port):
        self.mail_server = ImapSmtp(
            smtp_server=server,
            smtp_port=port,
        )

    def set_credential(self, email_account, email_password):
        self.email_account = email_account
        self.email_password = email_password
        self.is_authorize = False

    def authorize_email(self, email_account, email_password):
        if self.mail_server != None and self.is_authorize == False:
            self.mail_server.authorize_smtp(
                account=email_account, password=email_password
            )
            self.is_authorize = True

    def send_message(
        self,
        recipients,
        subject,
        attachments=None,
        body=None,
        cc=None,
        bcc=None,
        is_html=False,
    ):
        res = False
        if self.is_authorize == True:
            res = True
            if body is None or body.strip() == "":
                body = self.default_body
            self.mail_server.send_message(
                sender=self.email_account,
                recipients=recipients,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                attachments=attachments,
                attachment_position=AttachmentPosition.TOP,
                html=is_html,
            )
        else:
            self.authorize_email(self.email_account, self.email_password)

        return res
