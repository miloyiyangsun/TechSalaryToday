import requests
from bs4 import BeautifulSoup
from groq import Groq
import time
import re
import json
import os
from pathlib import Path


# Groq API Configuration
# Load environment variables from .env file if it exists
def load_env_file():
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value


load_env_file()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")


class GroqTranslator:
    """
    A translation service using Groq API for fast, high-quality translations.
    使用 Groq API 进行快速、高质量翻译的翻译服务。
    """

    def __init__(self, api_key=GROQ_API_KEY):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Fast and efficient model

    def translate_text(self, text, source_lang="nl", target_lang="en"):
        """
        Translate text using Groq API.
        使用 Groq API 翻译文本。

        Args:
            text (str): Text to translate
            source_lang (str): Source language code (default: "nl" for Dutch)
            target_lang (str): Target language code (default: "en" for English)

        Returns:
            str: Translated text
        """
        if not text or not text.strip():
            return text

        # Create language names for better prompt
        lang_names = {
            "nl": "Dutch",
            "en": "English",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "it": "Italian",
        }

        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)

        prompt = f"""Translate the following {source_name} text to {target_name}. 
Provide only the translation, no explanations or additional text.

Text to translate:
{text}

Translation:"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.1,  # Low temperature for consistent translations
                max_tokens=1000,  # Adjust based on your needs
            )

            translated_text = chat_completion.choices[0].message.content.strip()
            return translated_text

        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails


# Initialize global translator instance
groq_translator = GroqTranslator()

# import time # We don't need time for this diagnostic step
# from deep_translator import GoogleTranslator # We don't need translation for this diagnostic step

# Selenium Imports - a more powerful tool for browser automation
# 引入 Selenium - 一个更强大的浏览器自动化工具
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def inspect_html_structure(url):
    """
    This function fetches the webpage and prints its full HTML content
    for inspection, helping us find the correct selectors for scraping.

    这个函数获取网页并打印其完整的HTML内容以供检查，
    帮助我们找到用于抓取的正确选择器。
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Print the entire HTML content for analysis
        # 打印整个HTML内容以供分析
        print("--- Start of Page HTML ---")
        print(response.text)
        print("--- End of Page HTML ---")

        # We can also try a very broad search to see what we get
        # 我们也可以尝试一个非常宽泛的搜索，看看能得到什么
        soup = BeautifulSoup(response.text, "html.parser")
        h2_tags = soup.find_all("h2")
        print(f"\n\n--- Found {len(h2_tags)} H2 tags for reference ---")
        for tag in h2_tags:
            print(tag.prettify())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the HTTP request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def stress_test_translation(url):
    """
    This function performs a stress test on the translation service:
    1. Scrapes all job postings from the first page of the given URL.
    2. Extracts all text content from each posting.
    3. Translates the content for each posting from Dutch to English.

    这个函数对翻译服务进行压力测试：
    1. 从给定的URL抓取第一页的所有招聘信息。
    2. 从每个招聘信息中提取所有文本内容。
    3. 将每个招聘信息的内容从荷兰语翻译成英语。
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # New Strategy: Find all job titles, then find their parent container (the "card").
        # 新策略：找到所有职位标题，然后找到它们的父容器（即"卡片"）。
        # The 'h2' tag seems to be the most reliable anchor for each job listing.
        # 'h2'标签似乎是每个职位列表最可靠的锚点。
        job_cards = [h2_tag.parent for h2_tag in soup.find_all("h2")]

        # Filter out any potential non-job h2 parents if they exist
        # 过滤掉任何可能存在的非职位h2父元素
        job_cards = [
            card for card in job_cards if card and card.select_one("a.jobTitle")
        ]

        if not job_cards:
            print("Could not find any job cards on the page using the new H2 strategy.")
            print("使用新的H2策略在页面上找不到任何招聘信息卡片。")
            return

        print(
            f"--- Stress Test: Scrape and Translate Full Page (Corrected Strategy) ---"
        )
        print(f"找到了 {len(job_cards)} 条招聘信息。现在开始逐条翻译...")
        print(f"Found {len(job_cards)} job postings. Starting translation for each...")
        print("-" * 50)

        translated_count = 0
        for i, card in enumerate(job_cards):
            # Extract all text from the card
            original_text = card.get_text(separator=" | ", strip=True)

            if not original_text:
                continue

            print(f"--- 正在处理第 {i+1} 条 (Processing item {i+1}) ---")
            print(f"原始荷兰语内容 (Original Dutch):\n{original_text}\n")

            # Translate the text
            try:
                translated_text = groq_translator.translate_text(original_text)
                print(f"翻译后英语内容 (Translated English):\n{translated_text}\n")
                translated_count += 1
            except Exception as e:
                print(f"翻译第 {i+1} 条时出错 (Error translating item {i+1}): {e}")

            print("-" * 50)
            time.sleep(1)

        print("--- 测试完成 (Test Complete) ---")
        print(f"总共找到 {len(job_cards)} 条信息，成功翻译 {translated_count} 条。")
        print(
            f"Found {len(job_cards)} items in total, successfully translated {translated_count} of them."
        )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the HTTP request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def scrape_multiple_pages(base_url, num_pages_to_scrape):
    """
    Scrapes and translates job postings from multiple pages of the website.

    从网站的多个页面上抓取和翻译招聘信息。

    1.  从第1页循环到指定的页数。
    2.  为每一页构建URL。
    3.  从每一页抓取和翻译工作数据。
    """
    total_jobs_found = 0
    total_jobs_translated = 0

    print(f"--- Starting Scraper for {num_pages_to_scrape} Pages ---")

    for page_num in range(1, num_pages_to_scrape + 1):
        # Construct the URL for the current page.
        # Based on common patterns, page numbers are often passed as a query parameter.
        # 为当前页面构建URL。
        # 根据常见模式，页码通常作为查询参数传递。
        paginated_url = f"{base_url}&page={page_num}"

        print(f"\n--- Scraping Page {page_num} ---")
        print(f"URL: {paginated_url}")
        print("-" * 50)

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(paginated_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = [h2_tag.parent for h2_tag in soup.find_all("h2")]
            job_cards = [
                card for card in job_cards if card and card.select_one("a.jobTitle")
            ]

            if not job_cards:
                print(
                    f"No job cards found on page {page_num}. This could be the last page."
                )
                break  # Exit the loop if a page has no jobs

            page_jobs_found = len(job_cards)
            total_jobs_found += page_jobs_found
            print(f"Found {page_jobs_found} jobs on this page.")

            translated_on_page = 0
            for i, card in enumerate(job_cards):
                original_text = card.get_text(separator=" | ", strip=True)
                if not original_text:
                    continue

                # For brevity in this test, let's just print the title
                job_title = card.select_one("a.jobTitle").get_text(strip=True)

                try:
                    translated_title = groq_translator.translate_text(
                        job_title, source_lang="nl", target_lang="en"
                    )
                    print(
                        f"  - Original: {job_title} -> Translated: {translated_title}"
                    )
                    total_jobs_translated += 1
                    translated_on_page += 1
                except Exception as e:
                    print(
                        f"    - Could not translate job title: {job_title}, Error: {e}"
                    )

                time.sleep(0.5)  # Shorten delay slightly for this multi-page test

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the HTTP request for page {page_num}: {e}")
            continue  # Skip to the next page if one fails
        except Exception as e:
            print(f"An unexpected error occurred on page {page_num}: {e}")
            continue

    print("\n--- Multi-Page Scraping Complete ---")
    print(f"Total pages scraped: {num_pages_to_scrape}")
    print(f"Total jobs found: {total_jobs_found}")
    print(f"Total jobs successfully translated: {total_jobs_translated}")


def run_large_scale_translation_test(base_url, max_jobs_to_translate):
    """
    Performs a large-scale stress test on the scraping and translation process.

    对抓取和翻译过程进行大规模压力测试。

    1.  获取并翻译招聘信息的完整文本。
    2.  逐页抓取，直到翻译了目标数量的职位。
    3.  测量并报告翻译任务的性能。
    """
    translated_jobs_count = 0
    page_num = 1
    all_translation_times = []

    print(
        f"--- Starting Large-Scale Test: Translating {max_jobs_to_translate} Full Job Postings ---"
    )
    start_time = time.time()

    while translated_jobs_count < max_jobs_to_translate:
        paginated_url = f"{base_url}&page={page_num}"
        print(
            f"\n--- Scraping Page {page_num} (Translated {translated_jobs_count}/{max_jobs_to_translate}) ---"
        )

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(paginated_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = [
                h2.parent
                for h2 in soup.find_all("h2")
                if h2.parent and h2.parent.select_one("a.jobTitle")
            ]

            if not job_cards:
                print("No more job cards found. Ending test.")
                break

            for card in job_cards:
                if translated_jobs_count >= max_jobs_to_translate:
                    break

                original_text = card.get_text(separator=" | ", strip=True)
                if not original_text:
                    continue

                translation_start_time = time.time()
                try:
                    translated_text = groq_translator.translate_text(
                        source="nl", target="en"
                    ).translate(original_text)
                    translation_end_time = time.time()

                    duration = translation_end_time - translation_start_time
                    all_translation_times.append(duration)

                    translated_jobs_count += 1

                    print(
                        f"Job {translated_jobs_count}/{max_jobs_to_translate}: OK ({duration:.2f}s)"
                    )
                    # print(f"  - Original: {original_text[:80]}...") # Optional: print snippet
                    # print(f"  - Translated: {translated_text[:80]}...") # Optional: print snippet

                except Exception as e:
                    print(f"Job {translated_jobs_count + 1}: FAILED. Error: {e}")

                # Aggressively short sleep time to stress the service
                # 积极缩短休眠时间以给服务带来压力
                time.sleep(0.2)

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page_num}: {e}")

        page_num += 1

    end_time = time.time()
    total_duration = end_time - start_time

    print("\n--- Test Complete: Performance Report ---")
    print(f"Total jobs translated: {translated_jobs_count}")
    print(f"Total time taken: {total_duration:.2f} seconds")

    if all_translation_times:
        min_time = min(all_translation_times)
        max_time = max(all_translation_times)
        avg_time = sum(all_translation_times) / len(all_translation_times)
        print(f"Shortest translation time: {min_time:.2f} seconds")
        print(f"Longest translation time: {max_time:.2f} seconds")
        print(f"Average translation time: {avg_time:.2f} seconds")
    else:
        print("No successful translations to report on.")


def get_full_job_description_with_selenium(detail_page_url):
    """
    Uses Selenium to load a job detail page, extract the full job description,
    and translate it to English.

    使用Selenium加载职位详情页面，提取完整的职位描述，并翻译成英文。
    """
    print(f"Processing job page: {detail_page_url}")

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the page
        driver.get(detail_page_url)
        time.sleep(2)  # Wait for page to load

        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Try to find the job description element
        # This selector might need adjustment based on the actual page structure
        description_element = soup.select_one("article.job-body")

        if description_element:
            # Extract text content
            original_text = description_element.get_text(separator="\n", strip=True)

            print("Original job description (first 300 characters):")
            print(
                original_text[:300] + "..."
                if len(original_text) > 300
                else original_text
            )
            print("\n" + "-" * 50)

            # Translate to English
            print("Translating to English...")
            translated_text = groq_translator.translate_text(original_text)

            print("Translated job description:")
            print(translated_text)
            print("\n" + "=" * 50)

            return {
                "url": detail_page_url,
                "original": original_text,
                "translated": translated_text,
                "success": True,
            }
        else:
            print("Could not find job description element on the page")
            return {
                "url": detail_page_url,
                "success": False,
                "error": "Element not found",
            }

    except Exception as e:
        print(f"Error processing {detail_page_url}: {e}")
        return {"url": detail_page_url, "success": False, "error": str(e)}

    finally:
        driver.quit()


def inspect_detail_page_html(list_url):
    """
    Scrapes the list page to get the first detail URL, then prints the
    entire HTML of that detail page for inspection. This helps us find the
    correct selector for the full job description.

    抓取列表页面以获取第一个详细信息的URL，然后打印该详细信息页面的
    整个HTML以供检查。这有助于我们为完整的职位描述找到正确的选择器。
    """
    print("--- Inspecting Detail Page HTML ---")

    try:
        # Step 1: Get the detail page URL from the list page
        print("Step 1: Scraping list page to find a job link...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        list_response = requests.get(list_url, headers=headers)
        list_response.raise_for_status()
        list_soup = BeautifulSoup(list_response.text, "html.parser")
        first_job_link_tag = list_soup.select_one("a.jobTitle")

        if not first_job_link_tag or not first_job_link_tag.get("href"):
            print("Could not find a valid link to a job detail page.")
            return

        detail_page_url = first_job_link_tag.get("href")
        print(f"Found detail page URL: {detail_page_url}")

        # Step 2: Visit detail page and print its full HTML
        print("\nStep 2: Fetching full HTML from detail page for inspection...")
        detail_response = requests.get(detail_page_url, headers=headers)
        detail_response.raise_for_status()

        print("\n" + "=" * 25 + " DETAIL PAGE HTML START " + "=" * 25 + "\n")
        print(detail_response.text)
        print("\n" + "=" * 25 + " DETAIL PAGE HTML END " + "=" * 27 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the HTTP request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def diagnose_page_structure(base_url):
    """
    Diagnostic function to inspect the actual HTML structure of job pages
    and find the correct selectors for job descriptions.

    诊断函数，用于检查职位页面的实际HTML结构，
    找到职位描述的正确选择器。
    """
    print("--- Page Structure Diagnosis ---")

    try:
        # Get a few job links first
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        list_response = requests.get(base_url, headers=headers, timeout=10)
        list_response.raise_for_status()
        list_soup = BeautifulSoup(list_response.text, "html.parser")

        job_links = [a["href"] for a in list_soup.select("a.jobTitle") if a.get("href")]

        if not job_links:
            print("No job links found on the list page")
            return

        # Test the first job link
        test_url = job_links[0]
        print(f"Testing URL: {test_url}")

        # Try with simple requests first
        print("\n=== Testing with Simple HTTP Request ===")
        detail_response = requests.get(test_url, headers=headers, timeout=10)
        detail_response.raise_for_status()

        soup = BeautifulSoup(detail_response.text, "html.parser")

        # Look for various possible selectors
        selectors_to_test = [
            "article.job-body",
            "article",
            ".job-body",
            ".job-description",
            ".content",
            ".description",
            "#content",
            "main",
            ".main-content",
            "[class*='job']",
            "[class*='description']",
            "[class*='content']",
        ]

        print("Testing different CSS selectors:")
        for selector in selectors_to_test:
            elements = soup.select(selector)
            if elements:
                element = elements[0]
                text_content = element.get_text(strip=True)[:200]  # First 200 chars
                print(f"✓ '{selector}': Found {len(elements)} element(s)")
                print(f"  Sample text: {text_content}...")
                print()
            else:
                print(f"✗ '{selector}': No elements found")

        # Also try with Selenium
        print("\n=== Testing with Selenium (with JavaScript) ===")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(test_url)
            time.sleep(3)  # Wait for JS to load

            selenium_soup = BeautifulSoup(driver.page_source, "html.parser")

            print("Testing selectors with Selenium-rendered HTML:")
            for selector in selectors_to_test:
                elements = selenium_soup.select(selector)
                if elements:
                    element = elements[0]
                    text_content = element.get_text(strip=True)[:200]
                    print(f"✓ '{selector}': Found {len(elements)} element(s)")
                    print(f"  Sample text: {text_content}...")
                    print()
                else:
                    print(f"✗ '{selector}': No elements found")

        finally:
            driver.quit()

        # Save the HTML for manual inspection
        with open("diagnostic_simple.html", "w", encoding="utf-8") as f:
            f.write(detail_response.text)
        with open("diagnostic_selenium.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print(f"\nHTML files saved for manual inspection:")
        print(f"- diagnostic_simple.html (simple HTTP)")
        print(f"- diagnostic_selenium.html (Selenium with JS)")

    except Exception as e:
        print(f"Diagnosis failed: {e}")


def extract_structured_job_info(soup, url):
    """
    Extract structured job information with detailed labels and sections.

    提取结构化的职位信息，包含详细的标签和分区。
    """
    job_info = {
        "url": url,
        "extraction_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "company_info": {},
        "job_details": {},
        "requirements": {},
        "employment_conditions": {},
        "contact_info": {},
        "raw_content": "",
    }

    try:
        # Extract main job content
        main_content = soup.select_one(".jobColumn.wide")
        if not main_content:
            return None

        job_info["raw_content"] = main_content.get_text(separator="\n", strip=True)

        # Extract job title
        title_element = soup.select_one("h1")
        if title_element:
            job_info["job_details"]["title"] = title_element.get_text(strip=True)

        # Extract company information
        company_info_element = soup.select_one(".responsiveCompanyInfo")
        if company_info_element:
            company_text = company_info_element.get_text(strip=True)
            # Parse company info (format: Company · Location · Date)
            parts = [part.strip() for part in company_text.split("·")]
            if len(parts) >= 3:
                job_info["company_info"]["name"] = parts[0]
                job_info["company_info"]["location"] = parts[1].replace(
                    "Standplaats: ", ""
                )
                job_info["company_info"]["posting_date"] = parts[2]

        # Extract job features from sidebar
        features = {}
        feature_elements = soup.select(".jobFeatures .feature")
        for feature in feature_elements:
            label_elem = feature.select_one("b")
            desc_elem = feature.select_one(".description")
            if label_elem and desc_elem:
                label = label_elem.get_text(strip=True)
                description = desc_elem.get_text(strip=True)
                features[label] = description

        job_info["job_details"]["features"] = features

        # Extract contact information
        contact_elements = soup.select(".jobContact .contactInfo")
        for contact in contact_elements:
            contact_text = contact.get_text(separator=" | ", strip=True)
            if "Adres" in contact_text:
                job_info["contact_info"]["address"] = contact_text.replace(
                    "Adres | ", ""
                )
            elif "Contactgegevens" in contact_text:
                job_info["contact_info"]["contact_details"] = contact_text.replace(
                    "Contactgegevens | ", ""
                )

        # Parse main content for structured sections
        content_text = job_info["raw_content"]

        # Try to identify different sections in the job description
        sections = {
            "job_description": "",
            "requirements": "",
            "what_we_offer": "",
            "employment_conditions": "",
            "application_process": "",
        }

        # Define section patterns (Dutch and English)
        section_patterns = {
            "job_description": [
                r"(Functieomschrijving|Job description|What will you do|Wat ga je doen)",
                r"(About the role|Over de functie)",
            ],
            "requirements": [
                r"(Functie-eisen|Job requirements|Requirements|Wat vragen wij|What do we ask)",
                r"(Your profile|Jouw profiel|Competencies|Competenties)",
            ],
            "what_we_offer": [
                r"(Wat bieden wij|What we offer|What do we offer|Wat krijg je ervoor terug)"
            ],
            "employment_conditions": [
                r"(Arbeidsvoorwaarden|Employment conditions|Salary|Salaris)"
            ],
            "application_process": [
                r"(Solliciteren|Apply|Application|How to apply|Bijzonderheden)"
            ],
        }

        # Split content into sections based on patterns
        current_section = "job_description"
        current_content = []

        lines = content_text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line starts a new section
            section_found = False
            for section_name, patterns in section_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Save previous section
                        if current_content:
                            sections[current_section] = "\n".join(
                                current_content
                            ).strip()
                        # Start new section
                        current_section = section_name
                        current_content = [line]
                        section_found = True
                        break
                if section_found:
                    break

            if not section_found:
                current_content.append(line)

        # Save the last section
        if current_content:
            sections[current_section] = "\n".join(current_content).strip()

        job_info["structured_content"] = sections

        return job_info

    except Exception as e:
        print(f"Error extracting structured job info: {e}")
        return None


def translate_structured_job_info(job_info):
    """
    Translate structured job information to English.

    将结构化的职位信息翻译成英文。
    """
    translated_info = job_info.copy()

    try:
        # Translate company info
        if "name" in job_info["company_info"]:
            translated_info["company_info"]["name_en"] = groq_translator.translate_text(
                source="auto", target="en"
            ).translate(job_info["company_info"]["name"])

        # Translate job title
        if "title" in job_info["job_details"]:
            translated_info["job_details"]["title_en"] = groq_translator.translate_text(
                source="auto", target="en"
            ).translate(job_info["job_details"]["title"])

        # Translate job features
        if "features" in job_info["job_details"]:
            translated_features = {}
            for key, value in job_info["job_details"]["features"].items():
                translated_key = groq_translator.translate_text(key)
                translated_value = groq_translator.translate_text(
                    source="auto", target="en"
                ).translate(value)
                translated_features[f"{key} ({translated_key})"] = (
                    f"{value} ({translated_value})"
                )
            translated_info["job_details"]["features_translated"] = translated_features

        # Translate structured content sections
        translated_sections = {}
        for section_name, content in job_info["structured_content"].items():
            if content.strip():
                # Limit content length for translation
                content_to_translate = (
                    content[:3000] if len(content) > 3000 else content
                )
                translated_content = groq_translator.translate_text(
                    source="auto", target="en"
                ).translate(content_to_translate)
                translated_sections[section_name] = {
                    "original": content,
                    "translated": translated_content,
                    "word_count": len(content.split()),
                }

        translated_info["translated_sections"] = translated_sections

        return translated_info

    except Exception as e:
        print(f"Error translating job info: {e}")
        return translated_info


def print_structured_job_info(job_info):
    """
    Print job information in a beautiful, structured format.

    以美观的结构化格式打印职位信息。
    """
    print("\n" + "=" * 80)
    print("🎯 STRUCTURED JOB ANALYSIS REPORT")
    print("=" * 80)

    # Basic Information
    print("\n📋 BASIC INFORMATION")
    print("-" * 40)
    print(f"🔗 URL: {job_info['url']}")
    print(f"⏰ Extracted: {job_info['extraction_timestamp']}")

    # Job Title
    if "title" in job_info["job_details"]:
        print(f"\n💼 JOB TITLE")
        print("-" * 40)
        print(f"Original: {job_info['job_details']['title']}")
        if "title_en" in job_info["job_details"]:
            print(f"English:  {job_info['job_details']['title_en']}")

    # Company Information
    print(f"\n🏢 COMPANY INFORMATION")
    print("-" * 40)
    company_info = job_info["company_info"]
    if "name" in company_info:
        print(f"Company:  {company_info['name']}")
        if "name_en" in company_info:
            print(f"         ({company_info['name_en']})")
    if "location" in company_info:
        print(f"Location: {company_info['location']}")
    if "posting_date" in company_info:
        print(f"Posted:   {company_info['posting_date']}")

    # Job Features
    if (
        "features_translated" in job_info["job_details"]
        and job_info["job_details"]["features_translated"]
    ):
        print(f"\n🏷️  JOB FEATURES (TRANSLATED)")
        print("-" * 40)
        for key, value in job_info["job_details"]["features_translated"].items():
            print(f"{key}")
            print(f"    {value}")
            print()
    elif "features" in job_info["job_details"] and job_info["job_details"]["features"]:
        print(f"\n🏷️  JOB FEATURES (ORIGINAL)")
        print("-" * 40)
        for key, value in job_info["job_details"]["features"].items():
            print(f"{key:15}: {value}")

    # Contact Information
    if job_info["contact_info"]:
        print(f"\n📞 CONTACT INFORMATION")
        print("-" * 40)
        for key, value in job_info["contact_info"].items():
            if value:
                print(f"{key}: {value}")

    # Translated Content Sections
    if "translated_sections" in job_info:
        print(f"\n📄 DETAILED JOB CONTENT (TRANSLATED)")
        print("=" * 80)

        section_titles = {
            "job_description": "🎯 JOB DESCRIPTION",
            "requirements": "✅ REQUIREMENTS & QUALIFICATIONS",
            "what_we_offer": "🎁 WHAT WE OFFER",
            "employment_conditions": "💰 EMPLOYMENT CONDITIONS",
            "application_process": "📝 APPLICATION PROCESS",
        }

        for section_name, section_data in job_info["translated_sections"].items():
            if section_data["translated"].strip():
                title = section_titles.get(
                    section_name, section_name.upper().replace("_", " ")
                )
                print(f"\n{title}")
                print("-" * 60)
                print(f"📊 Word Count: {section_data['word_count']} words")
                print(f"📝 Content:")
                print(section_data["translated"])
                print()

    # Statistics
    print(f"\n📊 EXTRACTION STATISTICS")
    print("-" * 40)
    total_words = len(job_info["raw_content"].split())
    print(f"Total words extracted: {total_words}")

    sections_with_content = sum(
        1
        for section in job_info["translated_sections"].values()
        if section["translated"].strip()
    )
    print(f"Sections identified: {sections_with_content}")

    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)


def print_json_data(job_info, translated_job_info):
    """
    Print both original and translated JSON data for inspection.

    打印原始和翻译后的JSON数据以供检查。
    """
    print("\n" + "=" * 80)
    print("📄 RAW JSON DATA OUTPUT")
    print("=" * 80)

    # Print Original JSON Data
    print("\n🔍 ORIGINAL JSON DATA (BEFORE TRANSLATION)")
    print("-" * 60)
    try:
        original_json = json.dumps(job_info, ensure_ascii=False, indent=2)
        print(original_json)
    except Exception as e:
        print(f"Error printing original JSON: {e}")

    print("\n" + "=" * 60)

    # Print Translated JSON Data
    print("\n🌐 TRANSLATED JSON DATA (AFTER TRANSLATION)")
    print("-" * 60)
    try:
        translated_json = json.dumps(translated_job_info, ensure_ascii=False, indent=2)
        print(translated_json)
    except Exception as e:
        print(f"Error printing translated JSON: {e}")

    print("\n" + "=" * 80)
    print("📊 JSON DATA COMPARISON COMPLETE")
    print("=" * 80)


def process_single_structured_job(base_url):
    """
    Process a single job with detailed structured output.

    处理单个职位并输出详细的结构化信息。
    """
    print("🚀 Starting structured job analysis...")

    # Setup browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = None

    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Browser initialized successfully")

        # Get job links
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        print("🔍 Fetching job listings...")
        list_response = requests.get(base_url, headers=headers, timeout=15)
        list_response.raise_for_status()
        list_soup = BeautifulSoup(list_response.text, "html.parser")

        job_links = [a["href"] for a in list_soup.select("a.jobTitle") if a.get("href")]

        if not job_links:
            print("❌ No job links found")
            return

        # Process the first job
        job_url = job_links[0]
        print(f"🎯 Processing job: {job_url}")

        # Extract content with Selenium
        driver.get(job_url)
        time.sleep(3)

        selenium_soup = BeautifulSoup(driver.page_source, "html.parser")

        print("📊 Extracting structured information...")
        job_info = extract_structured_job_info(selenium_soup, job_url)

        if not job_info:
            print("❌ Failed to extract job information")
            return

        print("🌐 Translating content...")
        translated_job_info = translate_structured_job_info(job_info)

        print("📄 Generating structured report...")
        print_structured_job_info(translated_job_info)

        # Also save to JSON file for further analysis
        output_file = "structured_job_analysis.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(translated_job_info, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Detailed data saved to: {output_file}")

        print_json_data(job_info, translated_job_info)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser closed")


if __name__ == "__main__":
    base_job_url = "https://tweakers.net/carriere/it-banen/zoeken/#filter:q1ZKTixKTS3ySS1LzSlWsoo2jNVRyspPCshJTE5NCc7MS04NSC3KzE9RsjKsBQA"

    # Process single job with structured output
    process_single_structured_job(base_job_url)
