package com.nsewebscraper.controller;

import com.nsewebscraper.model.LargeDeal;
import com.nsewebscraper.service.ScraperService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/deals")
public class ScraperController {

    @Autowired
    private ScraperService scraperService;

    // Fetch the latest deals from the database
    @GetMapping
    public List<LargeDeal> getAllDeals() {
        return scraperService.getAllDeals();
    }

    // Trigger the scraping process manually
    @PostMapping("/scrape")
    public String triggerScraping() {
        scraperService.scrapeAndSaveDeals();
        return "Scraping started successfully!";
    }
}
