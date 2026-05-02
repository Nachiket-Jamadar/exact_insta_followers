from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)


def get_follower_count(username):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode

    # Mobile phone simulation
    mobile_emulation = {
        "deviceName": "iPhone 12 Pro"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(options=options)
    url = f"https://www.instagram.com/{username}"
    driver.get(url)
    # Wait for the followers element to be present
    wait = WebDriverWait(driver, 10)
    followers_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'followers')]/span")))
    followers_value = followers_element.get_attribute('title')
    driver.quit()  # Close the browser
    return followers_value


@app.route('/followers', methods=['GET'])
def get_followers():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Username parameter is required'}), 400

    try:
        followers_count = get_follower_count(username)
        return jsonify({'username': username, 'followers': followers_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
