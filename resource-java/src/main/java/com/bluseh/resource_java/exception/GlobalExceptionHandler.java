package com.bluseh.resource_java.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.web.reactive.error.ErrorWebExceptionHandler;
import org.springframework.cloud.gateway.support.NotFoundException;
import org.springframework.core.annotation.Order;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@Component
@Order(-1)
public class GlobalExceptionHandler implements ErrorWebExceptionHandler {

    @Override
    public Mono<Void> handle(ServerWebExchange exchange, Throwable ex) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.OK);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> result = new HashMap<>();
        result.put("success", false);
        result.put("timestamp", System.currentTimeMillis());

        if (ex instanceof NotFoundException) {
            result.put("code", 404);
            result.put("message", "服务未找到");
            log.warn("Service not found: {}", ex.getMessage());
        } else if (ex instanceof java.net.ConnectException) {
            result.put("code", 503);
            result.put("message", "服务不可用");
            log.error("Service unavailable: {}", ex.getMessage());
        } else if (ex instanceof java.net.SocketTimeoutException) {
            result.put("code", 504);
            result.put("message", "请求超时");
            log.error("Request timeout: {}", ex.getMessage());
        } else {
            result.put("code", 500);
            result.put("message", "网关内部错误");
            log.error("Gateway internal error: {}", ex.getMessage(), ex);
        }

        String jsonResult = convertToJson(result);
        DataBuffer buffer = response.bufferFactory().wrap(jsonResult.getBytes(StandardCharsets.UTF_8));
        
        return response.writeWith(Mono.just(buffer));
    }

    private String convertToJson(Map<String, Object> result) {
        StringBuilder json = new StringBuilder();
        json.append("{");
        json.append("\"success\":").append(result.get("success")).append(",");
        json.append("\"code\":").append(result.get("code")).append(",");
        json.append("\"message\":\"").append(result.get("message")).append("\",");
        json.append("\"timestamp\":").append(result.get("timestamp"));
        json.append("}");
        return json.toString();
    }
} 