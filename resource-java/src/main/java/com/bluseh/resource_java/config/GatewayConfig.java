package com.bluseh.resource_java.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsWebFilter;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

@Configuration
public class GatewayConfig {

    /**
     * 自定义路由配置
     */
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
                // 用户服务路由
                .route("user-service-route", r -> r
                        .path("/api/users/**")
                        .filters(f -> f
                                .stripPrefix(1)
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + "")
                                .addResponseHeader("X-Gateway-Response", "true"))
                        .uri("lb://user-service"))
                
                // 订单服务路由
                .route("order-service-route", r -> r
                        .path("/api/orders/**")
                        .filters(f -> f
                                .stripPrefix(1)
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + "")
                                .addResponseHeader("X-Gateway-Response", "true"))
                        .uri("lb://order-service"))
                
                // 默认路由 - 转发到默认服务
                .route("default-route", r -> r
                        .path("/**")
                        .filters(f -> f
                                .addRequestHeader("X-Response-Time", System.currentTimeMillis() + "")
                                .addResponseHeader("X-Gateway-Response", "true"))
                        .uri("lb://default-service"))
                .build();
    }

    /**
     * 跨域配置
     */
    @Bean
    public CorsWebFilter corsWebFilter() {
        CorsConfiguration corsConfig = new CorsConfiguration();
        corsConfig.setAllowedOriginPatterns(Arrays.asList("*"));
        corsConfig.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        corsConfig.setAllowedHeaders(Arrays.asList("*"));
        corsConfig.setAllowCredentials(true);
        corsConfig.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfig);

        return new CorsWebFilter(source);
    }
} 