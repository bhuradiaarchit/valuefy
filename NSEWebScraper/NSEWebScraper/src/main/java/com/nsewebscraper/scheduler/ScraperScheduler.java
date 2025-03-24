package com.nsewebscraper.scheduler;

import com.nsewebscraper.service.ScraperService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class ScraperScheduler {

    @Autowired
    private ScraperService scraperService;

    // Runs every day at 9 AM (adjust timing as needed)
    @Scheduled(cron = "0 0 9 * * ?")
    public void runScraperDaily() {
        scraperService.scrapeAndSaveDeals();
        System.out.println("✅ Scraping job executed at 9 AM.");
    }
}
