
# Amy

**Amy** is a quirky and semi-useful IRC bot designed to spice up your IRC experience. Whether you're commanding her to execute tasks, show off ASCII art, or just cause a bit of friendly chaos, Amy is always happy to help (or at least entertain).

---

## Features

- **Dynamic Commands**: Amy supports a variety of text-based commands for moderators and users.
- **Moderation Tools**: Designed to help mods manage their channels effectively.
- **ASCII Art Performances**: Amy adds personality to interactions with expressive ASCII art.
- **Authentication System**: Grants special privileges to authorized users, managed via `config.json`.

---

## Commands

Amy comes with the following command set:

| Command Pattern                | Description                                                                                   |
|--------------------------------|-----------------------------------------------------------------------------------------------|
| `$reload`                      | Reloads the bot (mods only).                                                                  |
| `$join <channel>`              | Joins a specified channel (mods only).                                                       |
| `$nick <new_name>`             | Changes the bot's nickname (mods only).                                                      |
| `$op <user>`                   | Grants operator privileges to a specified user (mods only, channel use only).                |
| `$auth <username> <password>`  | Authenticates a user with their credentials (must be sent in a private message to Amy).    |
| `(^d\|.* d)o(o+)m.*`            | Responds with a dramatic ASCII art sequence of "DOOM!"                                       |
| `fuck <something>`             | Expresses strong disapproval with an ASCII art sequence and the given input.                 |

---

### Detailed Command Descriptions

#### `$reload`
- **What it does**: Disconnects and reloads Amy.
- **Who can use it**: Mods with "o" (operator) privileges.
- **Behavior**: If unauthorized, Amy humorously refuses the command and kicks the user out of the channel.

#### `$join <channel>`
- **What it does**: Makes Amy join a specified IRC channel.
- **Who can use it**: Mods with "h" (half-op) or higher privileges.
- **Behavior**: Unauthorized attempts result in playful ASCII art and a kick.

#### `$nick <new_name>`
- **What it does**: Changes Amy's nickname.
- **Who can use it**: Mods with "o" (operator) privileges.
- **Behavior**: Unauthorized users receive a loud, humorous refusal.

#### `$op <user>`
- **What it does**: Grants operator status to a specified user in the current channel.
- **Who can use it**: Mods with "o" (operator) privileges.
- **Behavior**: Only works in a channel; otherwise, Amy gently reminds the user.

#### `$auth <username> <password>`
- **What it does**: Authenticates a user with their username and password.
- **Who can use it**: Any user, but it must be sent via private message.
- **Behavior**: Public use of this command triggers a stern warning about password security.

#### `(^d|.* d)o(o+)m.*`
- **What it does**: Triggers an ASCII art sequence representing DOOM in its most glorious form.
- **Who can use it**: Anyone.
- **Behavior**: Amy sends a dramatic series of ASCII lines to the channel with timed delays.

#### `fuck <something>`
- **What it does**: Outputs an ASCII sequence expressing strong feelings about the input.
- **Who can use it**: Anyone.
- **Behavior**: The sequence includes the text provided by the user, shouting it loudly for all to see.

---

## Configuration

Amy is configured via a JSON file, `config.json`. Here’s a sample:

```json
{
    "irc.hackermeme.net": {
        "channels": ["#cmd", "#design", "#hackermeme", "#music"],
        "prefix": "amy!amy@localhost",
        "sslflag": false,
        "port": 6667,
        "mods": {
            "heather": ["o", "<PASSWORD-HASH>"],
            "epoch": ["o", "<PASSWORD-HASH>"],
            "alice": ["o", "<PASSWORD-HASH>"],
            "bunny": ["o", "<PASSWORD-HASH>"],
            "uniquelyelite": ["h", "<PASSWORD-HASH>"]
        }
    }
}
```

### Configuration Notes
- **Server Settings**: Define the IRC server, channels, and connection options.
- **Moderators**: Use hashed passwords to manage access levels:
  - `"o"`: Operator privileges.
  - `"h"`: Half-op privileges.

---

**Amy**: 🤗 Polite. 🤓 Quirky. 🌟 Useful... sometimes.