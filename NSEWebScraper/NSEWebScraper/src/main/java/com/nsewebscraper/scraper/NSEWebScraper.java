package com.nsewebscraper.scraper;

import com.nsewebscraper.model.LargeDeal;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

@Component
public class NSEWebScraper {

    private static final String URL = "https://www.nseindia.com/market-data/large-deals";

    public List<LargeDeal> scrapeData() {
        System.out.println("🚀 Initializing WebDriver...");

        try {
            // ✅ Set up WebDriverManager and ensure ChromeDriver is downloaded
            WebDriverManager.chromedriver().setup();

            // ✅ Configure ChromeOptions to ensure the browser opens
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--start-maximized"); // Open browser in full screen
            options.addArguments("--disable-blink-features=AutomationControlled"); // Prevent detection

            // ✅ Manually specify ChromeDriver path if needed (Optional)
             System.setProperty("webdriver.chrome.driver", "D:/NSEWebScraper/chromedriver.exe");

            WebDriver driver = new ChromeDriver(options);
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));

            System.out.println("✅ ChromeDriver launched successfully!");

            // ✅ Open NSE website
            driver.get(URL);
            System.out.println("🌐 Opened URL: " + URL);

            // ✅ Wait for the table to load dynamically
            wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath("//table/tbody/tr")));

            // ✅ Find table rows
            List<WebElement> rows = driver.findElements(By.xpath("//table/tbody/tr"));
            System.out.println("🔍 Total Rows Found: " + rows.size());

            List<LargeDeal> deals = new ArrayList<>();

            for (WebElement row : rows) {
                List<WebElement> cols = row.findElements(By.tagName("td"));

                if (cols.size() > 5) {
                    LargeDeal deal = new LargeDeal();
                    deal.setSecurity(cols.get(0).getText());
                    deal.setClientName(cols.get(1).getText());
                    deal.setDealType(cols.get(2).getText());
                    deal.setQuantity(cols.get(3).getText());
                    deal.setPrice(cols.get(4).getText());
                    deal.setDate(cols.get(5).getText());
                    deals.add(deal);
                }
            }

            System.out.println("✅ Scraped Deals: " + deals);

            // ✅ Keep browser open for 10 seconds before quitting
            Thread.sleep(10000);

            driver.quit(); // Close browser
            return deals;

        } catch (Exception e) {
            System.out.println("❌ Error occurred: " + e.getMessage());
            e.printStackTrace();
            return new ArrayList<>();
        }
    }
}
