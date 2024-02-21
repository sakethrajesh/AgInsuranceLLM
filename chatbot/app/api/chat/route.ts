import { kv } from '@vercel/kv'
import { Message, StreamingTextResponse } from "ai";
import { auth } from '@/auth'
import { nanoid } from '@/lib/utils'


export async function POST2(req: Request) {

  const json = await req.json()
  const URL = process.env.URL;
  
  const response = await fetch(`${URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ messages: json["messages"] })
  });

  if (response.ok) {
    const data = await response.json();
    return new Response(data["text"], { status: 200 })

  } else {
    return new Response("There was an error", { status: 500 })

  }

}

export async function POST(req: Request) {
  const { messages }: { messages: Message[] } = await req.json();
  const URL = process.env.URL;
  const response = await fetch(`${URL}/api/stream_chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ messages: messages })
  }); 

    if (response.ok) {
      let reader = response.body?.getReader();
    
      let decoder = new TextDecoder();

      return new Response(new ReadableStream({
        async start(controller) {
          let buffer = '';
          while (true && reader !== undefined) {
              const { done, value } = await reader.read();
              if (done) break;
              let chunk = decoder.decode(value, { stream: true });
              try {
                    //console.log("Chunk:", chunk);
                    chunk.split("\n").forEach((line) => {
                      if(line.trim().length > 0)
                      {
                        //console.log("Line:", line);
                        const json = JSON.parse(line);
                        if (json && json.text && json.text.length > 0) {
                            buffer += json.text; 
                        }
                      }
                    });
                
              } catch (error) {
                  //console.log("Error Chunk:", chunk);
                  console.error('Error parsing JSON chunk', error);
              }
              if (buffer.length > 20) { // Threshold can adjusted for more responsiveness
                  controller.enqueue(buffer);
                  buffer = '';
              }
          }
          if (buffer.length > 0) {
              controller.enqueue(buffer); // complete leftover buffer
          }
          controller.close();
          reader?.releaseLock();
      } 
      }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  } else {
      return new Response("Error:", { status: 500 });
  }

}
// const openai = new OpenAI({
//   apiKey: process.env.OPENAI_API_KEY
// })

// export async function POST2 (req: Request) {
//   const json = await req.json()
//   const { messages, previewToken } = json
//   const userId = (await auth())?.user.id

//   if (!userId) {
//     return new Response('Unauthorized', {
//       status: 401
//     })
//   }

//   const stream = OllamaStream(res, {
//     async onCompletion(completion) {
//       const title = json.messages[0].content.substring(0, 100)
//       const id = json.id ?? nanoid()
//       const createdAt = Date.now()
//       const path = `/chat/${id}`
//       const headers = {
//         'Content-Type': 'application/json'
//       };
//       const res = fetch('https://api.openai.com/v1/engines/davinci-codex/completions', 
      
//       body: JSON.stringify({
//         model: 'gpt-3.5-turbo',
//         messages,
//       }));

//       const payload = {
//         id,
//         title,
//         userId,
//         createdAt,
//         path,
//         messages: [
//           ...messages,
//           {
//             content: completion,
//             role: 'assistant'
//           }
//         ]
//       }
//       await kv.hmset(`chat:${id}`, payload)
//       await kv.zadd(`user:chat:${userId}`, {
//         score: createdAt,
//         member: `chat:${id}`
//       })
//     }
//   })  

// }

