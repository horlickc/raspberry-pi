import email
import imaplib

username = "tobychan98.w@gmail.com"
password = "ZwFMwNTeehyL9aGR"

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

mail.select("inbox")
# result, data = mail.uid("search", None, "ALL")

(retcode, messages) = mail.search(None, "(UNSEEN)")

list = messages[0].split()
len(list)

print(messages)


