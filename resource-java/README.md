# Spring Cloud API Gateway with Nacos Discovery

这是一个基于Spring Cloud Gateway和Nacos服务发现的API网关项目。

## 功能特性

- 🚀 **Spring Cloud Gateway**: 基于Spring Cloud Gateway的API网关
- 🔍 **Nacos服务发现**: 使用Nacos作为服务注册与发现中心
- ⚖️ **负载均衡**: 集成Spring Cloud LoadBalancer
- 🔒 **跨域支持**: 全局CORS配置
- 📊 **监控端点**: 集成Spring Boot Actuator
- 🛡️ **全局过滤**: 请求日志记录和异常处理
- 🏥 **健康检查**: 服务健康状态监控

## 技术栈

- Spring Boot 3.4.7
- Spring Cloud 2024.0.1
- Spring Cloud Gateway
- Nacos Discovery 2022.0.0.0
- Spring Cloud LoadBalancer
- Lombok

## 快速开始

### 1. 环境准备

确保你的系统已安装：
- JDK 24
- Maven 3.6+
- Nacos Server 2.x

### 2. 启动Nacos

```bash
# 下载并启动Nacos
wget https://github.com/alibaba/nacos/releases/download/2.2.3/nacos-server-2.2.3.zip
unzip nacos-server-2.2.3.zip
cd nacos/bin
./startup.sh -m standalone
```

Nacos默认访问地址：http://localhost:8848/nacos
默认账号密码：nacos/nacos

### 3. 启动API Gateway

```bash
# 进入项目目录
cd resource-java

# 编译项目
mvn clean compile

# 启动应用
mvn spring-boot:run
```

API Gateway将在 http://localhost:8080 启动

### 4. 验证服务

访问以下端点验证服务状态：

- 健康检查: http://localhost:8080/health/status
- 服务列表: http://localhost:8080/health/services
- 服务信息: http://localhost:8080/health/info
- Actuator: http://localhost:8080/actuator

## 配置说明

### 主要配置项

```properties
# 应用名称
spring.application.name=api-gateway

# 服务器端口
server.port=8080

# Nacos服务发现配置
spring.cloud.nacos.discovery.server-addr=127.0.0.1:8848
spring.cloud.nacos.discovery.namespace=public
spring.cloud.nacos.discovery.group=DEFAULT_GROUP

# Gateway路由配置
spring.cloud.gateway.discovery.locator.enabled=true
spring.cloud.gateway.discovery.locator.lower-case-service-id=true
```

### 路由配置

项目预配置了以下路由：

1. **用户服务路由**
   - 路径: `/api/users/**`
   - 目标服务: `user-service`
   - 过滤器: 去除路径前缀

2. **订单服务路由**
   - 路径: `/api/orders/**`
   - 目标服务: `order-service`
   - 过滤器: 去除路径前缀

3. **默认路由**
   - 路径: `/**`
   - 目标服务: `default-service`

## 使用示例

### 1. 注册微服务

确保你的微服务已注册到Nacos，例如：

```yaml
# user-service application.yml
spring:
  application:
    name: user-service
  cloud:
    nacos:
      discovery:
        server-addr: 127.0.0.1:8848
```

### 2. 通过网关访问服务

```bash
# 访问用户服务
curl http://localhost:8080/api/users/1

# 访问订单服务
curl http://localhost:8080/api/orders/1
```

### 3. 查看路由信息

```bash
# 查看所有路由
curl http://localhost:8080/actuator/gateway/routes
```

## 自定义配置

### 添加新的路由

在 `application.properties` 中添加：

```properties
spring.cloud.gateway.routes[2].id=product-service-route
spring.cloud.gateway.routes[2].uri=lb://product-service
spring.cloud.gateway.routes[2].predicates[0]=Path=/api/products/**
spring.cloud.gateway.routes[2].filters[0]=StripPrefix=1
```

### 自定义过滤器

在 `GatewayConfig.java` 中添加自定义过滤器：

```java
@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("custom-route", r -> r
            .path("/api/custom/**")
            .filters(f -> f
                .stripPrefix(1)
                .addRequestHeader("Custom-Header", "value"))
            .uri("lb://custom-service"))
        .build();
}
```

## 监控和日志

### 日志配置

项目配置了详细的日志记录：

- Gateway请求日志: `DEBUG` 级别
- Nacos连接日志: `DEBUG` 级别
- 全局过滤器日志: `INFO` 级别

### 监控端点

- `/actuator/health`: 健康检查
- `/actuator/info`: 应用信息
- `/actuator/gateway/routes`: 路由信息
- `/actuator/gateway/globalfilters`: 全局过滤器
- `/actuator/metrics`: 指标信息

## 故障排除

### 常见问题

1. **Nacos连接失败**
   - 检查Nacos服务是否启动
   - 验证网络连接和端口配置

2. **服务发现失败**
   - 确认微服务已正确注册到Nacos
   - 检查服务名称和命名空间配置

3. **路由不生效**
   - 验证路由配置语法
   - 检查目标服务是否可用

### 调试模式

启用调试日志：

```properties
logging.level.org.springframework.cloud.gateway=DEBUG
logging.level.com.alibaba.nacos=DEBUG
```

## 部署

### Docker部署

```dockerfile
FROM openjdk:24-jdk-slim
COPY target/resource-java-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

### 生产环境配置

```properties
# 生产环境配置
spring.cloud.nacos.discovery.server-addr=nacos-server:8848
spring.cloud.nacos.discovery.namespace=prod
logging.level.org.springframework.cloud.gateway=WARN
management.endpoints.web.exposure.include=health,info
```

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License 