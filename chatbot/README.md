# Frontend

## Table of Contents

1. [File Structure](#file-structure)
2. [Nextjs API](#nextjs-api)
3. [Styling](#styling)
4. [env file](#env-file)
5. [Running Locally](#running-locally)
6. [Pushing to Container Registry](#pushing-to-container-registry)
   - [What is happening under the hood?](#what-is-happening-under-the-hood)
   - [To execute the push to the container registry](#to-execute-the-push-to-the-container-registry)
7. [Known Issues](#known-issues)

## File Structure
```
.
└── chatbot/
    ├── app/
    │   ├── (chat)/
    │   │   ├── chat/
    │   │   │   └── [id]/
    │   │   │       └── page.tsx
    │   │   ├── layout.tsx
    │   │   └── page.tsx
    │   ├── api/
    │   │   ├── auth/
    │   │   │   └── [...nextauth]/
    │   │   │       └── route.ts
    │   │   ├── chat/
    │   │   │   └── route.ts
    │   │   └── tags/
    │   │       └── route.ts
    │   ├── share/
    │   │   └── [id]/
    │   │       └── page.tsx
    │   ├── sign-in/
    │   │   └── page.tsx
    │   ├── actions.ts
    │   ├── global.css
    │   └── layout.tsx
    ├── components/
    │   ├── ui/
    │   │   └── {rest of files from ui are custom components}
    │   └── {rest of file in components come from shadcn/ui}
    ├── lib/
    │   └── hooks
    ├── public
    ├── .dockerignore
    ├── .env.example
    ├── .env
    ├── .gitignore
    ├── Dockerfile
    ├── README.md
    ├── auth.ts
    ├── docker-compose.yaml
    ├── dockerpush.sh
    ├── middleware.ts
    ├── next-env.d.ts
    ├── next.config.js
    ├── package.json
    ├── postcss.config.js
    ├── tailwind.config.js
    └── tsconfig.json
```

## Nextjs API

Next.js API routes allow you to build APIs directly within your Next.js application. They are server-side functions that can receive HTTP requests and return responses. You can use them to handle tasks like interacting with a database, handling form submissions, or even building a full-fledged API. They are created by adding JavaScript files in the app/api directory of your Next.js project.

In this project, three main endpoints are built using api routes to handle auth, chating, and pulling avlaible model tags.

### auth

### chat

### tags

## Styling
- Component Library [shadcn/ui](https://ui.shadcn.com)
- Styling with [Tailwind CSS](https://tailwindcss.com)
- [Radix UI](https://radix-ui.com) for headless component primitives
- Icons from [Phosphor Icons](https://phosphoricons.com)


## env file
Create .env file and copy contents of .env.example into .env

assign these values

``` .env
# Google Auth Credentials
AUTH_GOOGLE_ID=
AUTH_GOOGLE_SECRET=

# Secret key used for encryption in the auth module
AUTH_SECRET=

# Base URL of your backend API
URL=

# The host URL of your application
HOST=

# Base URL of your REDIS REST API
# Token for authenticating with the REDIS REST API
# check README.md in the redis directery for more information
KV_REST_API_URL=
KV_REST_API_TOKEN=

# The base URL of your Next.js application, used by NextAuth for callbacks and redirects
NEXTAUTH_URL=


# _______________ PRODUCTION ONLY _______________ #


# Proxy URL for redirecting during authentication (only needed in production)
AUTH_REDIRECT_PROXY_URL=
```


## Running Locally
### 1. run with local version of node
This method supports hot reload (no need to kill and run again when changes are made).
``` bash
npm run dev
```

### 2. run with docker

This method produces a result in the same format as used in production.
``` bash
docker compose up --build
```

## Pushing to Container Registry

Open dockerpush.sh

```bash
# set these variables
registry=""
username=""
project=""
serviceName=""
```

### What is happening under the hood?
This is an example
```bash
#!/bin/bash

# Define these variables
registry="container.cs.vt.edu"
username="saketh"
project="aginsurancellm"
serviceName="frontend"

# login to the container registry
docker login $registry

# Build the image for a linux/amd64 platform 
docker build --platform linux/amd64 -t $registry/$username/$project/$serviceName .

# Push the image
docker push $registry/$username/$project/$serviceName
```

### To execute the push to the container registry
```bash
bash dockerpush.sh
```

## Known Issues
