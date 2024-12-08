# Amy

**Amy** is a quirky and semi-useful IRC bot designed to spice up your IRC experience. Whether you're commanding her to execute tasks, show off ASCII art, or just cause a bit of friendly chaos, Amy is always happy to help (or at least entertain).

---

## Features

- **Dynamic Commands**: Amy supports a variety of text-based commands for moderators and users.
- **Moderation Tools**: Designed to help mods manage their channels effectively.
- **ASCII Art Performances**: Amy adds personality to interactions with expressive ASCII art.
- **Authentication System**: Grants special privileges to authorized users, managed via `config.json`.
- **Information Collection**: Amy can identify and process patterns like URLs, emails, card numbers, and more for moderation or analysis.

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

## Information Collection

Amy includes a comprehensive set of tools to collect and process information from text. These capabilities are designed for moderation, filtering, and enriching the user experience. Here’s an overview of what Amy can collect and how it processes data:

### Information Types

| Type                     | Description                                                                                   |
|--------------------------|-----------------------------------------------------------------------------------------------|
| **Card Information**     | Detects and processes card details like number, type, and status.                             |
| **Darknet Links**         | Identifies `.onion` addresses commonly used on the dark web.                                  |
| **Pastebin Links**        | Extracts raw content from supported pastebin-like services.                                   |
| **Contact Information**   | Recognizes email addresses and other contact details.                                        |
| **Web Links**             | Detects URLs, IP addresses, and specific services like YouTube.                              |

### How It Works

1. **Pattern Matching**: 
   Amy uses a set of regular expressions to identify specific patterns in text, such as:
   - Credit card numbers (`\b[0-9]{16}\b`)
   - Email addresses (`[A-Z0-9_.+-]+@[A-Z0-9-]+\.[A-Z0-9-.]+`)
   - URLs (`(?:http|ftp|git|irc)s?://...`)
   - Darknet `.onion` addresses.

2. **Data Processing**: 
   Detected information is passed through corresponding handlers, which can:
   - Validate the data (e.g., Luhn's algorithm for card numbers).
   - Fetch additional metadata (e.g., using YouTube’s oEmbed API).
   - Retrieve and screen content (e.g., from Pastebin).

3. **Queue System**:
   Amy uses a multi-threaded queue to handle data processing efficiently in real-time.

4. **JSON Integration**:
   Processed information is structured into JSON format for easy handling and potential logging.

### Example Configurations

Sample regular expressions and handlers are defined in `handlers`:

```python
self.card_handlers = {
    r"\b[0-9]{16}\b": self.ccn_handler,
    r"\b(DEBIT|CREDIT)\b": lambda x: {"card_account": [y.lower() for y in x]},
    ...
}
```

---

## Configuration

Amy is configured via a JSON file, `config.json`. See the earlier sections for a sample configuration file.

---

## Running Amy

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Amy.git
   cd Amy
   ```

2. Configure the bot:
   - Copy and edit the sample configuration:
     ```bash
     cp config.sample.json config.json
     nano config.json
     ```

3. Run the bot:
   ```bash
   python Amy.py
   ```

---

## Contributing

Want to add new features or commands? Feel free to fork the repo, make changes, and submit a pull request. Amy is always open to new ideas!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Amy**: 🤗 Polite. 🤓 Quirky. 🌟 Useful... sometimes.