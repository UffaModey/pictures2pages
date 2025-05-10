# 🖼️ Picture2Pages API
**Turn images into imaginative short stories or poems using AI.**  
This project combines computer vision and natural language generation to demonstrate how artificial intelligence can be used creatively in real-world applications. Built on AWS, it uses image analysis with Rekognition and language generation with OpenAI’s GPT model.

---

## 🚀 Core Learning Goals

- Understand how **Computer Vision** (CV) is used to extract meaningful insights from images.
- Apply **Text Generation** using a large language model (LLM) to turn image descriptions into creative outputs.
- Explore how to integrate multiple AI services using **cloud-native tools** like AWS Lambda and S3.
- Practice **prompt engineering** to shape the outputs of generative AI.
- Gain hands-on experience with **serverless deployment** and containerized Lambda functions.
- Learn how to connect AI services via a **RESTful API** using AWS API Gateway.

---

## 🧰 Tech Stack

| Component        | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **AWS Lambda**   | Executes the backend Python code using serverless compute.                  |
| **AWS S3**       | Stores user-uploaded images for analysis.                                   |
| **AWS Rekognition** | Detects objects, scenes, and other features in the images.               |
| **AWS ECR**      | Hosts a containerized Lambda function with custom dependencies.             |
| **OpenAI GPT-3.5 Turbo** | Generates a short story or poem based on image captions.            |
| **AWS API Gateway** | Exposes the API endpoint for receiving uploads and returning content.   |
| **Python**       | Primary backend language for orchestration and service integration.         |

---

## 🛠️ How It Works

1. **User uploads three images** via a frontend or `multipart/form-data` request.
2. The images are uploaded to **Amazon S3** with unique filenames.
3. **AWS Rekognition** analyzes each image and returns high-confidence labels.
4. The image labels are combined and used to prompt **OpenAI’s GPT-3.5 Turbo** to generate a story or poem.
5. The final result is returned to the user as a JSON object with a title and content.

---

## 📦 Installation & Deployment

> 💡 Recommended: Use [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) or Docker for local development.

### Prerequisites
- Python 3.11+
- Docker (for container build)
- AWS CLI & credentials configured
- OpenAI API key

### 1. Clone the repository
```bash
git clone https://github.com/UffaModey/pictures2pages
cd picture2pages
```
### 2. Build the Lambda Docker Image
``` bash
docker build -t picture2pages .
```


### 3. Test Locally (Optional)
``` bash
./local_lambda_deploy
``` 

### 4. Deploy to AWS Lambda
``` bash
./ecr_lambda_deploy
``` 
### 🧩 How to Build on This Project
1. 🔤 Add multilingual support using translation APIs
2. ✨ Use image captions instead of just labels to generate richer prompts
3. 🖼️ Implement a frontend UI with drag-and-drop upload support
4. 📊 Add feedback scoring to assess and improve generation quality
5. 📚 Include prompt templates for themes like sci-fi, romance, or humor

### 👩🏾‍💻 Created by
- Fafa Modey
- Software Engineer | Digital Rights Advocate | AI Educator
