import vertexai
from vertexai.generative_models import GenerativeModel, Part
vertexai.init(project="petrosa-data", location="us-central1")
import dotenv
import os

dotenv.load_dotenv()

PREFIX = os.getenv("PREFIX")
BUCKET = os.getenv("BUCKET")
SUFFIX = os.getenv("SUFFIX")

prompt = """This is the video of a candidate. 

The Job Description is as follows: Senior Data Engineer AI Studio - Video Self Interviewer JD You will work in a fast-paced environment alongside highly experienced and talented product owners, scrum masters, QA, designers & developers to analyze, architect, & build solutions based on business needs. You have an entrepreneurial mindset, like working in a team, can define and run experiments to learn what works, and like metrics to make decisions. You will work in an agile team and participate in all stages of product development, from concept to release, and subsequent iterations to react to learnings and refinements. You will contribute to the evolution of our applications and internal tooling, enabling better experiences for our customers and your teammates. About the project AI Studio is a leading digital healthcare company that creates trusted solutions that detect, predict, and prevent disease. Combining wearable biosensors and cloud-based data analytics with powerful proprietary algorithms that distill data from millions of heartbeats into clinically actionable information. We are seeking a talented Data Engineer to join our team. The ideal candidate will have a strong background in data engineering with expertise in DBT, Snowflake, Argo workflows, and Fivetran. You will play a key role in designing, building, and maintaining our data infrastructure to support our analytics and business intelligence initiatives. Main Tasks ● Design and implement data pipelines using DBT for transformation and modeling. ● Manage and optimize data warehouse solutions on Snowflake. ● Develop and maintain ETL processes using Fivetran for data ingestion. ● Utilize Terraform for infrastructure as code (IaC) to provision and manage resources in AWS, Snowflake, Kubernetes, and Fivetran. ● Collaborate with cross-functional teams to understand data requirements and deliver scalable solutions. ● Implement workflow automation using Argoworkflows to streamline data processing tasks. ● Ensure data quality and integrity throughout the data lifecycle.

Answer the following questions based on the video, and repeat the questions in the answer.

Describe the candidate in the video and his appeareance. 
Quality of the english of the candidate. (1-10, where 1 is the worst and 10 is the best)
Is the candidate a good fit for the job? 
Is the candidate good and articulate in describing his career?
Should the candidate proceed to the next steps?


"""


vision_model = GenerativeModel("gemini-1.5-flash-002")

# Generate text
response = vision_model.generate_content(
    [
        Part.from_uri(
            f"{PREFIX}{BUCKET}/imageToSave.webm", mime_type="video/webm"
        ),
       prompt,
    ]
)
print(response.text)
