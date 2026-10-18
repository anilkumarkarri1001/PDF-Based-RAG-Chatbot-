Steps to generate your API key : 

Step 1: Open Google AI Studio
Click the link below.
Open Gemini API Keys   : https://aistudio.google.com/app/api-keys?utm_source=chatgpt.com

Step 2: Sign in
Sign in with your Google/Gmail account.

Step 3: Click Create API key
If asked, select an existing project or create a new one.

Step 4: Copy your API key
Click the Copy button and keep the key private. 
Google AI for Developers
+1

Step 5: Add the key to your FastAPI project
Open your project's .env file and add:
GEMINI_API_KEY=paste_your_actual_api_key_here

=======================================================>
PS C:\Users\DELL\Downloads\fastapi-rag-gemini> python -m venv rag_env
PS C:\Users\DELL\Downloads\fastapi-rag-gemini> .\rag_env\Scripts\Activate.ps1
(rag_env) PS C:\Users\DELL\Downloads\fastapi-rag-gemini> pip install -r requirements.txt       



how to run the flask/fastapi server : 


(rag_env) PS C:\Users\DELL\Downloads\fastapi-rag-gemini> python -m uvicorn main:app

  import google.generativeai as genai
INFO:     Started server process [31020]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:53513 - "GET / HTTP/1.1" 200 OK

=> to generate the swagger file for the fastapi server :
http://127.0.0.1:8000/docs



1. Save installed packages to requirements.txt
pip freeze > requirements.txt
Meaning:
- pip freeze — lists installed Python packages and their versions.
- > — writes the output into a file.
- requirements.txt — the file where dependencies are saved.


=======================================================>
installed lib.s :

fastapi
uvicorn
python-dotenv
pydantic
chromadb
pypdf
python-multipart
google-generativeai


1. Purpose of each module in your RAG chatbot
Module	Why you used it
fastapi	Creates API endpoints for uploading HR policy documents and asking questions.
uvicorn	Runs your FastAPI application as a web server.
python-dotenv	Loads environment variables, such as your Gemini API key, from a .env file.
pydantic	Validates request data and defines structured input and output schemas.
chromadb	Stores document embeddings and retrieves relevant document chunks using similarity search.
pypdf	Extracts text from uploaded PDF HR policy documents.
python-multipart	Allows FastAPI to receive uploaded files through multipart form data.
google-generativeai	Provides the Google Gemini SDK for generating answers from the retrieved HR policy context.
=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>
sequence diagram for the RAG chatbot workflow:


@startuml
title RAG Chatbot - Sequence Diagram

actor User
participant "FastAPI" as API
participant "Upload / Ask Router" as Router
participant "PDF Parser" as PDF
participant "Gemini Embedding API" as Embedding
database "ChromaDB" as DB
participant "Gemini LLM" as LLM

== Document Upload ==
User -> API : POST /upload (PDF)
API -> Router : Forward request
Router -> PDF : Extract text
PDF --> Router : Extracted text
Router -> Router : Split text into chunks

loop For each chunk
  Router -> Embedding : Generate chunk embedding
  Embedding --> Router : Vector
  Router -> DB : Store chunk + vector + metadata
  DB --> Router : Storage result
end

Router --> User : Upload result

== Ask a Question ==
User -> API : POST /ask (question)
API -> Router : Forward request
Router -> Embedding : Embed question
Embedding --> Router : Question vector
Router -> DB : Search similar vectors
DB --> Router : Top matching chunks
Router -> LLM : Prompt with context + question
LLM --> Router : Generated answer
Router --> User : JSON answer

@enduml
  
=======================================================>
system architecture diagram for the RAG chatbot workflow:


@startuml
title PDF RAG Chatbot - System Architecture

actor User

rectangle "FastAPI Application" {
  component "main.py" as Main
  component "upload.py\nUpload Router" as Upload
  component "ask.py\nQuestion Router" as Ask
}

database "ChromaDB\nPersistent Vector Store" as DB
cloud "Gemini Embedding API" as Embed
cloud "Gemini Generative Model" as LLM
folder "uploads/\nPDF Files" as Files
folder "chroma_db/\nPersistent Data" as Storage

User --> Main : HTTP request
Main --> Upload : POST /upload
Main --> Ask : POST /ask

Upload --> Files : Save uploaded PDF
Upload --> Embed : Embed document chunks
Upload --> DB : Store chunks + vectors + metadata
DB --> Storage : Persist collection data

Ask --> Embed : Embed question
Ask --> DB : Similarity search
DB --> Ask : Top matching chunks
Ask --> LLM : Question + retrieved context
LLM --> Ask : Generated answer
Ask --> User : JSON response

note right of DB
Stores vectors and text
for semantic retrieval
end note

@enduml
  
=======================================================>
pdf upload flow : 


@startuml
title PDF Upload and Indexing Flow
start

:User sends PDF to POST /upload;
:FastAPI receives UploadFile;

if (Filename ends with .pdf?) then (Yes)
  :Save PDF under uploads/;
  :Read PDF using PdfReader;
  :Extract text from pages;

  if (Text extracted?) then (Yes)
    :Split text into overlapping chunks;

    while (More chunks?) is (Yes)
      :Generate embedding using Gemini;
      :Store chunk, vector, UUID and filename\nin ChromaDB;
    endwhile (No)

    :Return success message and chunk count;
  else (No)
    :Return meaningful error or\nno-readable-text response;
  endif

else (No)
  :Return HTTP 400;
endif

stop
@enduml

=======================================================>

Diagram 3 — Question-answering flow : 

@startuml
title RAG Question Answering Flow
start

:User submits question to POST /ask;
:Validate request with Pydantic;
:Generate question embedding using Gemini;
:Search ChromaDB for top 3 similar chunks;

if (Relevant chunks found?) then (Yes)
  :Combine retrieved chunks into context;
  :Build prompt with context and question;
  :Send prompt to Gemini generative model;
  :Receive generated answer;
  :Return question and answer as JSON;
else (No)
  :Return a safe "information not found"\nresponse;
endif

stop
@enduml

=======================================================>
Example: HR policies chatbot
Suppose an HR employee uploads leave_policy.pdf and asks, “How many casual leaves can an employee take?”
Stage	Example input	Example output
Upload	leave_policy.pdf	File accepted
Extraction	PDF pages	Policy text
Chunking	Policy text	Smaller text sections
Embedding	One text section	Numerical vector
Storage	Chunk + vector	Indexed record in ChromaDB
Retrieval	Employee's question vector	Three matching chunks at most
Generation	Chunks + question	Answer grounded in retrieved text
Response	Generated answer	JSON returned to client
The actual answer depends on the uploaded policy. The system should not invent a number of leave days if the document does not specify one.
3. Explain the project in a backend interview
Here is a sample answer you can practice. Use “I implemented” only for features you have actually built and tested.
60–90 second project explanation
Interview-ready answer
“I developed a PDF-based Retrieval-Augmented Generation chatbot using FastAPI, ChromaDB, and Google's Gemini APIs.
The main objective was to allow users to ask questions about documents, such as HR policies, without manually searching through entire PDFs.
I divided the backend into two main APIs. The first is the document-upload API. It accepts a PDF, extracts text using PyPDF, splits the text into overlapping chunks, generates embeddings using Gemini, and stores the chunks, vectors, and metadata in ChromaDB.
The second is the question-answering API. It converts the user's question into an embedding, retrieves the three most similar chunks from ChromaDB, and passes the retrieved context and question to Gemini's generative model. The generated answer is then returned as JSON.
I used FastAPI for REST APIs, Pydantic for request validation, ChromaDB for semantic search, and persistent local storage so the indexed data can be reused after a server restart.
Important areas for improvement include robust file validation, duplicate-upload handling, API timeouts and retries, retrieval relevance checks, secure file storage, and better observability.”
How to describe your responsibilities
Be ready to explain these five things clearly:
- Business problem: Finding specific information in long PDF documents is time-consuming.
- Backend design: Separate upload and question-answering routers.
- Data flow: PDF → extracted text → chunks → embeddings → ChromaDB → retrieval → Gemini answer.
- Technology choices: FastAPI for endpoints, ChromaDB for vector search, and Gemini for embeddings and generation.
- Trade-offs: External API latency and cost, retrieval quality, file size, document parsing limitations, and privacy.
Important terminology
Term	Simple interview explanation
RAG	Retrieves relevant information and gives it to an LLM to help generate an answer.
Embedding	A numerical representation of text meaning.
Vector database	Stores and searches vectors, often to find semantically similar text.
Chunking	Splitting a document into smaller text sections.
Chunk overlap	Repeating some text between adjacent chunks to preserve context across boundaries.
Semantic search	Finding text by meaning rather than only exact keyword matches.
Grounding	Using retrieved evidence to constrain the answer.
Persistent storage	Data remains available across application restarts, assuming the stored files are retained.
4. Interview questions and answers — backend engineer, around 2 years
Practice explaining the reasoning behind your decisions, not just memorizing definitions.
A. Architecture and fundamentals
Q1. Why did you use FastAPI?
FastAPI lets me build REST APIs using Python, supports request validation through Pydantic, and generates OpenAPI documentation automatically. It also supports asynchronous endpoints when I need non-blocking I/O.
Q2. Why did you split the code into main.py, upload.py, and ask.py?
main.py initializes the application and registers the routers. upload.py handles document ingestion, while ask.py handles retrieval and answer generation. This separation improves maintainability, testability, and separation of responsibilities.
Q3. Why use RAG instead of sending the whole PDF directly to Gemini?
RAG retrieves only relevant sections instead of sending an entire document for every question. This can reduce prompt size, cost, and latency while helping ground answers in the document. It also makes it easier to work with documents that exceed the model's practical context budget.
Q4. Why do you need a vector database? Why not a normal database?
A relational database is excellent for structured records and exact filtering. A vector database supports similarity search over embeddings. For example, a question about “time away from work” may retrieve a chunk discussing “leave policy” even when the exact words differ.
Q5. Why do you store both the text chunk and its embedding?
The embedding supports similarity search. The original text is needed as readable context for the LLM. Metadata such as the filename helps identify where the retrieved content came from.
Q6. What is the purpose of chunk overlap?
If a relevant sentence or rule is split at the end of one chunk and the beginning of another, overlap helps preserve surrounding context. In my implementation, the chunk size is 1,000 characters and the overlap is 200 characters.
Q7. Why use Gemini twice?
These are two different tasks. The embedding model converts text into vectors for retrieval. The generative model uses the question and retrieved text to produce a natural-language answer.
Q8. Why does /ask retrieve three chunks?
n_results=3 limits the number of retrieved results requested from ChromaDB. Three is a starting configuration, not a universally optimal value. I would evaluate retrieval quality and response quality on representative questions before choosing the final number.
Q9. What is the purpose of Pydantic in your project?
QuestionRequest validates the incoming JSON body and ensures that the question field has the expected type. I would add validation for empty strings, maximum length, and whitespace-only questions.
Example
from pydantic import BaseModel, Fieldclass QuestionRequest(BaseModel):    question: str = Field(        min_length=1,        max_length=2000    )
For a production API, you can also reject whitespace-only values with a field validator.
Q11. What is the purpose of HTTPException?
It lets the API return a meaningful HTTP error status and message. For example, an unsupported file type can produce HTTP 400 rather than an unexplained server error.
Q12. What happens when the FastAPI server restarts?
ChromaDB is configured with PersistentClient(path="chroma_db"), so its stored collection data can survive a normal restart if the directory remains intact. However, the uploaded files and database still need appropriate backups, access controls, and deployment storage.
“ChromaDB ని PersistentClient(path="chroma_db") తో configure చేశారు. కాబట్టి, chroma_db అనే folder అలాగే ఉంటే, application ని సాధారణంగా stop చేసి మళ్లీ start చేసినా, అందులో save చేసిన collection data అలాగే ఉంటుంది.”   
Edge case 3: What if the retrieved chunks do not contain the answer?
The current prompt tells Gemini to say the information is unavailable, but a prompt instruction alone cannot guarantee that the model will always abstain correctly.
Edge case 4: What if two users upload policy.pdf?
Your current implementation saves files using file.filename. Two uploads with the same name can overwrite the same file. Your database metadata also contains only the filename, not a user ID or unique document ID.
Edge case 5: What if the API is slow?
The request can involve an embedding API call, a vector database search, and a generation API call. Network latency or rate limits may dominate response time.
Better approach:
- Set appropriate timeouts for external API calls.
- Retry only transient failures and only a limited number of times.
7. More advanced questions to practice
These are questions where a strong answer explains a trade-off, not just a definition.
Q: How would you support multiple documents and let users select one?
Answer: Assign every document a unique ID and associate it with an owner or tenant. Store identifiers in ChromaDB metadata, and filter queries to the documents the user is allowed to access. For a document-specific question, include its document ID in the retrieval filter.
=======================================================>

=======================================================>



testing pdf content : 

# ABC Technologies Pvt. Ltd.
## Employee Handbook — HR Policies
**Document ID:** HR-POL-001  
**Version:** 1.0  
**Effective Date:** 1 January 2026  
**Document Type:** Sample Testing Document

**Important:** ABC Technologies Pvt. Ltd. and all policies in this document are fictional. This document is intended only for software testing and does not represent an actual company's policies.

---

## 1. Working Hours and Attendance Policy

### 1.1 Standard Working Hours
The standard working hours for full-time employees are 9:30 AM to 6:30 PM, Monday through Friday.

Employees are expected to complete eight working hours per day, excluding a one-hour lunch break.

### 1.2 Attendance
Employees must record their attendance through the company's attendance management system.

Employees who arrive more than 15 minutes after their scheduled start time must inform their reporting manager.

### 1.3 Remote Work
Employees may work remotely up to two days per week with prior approval from their reporting manager.

Remote work approval depends on project requirements and business needs.

---

## 2. Leave Policy

### 2.1 Casual Leave
Every eligible full-time employee receives 12 casual leave days per calendar year.

Casual leave should generally be requested at least two working days in advance.

### 2.2 Sick Leave
Every eligible full-time employee receives 10 sick leave days per calendar year.

Employees may be asked to provide a medical certificate if sick leave exceeds three consecutive working days.

### 2.3 Earned Leave
Eligible employees receive 15 earned leave days per calendar year.

Earned leave requests should generally be submitted at least seven working days before the intended leave date and require manager approval.

### 2.4 Public Holidays
The company observes 10 public holidays per calendar year.

The HR department publishes the holiday calendar at the beginning of each calendar year.

### 2.5 Leave Approval
All planned leave requests must be submitted through the company's leave management system.

Approval depends on the employee's available leave balance, project requirements, and manager authorization.

---

## 3. Salary and Payroll Policy

### 3.1 Salary Payment Date
Employee salaries are paid on the last working day of each calendar month.

If the last working day is affected by a banking holiday or operational issue, HR and Finance will communicate the revised payment date.

### 3.2 Payslips
Employees can access their monthly payslips through the employee self-service portal.

Payslips contain salary components and applicable deductions.

### 3.3 Salary Deductions
Applicable deductions may include statutory deductions, employee-authorized deductions, and deductions permitted under company policy and applicable law.

Employees should contact the Payroll team if they identify an error in their payslip.

---

## 4. Probation and Confirmation Policy

### 4.1 Probation Period
New employees are subject to a probation period of six months from their joining date.

### 4.2 Performance Review
The reporting manager evaluates employee performance, attendance, conduct, and role-specific objectives during probation.

### 4.3 Confirmation
Successful completion of probation is subject to satisfactory performance and written confirmation from HR.

If additional evaluation is required, HR may communicate an extension in accordance with the employee's employment terms and applicable law.

---

## 5. Code of Conduct Policy

### 5.1 Professional Behavior
Employees must maintain professional behavior and treat colleagues, customers, and business partners respectfully.

### 5.2 Harassment and Discrimination
The company prohibits workplace harassment, bullying, and unlawful discrimination.

Employees may report concerns to HR or the designated grievance-handling authority.

### 5.3 Confidentiality
Employees must protect confidential company information, customer information, credentials, and business records.

Confidential information must not be disclosed to unauthorized individuals.

### 5.4 Company Equipment
Company laptops, devices, accounts, and other equipment must be used responsibly and protected from unauthorized access.

Employees must report lost devices or suspected security incidents promptly.

---

## 6. Work-from-Home Policy

### 6.1 Eligibility
Employees may request remote work subject to role suitability, project requirements, and manager approval.

### 6.2 Availability
Employees working remotely must remain available during their agreed working hours and attend scheduled meetings.

### 6.3 Data Security
Employees must use approved company systems and follow company security requirements when accessing company information remotely.

Sensitive company information must not be stored on unauthorized personal devices or shared through unapproved services.

---

## 7. Resignation and Notice Period Policy

### 7.1 Notice Period
The standard notice period for permanent employees is 60 calendar days, subject to the employee's employment agreement and applicable law.

### 7.2 Resignation Submission
Employees must submit their resignation in writing to their reporting manager and HR.

### 7.3 Handover
Before leaving the company, employees must complete the assigned knowledge transfer, return company property, and hand over relevant work and documentation.

### 7.4 Exit Formalities
HR coordinates exit formalities and the final settlement process in accordance with company policy and applicable law.

---

## 8. Employee Grievance Policy

### 8.1 Raising a Grievance
Employees may submit workplace concerns or grievances to HR through the designated email channel or employee grievance portal.

### 8.2 Acknowledgment
HR aims to acknowledge a grievance within two working days.

### 8.3 Resolution
HR aims to provide an initial update within seven working days. Complex cases may require additional investigation and time.

### 8.4 Confidentiality
Grievances will be handled with appropriate confidentiality, subject to the requirements of a fair investigation and applicable law.

---

## 9. Learning and Development Policy

### 9.1 Training
Employees may participate in company-approved training programs related to their role and professional development.

### 9.2 Training Approval
Training requests require manager approval and depend on the available budget and business priorities.

### 9.3 Knowledge Sharing
Employees are encouraged to share relevant learning with their teams through presentations, documentation, or technical discussions.

---

## 10. IT and Information Security Policy

### 10.1 Password Security
Employees must use strong passwords and must not share their passwords with other people.

### 10.2 Multi-Factor Authentication
Employees must enable multi-factor authentication on company accounts wherever it is supported and required by company policy.

### 10.3 Security Incidents
Suspected phishing emails, unauthorized access, malware infections, or data leaks must be reported promptly to the IT or Security team.

### 10.4 Access Control
Access to company systems must be limited to authorized users and the permissions required for their job responsibilities.

---

## End of Document

**Document ID:** HR-POL-001  
**Version:** 1.0  
**Purpose:** Testing PDF extraction, text chunking, embedding generation, vector retrieval, and question answering in a RAG chatbot.
=======================================================>
testing questions : 

Question: How many casual leave days does an eligible employee receive per year?
Expected answer: An eligible full-time employee receives 12 casual leave days per calendar year.
Tests leave-policy retrieval



2

Question: What are the standard working hours?
Expected answer: 9:30 AM to 6:30 PM, Monday through Friday, with eight working hours excluding a one-hour lunch break.
Tests factual retrieval



3

Question: What is the notice period for permanent employees?
Expected answer: The standard notice period is 60 calendar days, subject to the employee's employment agreement and applicable law.
Tests a separate policy section



4

Question: When should HR acknowledge an employee grievance?
Expected answer: HR aims to acknowledge a grievance within two working days.
Tests a specific deadline



5

Question: How many paid annual leave days are provided in total across casual, sick, and earned leave?
Expected answer: 37 days in total: 12 casual leave days + 10 sick leave days + 15 earned leave days per calendar year for an eligible
=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>

=======================================================>