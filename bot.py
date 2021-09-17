from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import info

# make sure this path is correct
DRIVER_PATH = "/Users/josh/Developer/chromedriver"

driver = webdriver.Chrome(DRIVER_PATH)

RTX3080LINK1 = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
TEST = 'https://www.bestbuy.com/site/zagg-invisibleshield-glass-elite-maximum-impact-scratch-screen-protector-for-apple-iphone-12-12-pro/6422780.p?skuId=6422780'

driver.get(RTX3080LINK1)

isComplete = False

refresh_count = 0

while not isComplete:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
        refresh_count += 1
        driver.refresh()
        print('Retrying. Refresh # ', refresh_count)
        continue

    print("Add to cart button found")

    try:
        # add to cart
        atcBtn.click()
        print("Added to cart")
        # go to cart and begin checkout as guest
        driver.get("https://www.bestbuy.com/cart")
        print("Moved to cart")

        checkoutBtn = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cartApp"]/div[2]/div[1]/div/div[1]/div[1]/section[2]/div/div/div[4]/div/div[1]/button'))
        )
        
        print("Found checkout button")
        checkoutBtn.click()
        print("Successfully added to cart - beginning check out")

        # fill in email and password
        emailField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fld-e"))
        )
        emailField.send_keys(info.email)

        pwField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fld-p1"))
        )
        pwField.send_keys(info.password)

        # click sign in button
        signInBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/div[3]/button"))
        )
        signInBtn.click()
        print("Signing in")

        # fill in card cvv
        print("Finding CVV box")
        cvvField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#cvv'))
        )
        print("Found CVV attempting to fill")
        cvvField.send_keys(info.cvv)

        print("Looking for button")
        # place order
        placeOrderBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#checkoutApp > div.page-spinner.page-spinner--out > div:nth-child(1) > div.checkout.large-view.fast-track > main > div.checkout__container.checkout__container-fast-track > div.checkout__col.checkout__col--primary > div > div.checkout-panel.contact-card > div.contact-card__order-button > div > div.payment__order-summary > button'))
        )
        print('Found place order button')
        placeOrderBtn.click()

        isComplete = True
    except Exception as e:
        # make sure this link is the same as the link passed to driver.get() before looping
        driver.get(RTX3080LINK1)
        print("Error - restarting bot. Error message:", e)
        continue

print("Order successfully placed!!!!!")



