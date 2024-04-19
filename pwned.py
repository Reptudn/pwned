import bs4
import dotenv
import os
import scheduler
from typing import cast

HIBP_API_KEY = ""
DISCORD_WEBHOOK = ""

def check_password(password):
	# Check if the password has been pwned
	# Returns the number of times the password has been pwned
	# Returns -1 if the password is not pwned
	# Returns -2 if the password is invalid
	if not password:
		return -2
	# Hash the password
 
	headers = {
		"hibp-api-key": HIBP_API_KEY
	}

	hashed_password = hashlib.sha1(password.encode()).hexdigest().upper()
	# Send a request to the pwnedpasswords API
	response = requests.get(f'https://api.pwnedpasswords.com/range/{hashed_password[:5]}', headers=headers)
	# Check if the request was successful
	if response.status_code != 200:
		return -2
	# Parse the response
	soup = bs4.BeautifulSoup(response.text, 'html.parser')
	for line in soup.text.split('\n'):
		if hashed_password[5:] in line:
			return int(line.split(':')[1])
	return -1
if __name__ == '__main__':
	if not os.path.exists('.env'):
		with open('.env', 'a') as f: # create .env file and append
			f.write(f'HIBP_API_KEY="{str(input("Please enter your HIBP API key: "))}"\n')
			f.write(f'DISCORD_WEBHOOK="{str(input("Please enter your Discord webhook URL: "))}"\n')
		
	dotenv.load_dotenv()

	HIBP_API_KEY = cast(str, os.getenv('HIBP_API_KEY')) if os.getenv('HIBP_API_KEY') else ""
	DISCORD_WEBHOOK = cast(str, os.getenv('DISCORD_WEBHOOK')) if os.getenv('DISCORD_WEBHOOK') else ""

	if not HIBP_API_KEY or not DISCORD_WEBHOOK:
		print("Please provide the required environment variables.")
		exit(1)

	scheduler.add_job(check_password, 'interval', seconds=5)
	scheduler.run()

# JUST REALIZED THE API IS NOT FREE 0-0