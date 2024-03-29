all_reviews = []

for i in num['고유번호']:
    contents = []

    # url
    url = 'https://m.place.naver.com/restaurant/' + str(i) + '/review/visitor'

    # Webdriver headless mode setting
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # BS4 setting for secondary access
    session = requests.Session()
    headers = {
        "User-Agent": "user value"}

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))


    # Start crawling/scraping!
    try:
        service = webdriver.ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        res = driver.get(url)
        driver.implicitly_wait(30)

        # Pagedown
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        try:
            while True:
                driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[2]/div/a').click()
                time.sleep(0.4)
        except Exception as e:
            print('finish')

        time.sleep(25)
        html = driver.page_source
        bs = BeautifulSoup(html, 'lxml')
        reviews = bs.select('li.YeINN')

        for r in reviews:
            content = r.select_one('div.ZZ4OK.IwhtZ')

            # exception handling
            content = content.text if content else ''
            contents.append(content)
            time.sleep(0.06)
        
        all_reviews.append(contents)


    except Exception as e:
        print(e)

# 파일 저장
res = pd.DataFrame({'리뷰' : all_reviews})
res_tot = pd.concat([name, num, res], axis=1)
res_tot.to_csv("data_all_tot_01260247.csv", encoding='utf-8-sig')
