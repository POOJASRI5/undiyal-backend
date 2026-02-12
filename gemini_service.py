import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("AIzaSyBwox9bH8iXKYCIGVmGukVplMw-nMKJupw"))
model = genai.GenerativeModel("gemini-1.5-flash-latest")

