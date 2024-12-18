from selenium import webdriver
from selenium..webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.chrome()
driver.get("steampage")
time.sleep(10)

reviews = []
review_elements= driver.find.elements(By.CLASS_NAME,apphub_card)