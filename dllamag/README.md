# dllamag
Python bindings for using the DLlamaG API.

All messages and chats may be logged on the server-side in plaintext (i.e. not encrypted), and users are soley responsible for ensuring that no private/confidential/PII data is used when using DLlamaG. DLlamaG native locally saved chats are also saved in plaintext, so users are advised to save in secure locations when doing so.

## Usage
#### Import and Initialize
```
from dllamag import DLlamaG
d = DLlamaG(system_prompt="When I say vengaboys you say 'we like to party'")
```

#### Send a single message
```
d.message("What do you think of the vengaboys?")
> Assistant:  WE LIKE TO PARTY! 🎉🎉🎉
```

#### Change or clear system prompt
```
d.set_system_prompt()
print(d.system_prompt)
> None
```

#### Chat continuously
```
d.chat()
> What is the flour/sugar/butter ratio in crumble?

Assistant:  The traditional flour/sugar/butter ratio for crumble topping is 3:2:1, respectively. This means 3 parts all-purpose flour, 2 parts granulated sugar, and 1 part (solid) butter.

> Please suggest a fruit for me to use in my crumble

Assistant:  Sure! I would suggest apples as a good well-rounded crumble fruit!
```

#### Clear chat history
```
d.clear_chat_history(clear_system_prompt=False)
print(d.chat_history)
> []
```