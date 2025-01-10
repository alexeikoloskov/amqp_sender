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



```
python PyInstaller --onefile --icon=amqp_sender_icon.ico --add-data "amqp_sender_icon.ico;." --name "AMQPSender" --splash "splash.png" --windowed main.py
```