# Stage 1: Build the backend application
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app

# Copy gradle wrapper and project definition files
COPY gradlew .
COPY gradle/ gradle/
COPY build.gradle settings.gradle ./

# Fix line endings and grant execute permission
RUN sed -i 's/\r$//' gradlew && chmod +x gradlew

# Copy source code and build jar
COPY src/ src/
RUN ./gradlew bootJar -x test --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Add non-root user for security best practice
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy built artifact from builder stage
COPY --from=builder /app/build/libs/campus-hub-1.0.0.jar app.jar

# Use non-root user
USER appuser:appgroup

# Expose default application port
EXPOSE 8080

# Run Spring Boot application
ENTRYPOINT ["java", "-jar", "app.jar"]
