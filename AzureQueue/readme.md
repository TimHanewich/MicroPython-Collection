# AzureQueue
A simple and lightweight library for communicating with an Azure Queue, allowing you to read messages, put (create) messages, delete messages, and clear the queue.

*Full disclosure, I wrote this in Python and have not tested in MicroPython, but I'm quite certain everything here will run in MicroPython.*

## Example Usage
```
import AzureQueue

queue_url = "https://mystorageaccount.queue.core.windows.net/myqueue" # replace "mystorageaccount" with your storage account and "myqueue" with the name of your queue
sas_token = "sv=2022-11-02&ss=q&srt=sco&sp=rwdlacup&se=2025-11-29T22:05:13Z&st=2024-11-29T14:05:13Z&spr=https,http&sig=p%2FLf7zuVDLTGCwhg88%2FcCdu0jdnuZqznxLmtfIFf%2FZ0%3D" # get this SAS token when you create your SAS in the Azure Portal!
qs = AzureQueue.QueueService(queue_url, sas_token)

# clear the queue
qs.clear()

# put (create) a new message
qs.put("Hello, world! This is my new queue message!")

# receive (read) the next message in the queue
msg:AzureQueue.QueueMessage = qs.receive()
if msg == None:
    print("No message available.")
else:
    print(str(msg))
    qs.delete(msg.MessageId, msg.PopReceipt) # after reading the message, be sure to delete the message! Otherwise it will be added back to the queue after a short period of time (the "visibility timeout" of the message)
```

## Documentation Followed
Microsoft provides excellent documentation on the Azure Queue REST API:
- [Put message](https://learn.microsoft.com/en-us/rest/api/storageservices/put-message)
- [Get message](https://learn.microsoft.com/en-us/rest/api/storageservices/get-messages)
- [Delete message](https://learn.microsoft.com/en-us/rest/api/storageservices/delete-message2)
- [Clear queue](https://learn.microsoft.com/en-us/rest/api/storageservices/clear-messages)