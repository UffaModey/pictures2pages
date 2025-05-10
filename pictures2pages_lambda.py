import openai
import boto3
import requests
from openai import OpenAI
import re
import uuid
import base64
import os

# Set API keys and secrets using environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

s3_bucket = os.getenv("S3_BUCKET")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

response = requests.get("https://www.google.com")
print(f"test internet access: {response.status_code}")


def upload_image_to_s3(image_base64, bucket_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name="eu-west-2",
    )

    image_data = base64.b64decode(image_base64)
    filename = f"{uuid.uuid4()}.jpg"

    try:
        s3.put_object(
            Bucket=bucket_name, Key=filename, Body=image_data, ContentType="image/jpeg"
        )
        return filename
    except Exception as e:
        raise Exception(f"Error uploading to S3: {str(e)}")


def get_caption_for_image(filename, bucket_name):
    client = boto3.client(
        "rekognition",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name="eu-west-2",
    )

    try:
        response = client.detect_labels(
            Image={"S3Object": {"Bucket": bucket_name, "Name": filename}},
            MaxLabels=10,
        )
        print("Detected labels for " + filename)
        print()
        labels = response["Labels"]
        label_name_list = []
        for label in labels:
            label_name_list.append(label["Name"])
            print("Label: " + label["Name"])
            print("Confidence: " + str(label["Confidence"]))
        return label_name_list
    except Exception as e:
        return {"statusCode": 500, "error": str(e)}


def generate_content_from_image_labels(
    caption_1, caption_2, caption_3, theme=None, type="story"
):
    client = OpenAI(api_key=openai.api_key)
    print("Generating content from labels")

    theme_text = f" Write it in the theme of '{theme}'." if theme else ""

    prompt = (
        f"Write a short {type} of no more than 50 words that includes these elements: "
        f"{caption_1}, {caption_2}, and {caption_3}.{theme_text} "
        f"Generate a title for the {type} in 5 words or less."
    )

    try:
        career = "poet" if type == "poem" else "author"
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a children's {career} skilled in adventure, fantasy, "
                    "and emotional creative writing for ages 8 to 16.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        generated_content = completion.choices[0].message.content
        print("Content generated from openAI API")

        # Use regex to extract title and body reliably
        title_match = re.search(r"^Title:\s*(.*)", generated_content)
        title = title_match.group(1).strip() if title_match else f"Untitled {type}"

        # Remove the title line from content
        content = re.sub(r"^Title:.*\n?", "", generated_content).strip()

        return {"title": title, f"{type}": content}

    except Exception as e:
        return {"statusCode": 500, "error": str(e)}


def generate_content(event, context):

    try:
        image_data_1 = event["image_1"]
        image_data_2 = event["image_2"]
        image_data_3 = event["image_3"]
        theme = event.get("theme")  # Optional
        content_type = event.get("type", "story").lower()  # Can be 'story' or 'poem'

        print("Uploading images to S3")
        # Upload images to S3
        filename_1 = upload_image_to_s3(image_data_1, s3_bucket)
        filename_2 = upload_image_to_s3(image_data_2, s3_bucket)
        filename_3 = upload_image_to_s3(image_data_3, s3_bucket)

        print("Generating captions using Rekognition...")
        # Get captions
        caption_1 = get_caption_for_image(filename_1, s3_bucket)
        caption_2 = get_caption_for_image(filename_2, s3_bucket)
        caption_3 = get_caption_for_image(filename_3, s3_bucket)

        print(f"Captions:\n1: {caption_1}\n2: {caption_2}\n3: {caption_3}")

        result = generate_content_from_image_labels(
            caption_1, caption_2, caption_3, theme=theme, type=content_type
        )
        print("Successfully generated the story")
        return {"statusCode": 200, "body": result}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
