package com.nsewebscraper.repository;

import com.nsewebscraper.model.LargeDeal;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LargeDealRepository extends JpaRepository<LargeDeal, Long> {
}
