export async function GET() {

  const response = await fetch(
    'https://ollamaaginsurance.endeavour.cs.vt.edu/api/tags', 
    { cache: 'no-store' }
  )

  const data = await response

  return data
}
