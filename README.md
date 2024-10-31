# amqp_sender
desktop application for send amqp message



For getting crypto key do this
```
from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Your key: {key}")
```


```
pyinstaller --onefile --windowed main.py 
```

```
 pyside6-uic amqpSender.ui -o ui_amqpSender.py
```