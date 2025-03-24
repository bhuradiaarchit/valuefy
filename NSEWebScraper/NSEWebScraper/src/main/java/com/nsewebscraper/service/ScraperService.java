package com.nsewebscraper.service;

import com.nsewebscraper.model.LargeDeal;
import com.nsewebscraper.repository.LargeDealRepository;
import com.nsewebscraper.scraper.NSEWebScraper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ScraperService {

    @Autowired
    private NSEWebScraper nseWebScraper;

    @Autowired
    private LargeDealRepository repository;

    // Fetch all deals from DB
    public List<LargeDeal> getAllDeals() {
        return repository.findAll();
    }

    // Scrape data and save to DB
    public void scrapeAndSaveDeals() {
        List<LargeDeal> deals = nseWebScraper.scrapeData();
        repository.saveAll(deals);
        System.out.println("✅ Successfully saved " + deals.size() + " deals.");
    }
}
