# coding = utf-8
from selenium import webdriver
from urllib import parse
from time import sleep


class GetBibs:
    def __init__(self, driver_path, option_path, ieee_search_url, google_search_url) -> None:
        self.ieee_search_url = ieee_search_url
        self.google_search_url = google_search_url
        # Open Chrome
        option = webdriver.ChromeOptions()
        option.add_argument("--user-data-dir=" + option_path)
        self.browser = webdriver.Chrome(
            executable_path=driver_path, options=option
        )
        # Browser size: Don't change it!
        self.browser.set_window_size(800, 800)

    def get_bib_from_IEEE(self, paper_title):
        strto_pn = parse.quote(paper_title)
        url = self.ieee_search_url + strto_pn
        self.browser.get(url)
        compare_title = "".join(list(filter(str.isalnum, paper_title))).lower()
        # Loading
        for i in range(100):
            try:
                elements = self.browser.find_elements_by_css_selector(
                    "[class='List-results-items']"
                )
                elements[0].get_attribute("id")
                break
            except:
                sleep(0.1)
        # Scaning
        paper_url = r"https://ieeexplore.ieee.org/document/"
        for i in elements:
            s_title = i.text.split("\n")[0]
            s_title = "".join(list(filter(str.isalnum, s_title))).lower()
            if s_title == compare_title:
                paper_url += i.get_attribute("id")
                break
        if paper_url == r"https://ieeexplore.ieee.org/document/":  # 没找到
            return ""
        # Go to Detail Page
        self.browser.get(paper_url)
        # Waiting for `bib` button
        for i in range(100):
            try:
                element = self.browser.find_element_by_css_selector(
                    "[class='layout-btn-white cite-this-btn']"
                )
                element.click()
                break
            except:
                sleep(0.1)
        # Click `bibtex`
        for i in range(100):
            try:
                element = self.browser.find_element_by_css_selector(
                    "[class='modal-dialog']"
                )
                element = element.find_elements_by_css_selector(
                    "[class='document-tab-link']"
                )[1]
                element.click()
                break
            except:
                sleep(0.1)
        for i in range(100):
            try:
                self.browser.find_element_by_css_selector("[class='text ris-text']")
                break
            except:
                sleep(0.1)
        sleep(2)
        bib = self.browser.find_element_by_css_selector("[class='text ris-text']").text
        return bib

    def get_bib_from_google_scholar(self, paper_title):
        strto_pn = parse.quote(paper_title)
        url = self.google_search_url + strto_pn
        self.browser.get(url)
        # Loading data
        for i in range(100):
            try:
                element = self.browser.find_element_by_css_selector(
                    "[class='gs_r gs_or gs_scl']"
                )
                element = element.find_element_by_css_selector("[class='gs_fl']")
                element = element.find_element_by_css_selector(
                    "[class='gs_or_cit gs_nph']"
                )
                element.click()
                break
            except:
                sleep(0.1)
        for i in range(100):
            try:
                element = self.browser.find_element_by_id("gs_citi")
                element = element.find_element_by_css_selector("[class='gs_citi']")
                element.click()
                break
            except:
                sleep(0.1)
        for i in range(100):
            try:
                bib = self.browser.find_element_by_tag_name("pre").text
                break
            except:
                sleep(0.1)
        return bib

    def get_bib(self, paper_title):
        bib = self.get_bib_from_IEEE(paper_title)
        if bib != "":
            return "IEEE", bib
        return "Google", self.get_bib_from_google_scholar(paper_title)

if __name__ == "__main__":
    # The path of Chrome driver
    driver_path = r"D:\software\Tools\chromedriver.exe"
    # The data path of Chrome
    option_path = r"C:\Users\Lustre\AppData\Local\Google\Chrome\User Data"
    # IEEE Search Page
    ieee_search_url = r"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText="
    # Google Scholar Search Page
    google_search_url = r"https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&inst=1597255436240989024&q="
    
    # Init
    get_bibs = GetBibs(driver_path, option_path, ieee_search_url, google_search_url)
    
    # The paper list
    paper_list = [
        "Low-cost and area-efficient FPGA implementations of lattice-based cryptography",
        "High-speed polynomial multiplication architecture for ring-LWE and SHE cryptosystems",
    ]

    # Search
    with open("res.bib", "w", encoding="utf-8") as f:
        for paper in paper_list:
            source, bib = get_bibs.get_bib(paper)
            print_str = "\n% From {}: {}\n".format(source, paper)
            print(print_str)
            f.write(print_str)
            f.write(bib)            
