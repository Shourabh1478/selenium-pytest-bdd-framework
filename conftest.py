
import logging
import os
from datetime import datetime
import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser: chrome or firefox")


@pytest.fixture(scope="session", autouse=True)
def cleanup_old_results():
    """
    Cleans up old logs, reports, and screenshots before the test session starts.
    This acts like a 'Global Setup' in a Java framework.
    """
    # List of directories to clear
    dirs_to_clean = ['reports/screenshots', 'logs']
    
    # Also define the main report file to delete
    files_to_clean = ['reports/report.html']

    print("\n--- Cleaning up previous test results ---")
    
    for directory in dirs_to_clean:
        if os.path.exists(directory):
            # shutil.rmtree deletes the folder and all its contents
            shutil.rmtree(directory)
        os.makedirs(directory) # Recreate empty folder
        print(f"Cleared directory: {directory}")

    for file in files_to_clean:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted old report: {file}")
            
    print("--- Cleanup complete. Starting session ---\n")

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Sets up the basic configuration for logging once per session."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    log_filename = f"logs/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler() # This prints to the console
        ]
    )
    logging.info("Logging is set up. Log file: %s", log_filename)



@pytest.fixture
def logger(request):
    """Fixture that provides a logger instance for the specific test being run."""
    # This creates a logger named after the specific test case
    return logging.getLogger(request.node.name)

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    
    if browser == "chrome":
        # Selenium 4 will automatically find the driver on your PATH or download it
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress ChromeDriver logs
        options.add_argument("--disable-features=SystemCpuProbe") # THE DIRECT FIX
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3") # 3 = FATAL ONLY

    # 2. Add arguments to bypass system-level monitoring that causes the PDH error
        options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
        options.add_argument("--no-sandbox")           # Bypass OS security model
        options.add_argument("--disable-gpu")           # Often helps with Windows-specific hangs
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-allow-origins=*") # Fixes handshake hangs


        driver = webdriver.Chrome(options=options) 
    elif browser == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # We want to capture screenshots on failures during the 'call' phase
    # This also captures failures during 'setup' (like browser launch issues)
    if report.failed or (report.when == "call" and report.failed):
        try:
            # 1. Access the driver fixture safely
            # In Pytest-BDD, driver is usually in item.funcargs
            driver = item.funcargs.get('driver')
            
            if driver:
                # 2. Setup path
                screenshot_dir = "reports/screenshots"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                # 3. Create unique filename (crucial for reruns)
                # item.nodeid gives a unique ID even for parameterized/rerun tests
                timestamp = datetime.now().strftime('%H%M%S')
                clean_name = item.name.replace("[", "_").replace("]", "_").replace(" ", "_")
                file_name = f"{clean_name}_{timestamp}.png"
                destination_path = os.path.join(screenshot_dir, file_name)
                
                # 4. Save the file
                driver.save_screenshot(destination_path)
                
                # 5. Attach to HTML Report
                pytest_html = item.config.pluginmanager.getplugin('html')
                if pytest_html:
                    extra = getattr(report, 'extra', [])
                    # Use a relative path from the 'reports' folder for the HTML file to find it
                    html_path = f"screenshots/{file_name}"
                    screenshot_base64 = driver.get_screenshot_as_base64()
                    extra.append(pytest_html.extras.image(screenshot_base64))
                    extra.append(pytest_html.extras.image(html_path))
                    report.extra = extra
                    
                print(f"\n📸 Screenshot captured for {item.name}: {destination_path}")
        except Exception as e:
            print(f"\n❌ Screenshot capture failed: {e}")

@pytest.fixture
def context():
    """A simple dictionary to share data between steps."""
    return {}
