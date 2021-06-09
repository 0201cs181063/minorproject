from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import pickle



summarizer = pipeline('summarization')

pickle.dump(summarizer, open('sum.pkl', 'wb'))

