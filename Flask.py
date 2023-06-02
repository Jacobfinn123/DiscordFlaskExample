import requests
from flask import Flask, render_template, request, redirect, session
from config import REDIRECT_URL, CLIENT_SECRET, TOKEN, OAUTH_CALLBACK, CLIENT_ID

app = Flask(__name__)
app.secret_key = 'somesecretkeyiguess'.encode('utf8')


@app.route('/')
def index():

	# Checks for user access token
	if "token" in session:
		url = "https://discord.com/api/v9/users/@me"
		headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"Authorization": f"Bearer {session.get('token')}"
		}
		user_data = requests.get(url, headers=headers).json()
		user_id = user_data['id']
		user_display_name = f"{user_data['username']}#{user_data['discriminator']}"
		user_avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data['avatar']}"

		class User:
			def __init__(self, user_id, name, avatar):
				self.user_id = user_id
				self.name = name
				self.avatar = avatar

		user = User(user_id, user_display_name, user_avatar_url)
		return render_template("index.html", user=user)

	return render_template("index.html", oauth_url=OAUTH_CALLBACK)


@app.route('/callback/oauth')
def oauth():
	code = request.args['code']
	data = {
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET,
		"grant_type": "authorization_code",
		"redirect_uri": REDIRECT_URL,
		"code": code,
	}
	url = "https://discord.com/api/v9/oauth2/token"
	headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Authorization": f"Bearer {TOKEN}"
	}
	access_token = requests.post(url, data=data, headers=headers).json()['access_token']

	session['token'] = access_token
	return redirect("/")


@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")


if __name__ == "__main__":
	app.run(host="localhost", port=int("5000"), debug=True)
