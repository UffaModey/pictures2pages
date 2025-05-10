# Use the AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR /var/task

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --target . -r requirements.txt

# Copy your Lambda function
COPY pictures2pages_lambda.py .

# Set the Lambda function handler
CMD ["pictures2pages_lambda.generate_content"]
