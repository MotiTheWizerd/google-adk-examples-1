import uuid
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import base64

load_dotenv()

client = genai.Client()

contents = ("""Hi, create an image, here is the prompt: 
    create me a thumnail for fiverr programming gig for websites, make it fun and creative make it look like a comic book, don't use the word fiverr, you can use "NextJS"including the text "Websites with NextJS!" in a stylized speech bubble or banner, making it eye-catching and playful.
            use the colors "Red,Blak, Yellow
""")

response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    image = Image.open(BytesIO((part.inline_data.data)))
    image.save(f'image_{uuid.uuid4()}.png')
    image.show()