import sys
import time
import json
import cloudscraper
from bs4 import BeautifulSoup

class N11Crawler:
    __DEFAULT_FILENAME = "comments"
    __FILENAME = "comments"

    __run_executed = False

    __comments_list = []
    __page_count = 0
    __time_taken = "0"

    __scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "android",
            "desktop": False
        },
        disableCloudflareV1=True,
    )

    def __init__(self, product_id: str, save_as_json: bool = False, max_comments: int = 1000, progress_bar: bool = False):
        """
        n11.com comment crawler.

        product_id : str
                    Product id from product page. If you don't know how to find this id go to README.md.
        save_as_json : bool
                    Auto save to json file. (default is False)
        max_comments : int
                    Maximum number of comments. (default is 1000)
        progress_bar : bool
                    Show progress bar. (default is False)
        """
        assert isinstance(product_id, str), "product_id must be a non-empty string."
        assert isinstance(save_as_json, bool), "save_as_json must be a boolean."
        assert isinstance(max_comments, int), "max_comments must be a integer."
        assert isinstance(progress_bar, bool), "progress_bar must be a boolean."
        self.__product_id = str(product_id)
        self.__save_as_json = save_as_json
        self.__max_comments = max_comments
        self.__progress_bar = progress_bar

    def __progress(self, count: int, total: int, status: str = ""):
        """
        Show progress bar.

        count : int
                    Current page.
        total : int
                    Total number of page.
        status : str
                    Status updates. (default is empty)
        """
        if self.__progress_bar == False: return
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = "=" * filled_len + "-" * (bar_len - filled_len)

        sys.stdout.write("[%s] %s%s %s\r" % (bar, percents, "%", status))
        sys.stdout.flush()

    def __clear(self, text: str):
        """
        Remove spaces and line breaks from text.

        text : str
                    Text to clear.
        """
        return " ".join(text.split())

    def __save_json(self):
        """
        Save as json file.
        """
        with open(self.__FILENAME + ".json", "w", encoding="utf-8") as file:
            json.dump(self.__comments_list, file, ensure_ascii=False)

    def __get_page_count(self):
        """
        Get product number of page count.
        """
        try:
            html = self.__scraper.get("https://www.n11.com/component/render/groupProductReviews?page=1&productId=" + self.__product_id).text
        except:
            raise Exception("Product not found or you were blocked from the server.")

        soup = BeautifulSoup(html, "html.parser")

        try:
            page_count = int(soup.find("span", attrs={"class": "pageCount"}).text)
        except:
            try:
                no_comment = soup.find("p", attrs={"class": "unf-empty-text"}).text
                if no_comment != "":
                    page_count = 0
            except:
                page_count = 1

            # raise Exception("Product not found or you were blocked from the server.")

        self.__page_count = page_count

    def run(self):
        """
        Start fetching all comments page by page.
        """
        tic = time.perf_counter()
        self.__get_page_count()
        for x in range(1, self.__page_count + 1):
            self.__progress(x, self.__page_count + 1, "Fetching")
            try:
                html = self.__scraper.get("https://www.n11.com/component/render/groupProductReviews?page=" + str(x) + "&productId=" + self.__product_id).text
            except:
                raise Exception("Product not found or you were blocked from the server.")

            soup = BeautifulSoup(html, "html.parser")

            comments = soup.find_all("li", attrs={"class": "comment"})

            for comment in comments:
                try:
                    data_review_id = comment["data-reviewid"]
                    rating = str(comment.find("div", attrs={"class": "ratingCont"}).find("span")["class"][1])
                    rating = rating.replace("r", "")
                    date = comment.find("span", attrs={"class": "commentDate"}).text

                    try:
                        title = comment.find("h5", attrs={"class": "commentTitle"}).text
                    except:
                        title = "none"

                    try:
                        message = comment.find("p").text
                    except:
                        message = "none"

                    user_name = comment.find("span", attrs={"class": "userName"}).text
                    seller = comment.find("span", attrs={"class": "sellerNickname"}).find("b").text

                    comment_obj = {
                        "data_review_id": self.__clear(data_review_id),
                        "rating": self.__clear(rating),
                        "date": self.__clear(date),
                        "title": title,
                        "message": self.__clear(message),
                        "user_name": self.__clear(user_name),
                        "seller": self.__clear(seller)
                    }

                    if len(self.__comments_list) >= self.__max_comments:
                        break
                    else:
                        self.__comments_list.append(comment_obj)

                except:
                    raise

            if len(self.__comments_list) >= self.__max_comments:
                break

        if self.__save_as_json:
            self.__save_json()

        self.__run_executed = True
        toc = time.perf_counter()
        self.__time_taken = f"{toc - tic:0.4f}"

    def get_comments(self):
        """
        Get fetched comments as array.
        """
        assert self.__run_executed, "This function must be call after run() function."
        return self.__comments_list

    def get_page_count(self):
        """
        Get number of page count
        """
        assert self.__run_executed, "This function must be call after run() function."
        return self.__page_count

    def get_fetch_time(self):
        """
        Get how long it takes run() function execute
        """
        assert self.__run_executed, "This function must be call after run() function."
        return self.__time_taken

    def get_comments_length(self):
        """
        Get length of fetched comments
        """
        assert self.__run_executed, "This function must be call after run() function."
        return len(self.__comments_list)

    def save_as_json(self, filename: str = __DEFAULT_FILENAME):
        """
        Save comments as json file.

        filename : str
                    Filename of json file.
        """
        assert self.__run_executed, "This function must be call after run() function."
        assert isinstance(filename, str), "filename must be a non-empty string."
        self.__FILENAME = filename
        self.__save_json()
        return True