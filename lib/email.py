import smtplib


def sendemail(to_list, from_addr, subject,
              message, credentials, smtpserver, tls=False):
    header = "From: %s\r\n" % from_addr
    header += "To: %s\r\n" % ",".join(to_list)
    header += "Subject: %s\r\n" % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    if tls:
        server.starttls()
    server.login(credentials[0], credentials[1])
    problems = server.sendmail(from_addr, to_list, message)
    server.quit()
    return problems


if __name__ == "__main__":
    sendemail(
        "chkbot3@gmail.com",
        ["aaronryool@gmail.com"],
        "Error", message,
        "chkbot3@gmail.com", "")
