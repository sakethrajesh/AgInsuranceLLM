export async function GET() {

  const response = await fetch(
    'https://ollamaaginsurance.endeavour.cs.vt.edu/api/tags'
  )

  return response
}
