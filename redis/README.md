# Redis
This is a Key Value (KV) database that is used to store the chats of users

## Redis and Vercel KV
The open sources frontend template that this project is based from, uses Vercel KV. Vercel KV is a cloud service offered by vercel. However, Vercel KV is just Redis behind the curtain. We hosted our own redis database and use the Vercel KV npm package to interface with it. 

Just a simple swap.

## Running Locally
```bash 
cd redis
docker compose up --build
```