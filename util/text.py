from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

analyzer = SentimentIntensityAnalyzer()


def clean_text(input:str):
  return re.sub(r'https?://\S+', '', input).strip()

def vader_sentiment(input:str):
  if input and len(input) > 0:
    vs = analyzer.polarity_scores(input)
    return vs['neg'], vs['neu']
  else:
    return 0, 0