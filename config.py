from urllib import parse

TOKEN = ""  # Bot token
CLIENT_ID = ""  # Bot oauth client ID
CLIENT_SECRET = ""  # Bot oauth secret token
REDIRECT_URL = "http://localhost:5000/callback/oauth"  # URL where callback is handled
OAUTH_CALLBACK = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={parse.quote(REDIRECT_URL)}&response_type=code&scope=identify%20guilds%20email"  # Discord OAUTH Url
