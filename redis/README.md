# Redis
This is a Key Value (KV) database that is used to store the chats of users

## Redis and Vercel KV
The open sources frontend template that this project is based from, uses Vercel KV. Vercel KV is a cloud service offered by vercel. However, Vercel KV is just Redis behind the curtain. We hosted our own redis database and use the Vercel KV npm package to interface with it. 

Just a simple swap.

## docker-compose.yaml Breakdown
``` yaml
version: '3.1'

services:
  redis:
    image: redis
    ports:
      - '6379:6379' # will be used in SRH_CONNECTION_STRING down below

  serverless-redis-http:
    ports:
      - '8079:80' # if run locally, KV_REST_API_URL in frontend's .env would be "http://localhost:8079"
    image: hiett/serverless-redis-http:latest
    environment:
      SRH_MODE: env
      SRH_TOKEN: example_token # make a random secure token. if run locally, KV_REST_API_TOKEN in frontend's .env would be "example_token"
      SRH_CONNECTION_STRING: 'redis://redis:6379' # Using `redis` hostname since they're in the same Docker network.
```

## Running Locally
```bash 
cd redis
docker compose up --build
```

## What is hiett/serverless-redis-http?
1. HTTP-based Redis Pooler: This means that the system or package provides a way to access Redis, a type of database/cache, using HTTP requests. Instead of directly connecting to Redis through traditional means (like a direct client connection), it uses HTTP as the communication protocol. This allows for more flexibility in how applications can interact with Redis, especially in environments where direct connections might not be feasible or efficient.

2. Access Redis from Serverless: Serverless computing is a model where developers can write code that runs in response to events without having to manage the infrastructure. In this context, it means you can utilize Redis within a serverless architecture. This is particularly useful because serverless platforms typically have limitations on long-lived connections, which can be problematic for traditional Redis clients that maintain persistent connections.

3. Without Overloading Connection Limits: Redis has a limit on the number of connections it can handle simultaneously. When operating in a serverless environment where instances are ephemeral and can scale up and down rapidly, managing these connections becomes challenging. The HTTP-based Redis pooler likely manages connections to Redis in a way that prevents overloading Redis with too many simultaneous connections. It likely pools and manages connections efficiently, ensuring that the connection limit is not exceeded.

In essence, hiett/serverless-redis-http provides a solution for accessing Redis from a serverless environment using HTTP requests, while also ensuring that the connection limits of Redis are not exceeded, thus making it a more efficient and scalable approach.