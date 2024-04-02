import { Toaster } from 'react-hot-toast'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'

import '@/app/globals.css'
import { cn } from '@/lib/utils'
import { TailwindIndicator } from '@/components/tailwind-indicator'
import { Providers } from '@/components/providers'
import { Header } from '@/components/header'
import { SessionProvider } from 'next-auth/react'
import { auth } from '@/auth'

export const metadata = {
  metadataBase: new URL(`https://${process.env.HOST}`),
  title: {
    default: 'Agricultural Insurance LLM Project',
    // template: `%s - Next.js AI Chatbot`
  },
  description:
    'An  interactive conversational assistant to improve agricultural insurance selection.',
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png'
  }
}

export const viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: 'white' },
    { media: '(prefers-color-scheme: dark)', color: 'black' }
  ]
}

interface RootLayoutProps {
  children: React.ReactNode
}

export default async function RootLayout({ children }: RootLayoutProps) {
  const session = await auth()

  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn(
          'font-sans antialiased',
          GeistSans.variable,
          GeistMono.variable
        )}
      >
        <Toaster />
        <Providers
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="flex flex-col min-h-screen">
            <Header />
            <SessionProvider session={session}>
            <main className="flex flex-col flex-1 bg-muted/50">{children}</main>
            </SessionProvider>
          </div>
          <TailwindIndicator />
        </Providers>
      </body>
    </html>
  )
}
