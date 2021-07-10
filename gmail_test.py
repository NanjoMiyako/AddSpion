import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

import sys

def loadMailGroupInfo(path):

    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
        
        MailGroupId = l_strip[0].split(',')[1]
        MailTypeId = l_strip[1].split(',')[1]
        MailTypeName = l_strip[2].split(',')[1]
        SenderAddress = l_strip[3].split(',')[1]
        
        ToAddress = l_strip[4].split(',')
        ToAddress.pop(0)
        
        MailAppPassWord = l_strip[5].split(',')[1]
        
        return MailGroupId,MailTypeId,MailTypeName,SenderAddress,ToAddress,MailAppPassWord


def makeBodyText(comment, MailTypeName, expirationDate):

    string1 = "メールタイプ:" + MailTypeName +"\r\n"
    string1 += "データ有効期限:" + expirationDate + "日間\r\n"
    
    count1 = 1;
    for path1 in ShareFilePathList:
        string1 += "共有データパス"+ str(count1) + ":" + path1 + "\r\n"
        count1 = count1 + 1
    
    
    string1 += "コメント:" + comment + "\r\n"
    
    return string1


print("---AddSpion---")
while True:
    MailGroupFilePath = input("メールグループファイルURLを入力:")
    print("グループファイルパス:", MailGroupFilePath)
    
    string2 = input("-1を入力で決定:")
    if string2 == '-1':
        break

while True:
    titleLabel = input("メールタイトルラベルを入力:")
    print("タイトルラベル:", titleLabel)
    
    string2 = input("-1を入力で決定:")
    if string2 == '-1':
        break

ShareFilePathList = []        
while True:
    while True:
        ShareFilePath = input("共有ファイルデータURLを入力:")
        print("パス:", ShareFilePath)
        
        string2 = input("-1を入力で決定:")
        if string2 == '-1':
            ShareFilePathList.append(ShareFilePath)
            break
            
    string3 = input("共有ファイルデータURLの入力を続けますか(y/n):")
    if string3 != 'y':
            break
            
while True:
    expirationDate = input("共有ファイルデータURLの有効期限を入力:")
    print("有効期限:", expirationDate, "日間")
    
    string2 = input("-1を入力で決定:")
    if string2 == '-1':
        break

while True:
    comment = input("コメントを入力:")
    
    string2 = input("-1を入力で決定:")
    if string2 == '-1':
        break            

MailGroupId, MailTypeId, MailTypeName, SenderAddress, ToAddressList, MailAppPassWord = loadMailGroupInfo(MailGroupFilePath)

# メール作成
bodyText = makeBodyText(comment, MailTypeName, expirationDate)

print("以下の内容でメールを送ります:")
print("メールグループID:", MailGroupId)
print("メールタイプID:", MailTypeId)
print("送信元アドレス:", SenderAddress)
print("送信先アドレス:", ToAddressList)
print("コメント:",comment)

string3 = input("以上の内容でメールを送信しますか(y/n):")
if string3 != 'y':
        print("送信をキャンセルしました")
        sys.exit()

subject = "AddSpion-MailGroup-" + MailGroupId + "-MailType-" + MailTypeId + "-Label-" + titleLabel

# SMTPサーバに接続
smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
smtpobj.starttls()
smtpobj.login(SenderAddress, MailAppPassWord)



for toAddress in ToAddressList:
    # 作成したメールを送信
    msg = MIMEText(bodyText)
    msg['Subject'] = subject
    msg['From'] = SenderAddress
    msg['Date'] = formatdate()
    msg['To'] = toAddress
    smtpobj.send_message(msg)

print("メール送信しました")

smtpobj.close()



