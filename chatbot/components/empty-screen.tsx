import { useEffect, useState } from 'react'
import { UseChatHelpers } from 'ai/react'

import { Button } from '@/components/ui/button'
import { ExternalLink } from '@/components/external-link'
import { IconArrowRight, IconExternalLink } from '@/components/ui/icons'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue
} from './ui/select'

const exampleMessages = [
  {
    heading: 'See how you can enroll',
    message: 'How can I enroll in the PRF insurance program for my land?'
  },
  {
    heading: 'Find upcoming deadlines',
    message:
      'What is the deadline for purchasing PRF insurance for the upcoming season?'
  },
  {
    heading: 'Look up definitions for terms',
    message: `What does the acronym PRF-RI mean?`
  }
]

export function EmptyScreen({
  setModel,
  setInput
}: {
  setModel: any
  setInput: any
}) {
  const [models, setModels] = useState<{ name: string }[]>([])

  useEffect(() => {
    const fetchModels = async () => {
      const response = await fetch('/api/tags')
      const data = await response.json() // Parse the response as JSON
      setModels(data.models) // Access the 'models' property from the parsed JSON
      console.log(data.models)
    }

    fetchModels()
  }, [])

  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="rounded-lg border bg-background p-8">
        <h1 className="mb-2 text-lg font-semibold">
          Agricultural Insurance LLM Project
        </h1>
        <p className="mb-2 leading-normal text-muted-foreground">
          This is an interactive conversational assistant to improve
          agricultural insurance selection, with large language models (LLMs).
        </p>
        <p className="leading-normal text-muted-foreground">
          You can start a conversation here or try the following examples:
        </p>
        <div className="mt-4 flex flex-col items-start space-y-2">
          {exampleMessages.map((message, index) => (
            <Button
              key={index}
              variant="link"
              className="h-auto p-0 text-base"
              onClick={() => setInput(message.message)}
            >
              <IconArrowRight className="mr-2 text-muted-foreground" />
              {message.heading}
            </Button>
          ))}
        </div>
        <div className="mt-4 flex items-center justify-between">
          <Select
            onValueChange={value => {
              setModel(value)
            }}
            defaultValue={'llama2:chat'}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select a model" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Models</SelectLabel>
                {models.map((model, index) => (
                  <SelectItem key={index} value={model.name}>
                    {model.name}
                  </SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        {/* <div className="mt-4 flex items-center justify-between">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="pl-0">
                <h2 className="mb-2 text-lg font-semibold">
                  Choose a model: {' '}
                  {models.length > 0 ? models[0].name : 'Default Model'}
                </h2>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              sideOffset={8}
              align="start"
              className="w-[180px]"
            >
              {models.map((model, index) => (
                <DropdownMenuItem key={index}>
                  <div className="text-xs font-medium">
                    <p>{model.name}</p>
                  </div>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        </div> */}
      </div>
    </div>
  )
}
