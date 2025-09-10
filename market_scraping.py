# MGM MARKET
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import regex as re
import csv
from selenium.webdriver.common.by import By
from lxml import html
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
from pop_up_continue import WindowContinue
from info_window import WindowInfo


class ScrapingMarket:
    def __init__(self, main_driver, file_output_name):
        self.main_driver = main_driver
        self.file_output_name = file_output_name
        self.config = self.read_json("./variables.json")
        self.window_continue = WindowContinue()
        self.window_info = WindowInfo()
        self.accept = self.window_info.get_result()
        if self.accept == True:
            print(f"Scraping category into “{result}”…")
            self.get_data()

    def read_json(self, variables_file):
        with open(variables_file, "r") as file:
            config = json.load(file)
        return config

    def continue_scrapping(self):
        result = self.window_continue.get_result()
        if result is None:
            print("Extraction finished.")
        else:
            print(f"Scraping next category into “{result}”…")
            self.file_output_name = result
            self.get_data()

    def get_data(self):
        last_page = False
        first_time = True
        user_level_match = None
        user_trust_level = None
        join_date_user = None
        total_sales_product = None
        payment_type = None
        product_type_text = None
        product = None
        matches = None
        matches_user = None
        place_text = None
        price_match = None
        transactions = None

        next_page_to_process = 2
        while True:
            old_text = self.main_driver.find_element(
                By.XPATH,
                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/table/tbody/tr/td[2]/a[1]",
            ).text
            path_expression = self.main_driver.find_element(
                By.XPATH, "/html/body/div/div[1]/div/div/div[3]/div"
            )
            childs_elements = path_expression.find_elements(
                By.CSS_SELECTOR, "div.table-responsive.roundedlisting"
            )
            first_scrapping = True
            for row in childs_elements:
                matches = row.find_element(By.XPATH, "./table/tbody/tr/td[2]/a[1]").text
                print(matches)
                matches_user = row.find_element(
                    By.XPATH, "./table/tbody/tr/td[2]/a[3]"
                ).text
                price_match = row.find_element(By.XPATH, "./table/tbody/tr/td[5]").text
                price_match = re.search(
                    r"Price per pcs\s*:\s*([0-9]+\.[0-9]+\s*USD)", price_match
                )
                if price_match:
                    price_match = price_match.group(1)
                transactions = row.find_element(By.XPATH, "./table/tbody/tr/td[2]").text
                transactions = re.search(r"\((\d+)\)", transactions)
                if transactions:
                    transactions = transactions.group(1)

                if matches not in self.config["text"]["all"]:
                    button = row.find_element(
                        By.XPATH, f"./table/tbody/tr/td[5]/a"
                    )  # "ORDER" button
                    self.main_driver.execute_script(
                        "arguments[0].scrollIntoView();", button
                    )
                    ActionChains(self.main_driver).key_down(Keys.CONTROL).click(
                        button
                    ).key_up(Keys.CONTROL).perform()
                    windows = self.main_driver.window_handles
                    self.main_driver.switch_to.window(windows[-1])

                    try:
                        WebDriverWait(self.main_driver, 20).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "/html/body/div/div[1]/div/div/div[3]/div/h1",
                                )
                            )  # PROCEED TO CHECKOUT BUTTON
                        )
                        time.sleep(4)
                        if first_scrapping:
                            try:
                                market = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[3]/td[4]",
                                ).text
                            except Exception as e:
                                market = self.main_driver.find_element(
                                    By.XPATH,
                                    "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/td[4]",
                                ).text
                                print(f"Error: {e}")
                            first_scrapping = False
                        try:
                            place_text = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[1]/td[4]",
                            ).text
                        except:
                            WebDriverWait(self.main_driver, 20).until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[4]",
                                    )
                                )  # PROCEED TO CHECKOUT BUTTON
                            )
                            place_text = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[4]",
                            ).text
                        try:
                            user_level_match = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/span[2]",
                            ).text
                        except:
                            user_level_match = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/span[2]",
                            ).text
                        try:
                            user_trust_level = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/span[1]",
                            ).text
                        except:
                            user_trust_level = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/span[1]",
                            ).text
                        try:
                            join_date_user = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/i[2]",
                            ).text
                        except:
                            join_date_user = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/i[2]",
                            ).text
                        try:
                            total_sales_product = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/i[1]",
                            ).text
                        except:
                            total_sales_product = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/i[1]",
                            ).text
                        try:
                            payment_type = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[3]/td[2]",
                            ).text
                        except:
                            payment_type = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[3]/td[2]",
                            ).text
                        try:
                            product_type_text = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]",
                            ).text
                        except:
                            product_type_text = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]",
                            ).text

                        user_level_match = re.search(r"\d+", user_level_match)
                        if user_level_match:
                            user_level_match = user_level_match.group()

                        user_trust_level = re.search(r"\d+", user_trust_level)
                        if user_trust_level:
                            user_trust_level = user_trust_level.group()

                        try:
                            button = self.main_driver.find_element(
                                By.XPATH,
                                f"/html/body/div/div[1]/div/div/div[3]/div/div[2]/label[2]",
                            )  # boton "ORDER"
                        except:
                            button = self.main_driver.find_element(
                                By.XPATH,
                                f"/html/body/div/div[1]/div/div/div[3]/div/div[3]/label[2]",
                            )

                        self.main_driver.execute_script(
                            "arguments[0].scrollIntoView();", button
                        )
                        button.click()
                        time.sleep(2)

                        try:
                            product = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[2]/div[2]/p[1]",
                            ).text
                        except:
                            product = self.main_driver.find_element(
                                By.XPATH,
                                "/html/body/div/div[1]/div/div/div[3]/div/div[3]/div[2]/p[1]",
                            ).text

                        product = re.findall(r":\s*([0-9.]+)(?=/)", product)
                        if len(product) == 3:
                            stealth_level = product[0]
                            quality_level = product[1]
                            price_value_rating = product[2]
                        else:
                            stealth_level = None
                            quality_level = None
                            price_value_rating = None
                        time.sleep(2)
                        self.main_driver.close()
                        self.main_driver.switch_to.window(windows[0])
                        time.sleep(3)
                    except Exception as e:
                        print(f"Error: {e}")
                        time.sleep(2)
                        self.main_driver.close()
                        self.main_driver.switch_to.window(windows[0])
                        time.sleep(3)
                    if not last_page:
                        WebDriverWait(self.main_driver, 200).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "//nav[2]//ul[@class='pagination']/li[last()]",
                                )
                            )
                        )

                    self.config["user_info"]["user_level"].append(user_level_match)
                    self.config["user_info"]["user_trust_level"].append(
                        user_trust_level
                    )
                    self.config["market_info"]["specialized"].append(market)
                    self.config["user_info"]["join_year_user"].append(join_date_user)
                    self.config["user_info"]["orders"]["completed"].append(
                        total_sales_product
                    )
                    self.config["market_info"]["payment_method"].append(payment_type)
                    self.config["market_info"]["product_type"].append(product_type_text)
                    self.config["quality_info"]["stealth_level"].append(stealth_level)
                    self.config["quality_info"]["product_quality_level"].append(
                        quality_level
                    )
                    self.config["quality_info"]["price_value_rating"].append(
                        price_value_rating
                    )
                    self.config["text"]["all"].append(matches)
                    self.config["user_info"]["user"].append(matches_user)
                    self.config["place_info"]["place"].append(place_text)
                    self.config["market_info"]["price"].append(price_match)
                    self.config["sales_info"]["transactions"].append(transactions)

                else:
                    print(f"Product {matches} is duplicated, will not be process")

            try:
                self.main_driver.find_element(
                    By.XPATH,
                    f"//nav[2]//a[contains(@class, 'page-link') and contains(text(),'{next_page_to_process}')]",
                )
            except NoSuchElementException:
                print("Processing last page or the only one available")
                last_page = True
            try:
                if last_page:
                    break

                print(f"Clicking page:{next_page_to_process}")
                next_page = WebDriverWait(self.main_driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f"//nav[2]//a[contains(@class, 'page-link') and contains(text(),'{next_page_to_process}')]",
                        )
                    )
                )
                next_page_to_process = next_page_to_process + 1
                next_page.click()
                time.sleep(3)
                WebDriverWait(self.main_driver, 200).until(
                    lambda driver: driver.find_element(
                        By.XPATH,
                        "/html/body/div/div[1]/div/div/div[3]/div/div[2]/table/tbody/tr/td[2]/a[1]",
                    ).text
                    != old_text
                )
                time.sleep(3)
                try:
                    self.main_driver.find_element(
                        By.XPATH,
                        f"//nav[2]//a[contains(@class, 'page-link') and contains(text(),'{next_page_to_process}')]",
                    )
                except NoSuchElementException:
                    print("Processing last page or the only one available")
                    last_page = True

            except:
                print("No more available pages")
                break

        df_data_extracted = pd.DataFrame(
            {
                "Product Name": self.config["text"]["all"],
                "Seller": self.config["user_info"]["user"],
                "Origin": self.config["place_info"]["place"],
                "Price": self.config["market_info"]["price"],
                "Payment Method": self.config["market_info"]["payment_method"],
                "Product Type": self.config["market_info"]["product_type"],
                "User Level": self.config["user_info"]["user_level"],
                "User Trust Level": self.config["user_info"]["user_trust_level"],
                "Stealth Transaction Rating": self.config["quality_info"][
                    "stealth_level"
                ],
                "Product Quality Rating": self.config["quality_info"][
                    "product_quality_level"
                ],
                "Price/Value Rating": self.config["quality_info"]["price_value_rating"],
                "Specialized Market": self.config["market_info"]["specialized"],
                "Date Product": self.config["user_info"]["join_year_user"],
                "User Transactions": self.config["sales_info"]["transactions"],
                "Total Sales Product": self.config["user_info"]["orders"]["completed"],
            }
        ).sort_values(by="Seller")

        os.makedirs("DATA_EXTRACTED", exist_ok=True)
        df_data_extracted.to_excel(
            os.path.join("DATA_EXTRACTED", f"{self.file_output_name}.xlsx"), index=True
        )
        df_data_extracted.to_csv(
            os.path.join("DATA_EXTRACTED", f"{self.file_output_name}.csv"),
            index=False,
            sep=",",
        )
        self.continue_scrapping()
