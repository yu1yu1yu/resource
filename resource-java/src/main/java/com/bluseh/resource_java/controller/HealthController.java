package com.bluseh.resource_java.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/health")
public class HealthController {

    @Autowired
    private DiscoveryClient discoveryClient;

    @GetMapping("/status")
    public Mono<Map<String, Object>> healthStatus() {
        Map<String, Object> result = new HashMap<>();
        result.put("status", "UP");
        result.put("service", "api-gateway");
        result.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        result.put("uptime", System.currentTimeMillis());
        
        return Mono.just(result);
    }

    @GetMapping("/services")
    public Mono<Map<String, Object>> getServices() {
        Map<String, Object> result = new HashMap<>();
        result.put("services", discoveryClient.getServices());
        result.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        
        return Mono.just(result);
    }

    @GetMapping("/info")
    public Mono<Map<String, Object>> getInfo() {
        Map<String, Object> result = new HashMap<>();
        result.put("service", "api-gateway");
        result.put("version", "1.0.0");
        result.put("description", "Spring Cloud Gateway with Nacos Discovery");
        result.put("timestamp", LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")));
        
        return Mono.just(result);
    }
} 