package com.nsewebscraper;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
@SpringBootApplication
@EnableScheduling
public class NseWebScraperApplication {

	public static void main(String[] args) {
		SpringApplication.run(NseWebScraperApplication.class, args);
	}

}
