def download_videos(url):
    ''' Download videos from fbvideodown using URLs'''
    driver=webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get("https://fdown.net/index.php")
    time.sleep(5)
    try:
        consent_button = driver.find_element(By.XPATH, "//button[@class='fc-button fc-cta-consent fc-primary-button']")
        consent_button.click()
    except:
        pass
    time.sleep(2)
    try:
        input_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@class='form-control input-lg']")))
        input_box.clear()
        input_box.send_keys(url)
        download_button = driver.find_element(By.XPATH,"//button[@class='btn btn-primary input-lg']")
        time.sleep(3)
        download_button.click()
        time.sleep(5)
        try:
            video = driver.find_element(By.XPATH,"//a[@id='hdlink']")
            src = video.get_attribute('href')
        except:
            video = driver.find_element(By.XPATH, "//a[@id='sdlink']")
            src = video.get_attribute('href')
        return src
    except:
        src = ""
        return src