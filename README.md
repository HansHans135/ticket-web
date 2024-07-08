# ticket-web
Discord Bot的線上ticket解決方案

# 說明
現今Disocrd上有許多機器人有客服單紀錄系統，但卻無法線上觀看，必須將檔案下載下來。此系統主要解決html託管問題

# 使用
上傳位置 https://ticket.hans0805.me/upload

以requests為例(檔名請使用html_log)
```py
import requests
r=requests.post("https://ticket.hans0805.me/upload",data={"token":"Discord機器人token"},files={'html_log': open('ticket.html','rb')})
print(r.text)
```

# 限制
每個機器人每日只能上傳100個檔案，如有需要請Discord聯絡 08.hans_

**此專案不會儲存你的機器人權杖，僅作為身分驗證**
