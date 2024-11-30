import requests

def urljoin(part1:str, part2:str) -> str:
    """Combines two portions into a single URL, being mindful of repeating slashes."""
    if len(part1) == 0:
        return part2
    elif len(part2) == 0:
        return part1
    
    # strip out trailing
    if part1[len(part1) - 1] == "/":
        part1 = part1[:-1]
    
    # strip out leading
    if part2[0] == "/":
        part2 = part2[1:]

    return part1 + "/" + part2

def get_xml_tag(body:str, tag_name:str) -> str:
    """Strips out a value from the body based on the XML tag name it resides in."""
    try:
        i1:int = body.index("<" + tag_name + ">")
        i1:int = body.index(">", i1 + 1)
        i2:int = body.index("<", i1 + 1)
        return body[i1+1:i2]
    except:
        raise Exception("Unable to find XML tag '" + tag_name + "' in provided body.")

class QueueMessage:
    def __init__(self):
        self._id:str = None
        self._pop:str = None
        self._txt:str = None

    @property
    def MessageId(self) -> str:
        return self._id
    
    @MessageId.setter
    def MessageId(self, value) -> None:
        self._id = value

    @property
    def PopReceipt(self) -> str:
        return self._pop
    
    @PopReceipt.setter
    def PopReceipt(self, value) -> None:
        self._pop = value

    @property
    def MessageText(self) -> str:
        return self._txt
    
    @MessageText.setter
    def MessageText(self, value) -> None:
        self._txt = value

    def __repr__(self):
        return str({"MessageId": self.MessageId, "PopReceipt": self.PopReceipt, "MessageText": self.MessageText})


class QueueService:
    """Brokers communication with the Azure Queue REST API"""

    def __init__(self, queue_url:str, sas_token:str):
        """
        Creates a new instance of the QueueService class, ready to communicate with a specific queue within a specific Azure Storage Account.
        
        Parameters:
        queue_url (str): The URL directly to the Azure Storage Queue, i.e. "https://mystorageaccount.queue.core.windows.net/myqueue"
        sas_token (str): The Shared Access Signature (SAS) you get when generating in the Azure Portal. i.e. "sv=2022-11-02&ss=bfqt&srt=c&sp=rwdlacupiytfx&se=2024-11-30T19:34:10Z&st=2024-11-30T11:34:10Z&spr=https&sig=%2FKxtw%2FTzD0lXqj2kGyMuJ9Y0cFb16javsQb7Pz4b6KM%3D"
        """

        # ensure the URL has an actual queue name in it
        if "/" not in queue_url.lower().replace("https://", "").replace("http://", "") or queue_url[len(queue_url) - 1] == "/":
            raise Exception("You did not provide the URL to a specific Queue in the URL you provided. Ensure the URL you are providing is not only to a specific storage account, but also to a specific queue (i.e. '/myqueue' at the end)!")


        self._url = queue_url
        self._token = sas_token

    def put(self, text:str) -> None:
        """Adds a new message to the queue."""
        
        # construct body
        body:str = "<QueueMessage><MessageText>" + text + "</MessageText></QueueMessage>"

        # Make POST request
        post_url:str = urljoin(self._url, "messages") + "?" + self._token
        headers = {"Content-Type": "application/xml"}
        response = requests.post(post_url, headers=headers, data=body)
        
        # handle code?
        if response.status_code != 201:
            raise Exception("POST request to Azure Queue Service to upload message returned status code '" + str(response.status_code) + "', not the successful '201 CREATED'!")
        
    def receive(self) -> QueueMessage:
        """Receives the next message from the queue, but does NOT delete it."""

        # make get request
        get_url:str = urljoin(self._url, "messages") + "?" + self._token
        response = requests.get(get_url)
        response_body:str = response.text

        # handle error
        if response.status_code != 200:
            raise Exception("GET request to receive queue message returned status code " + str(response.status_code) + "! Body: " + response_body)

        # if there was no queue messages left
        if "<QueueMessagesList />" in response_body: # an empty list
            return None
        
        # get data from response body
        ToReturn:QueueMessage = QueueMessage()
        ToReturn.MessageId = get_xml_tag(response_body, "MessageId")
        ToReturn.PopReceipt = get_xml_tag(response_body, "PopReceipt")
        ToReturn.MessageText = get_xml_tag(response_body, "MessageText")
        return ToReturn
    
    def delete(self, message_id:str, pop_receipt:str) -> None:
        """Deletes a message from the queue."""

        # make DELETE request
        delete_url:str = urljoin(urljoin(self._url, "messages"), message_id) + "?popreceipt=" + pop_receipt + "&" + self._token
        response = requests.delete(delete_url)

        # handle error
        if response.status_code != 204: # when successful, it returns 204 NO CONTENT
            response_body:str = response.text
            raise Exception("Deletion of message '" + message_id + "' was unsuccessful! Status code '" + str(response.status_code) + "' was returned. Body: " + response_body)

    def clear(self) -> None:
        """Clears the queue of all messages"""

        # make DELETE request
        delete_url:str = urljoin(self._url, "messages")
        response = requests.delete(delete_url)

        # handle error
        if response.status_code != 204: # when successful, it returns 204 NO CONTENT
            response_body:str = response.text
            raise Exception("Clearing of queue was unsuccessful! Status code '" + str(response.status_code) + "' was returned. Body: " + response_body)

