# AWS S3 Operations Manager

A professional command-line tool for managing AWS S3 buckets and objects, built as part of interview preparation for a Systems Engineering role at Elsevier.

## 🎯 Project Goals

This project was developed as **Day 1** of a comprehensive 5-day interview preparation plan, with the following objectives:

### **Learning Objectives:**

- Learn cloud computing fundamentals and core AWS services
- Gain hands-on experience with AWS S3 through practical automation
- Strengthen Python scripting skills with proper error handling
- Create a demonstrable project showcasing skills with AWS
- Build confidence with AWS APIs

### **Technical Goals:**

- Implement complete CRUD operations for S3 bucket management
- Design an intuitive command-line interface for non-technical users
- Apply development best practices (type hints, documentation, logging)

## 📚 Learning Reflection

Day one provided a solid foundation in cloud technologies. Key accomplishments included:

**Cloud Computing Fundamentals:**

- Gained solid understanding of essential cloud concepts including auto-scaling and pay-as-you-go pricing models
- Understanding the transition from CapEx to OpEx in infrastructure management
- Learned about different cloud service models (IaaS, PaaS, SaaS)

**AWS Core Services:**

- **EC2**: Virtual servers and auto-scaling for handling traffic spikes
- **S3**: Object storage with lifecycle policies and security features
- **IAM**: Identity and access management with least privilege principles
- **VPC**: Virtual private clouds for network isolation and security
- **Lambda**: Serverless computing for event-driven architectures

**Practical Implementation:**

- Successfully built a comprehensive S3 management tool with full CRUD operations
- Implemented strong error handling, logging, and user interface design

The hands-on development experience reinforced theoretical concepts.

## ✨ Features

### **Complete S3 Bucket Operations:**

- **Create buckets** with automatic unique naming
- **List all buckets** in your AWS account
- **Delete buckets** (automatically handles object cleanup)
- **View bucket contents** with organized display

### **Smart File Management:**

- **Upload files** with automatic organization by type:
  - Documents (`.doc`, `.docx`) → `docs/` folder
  - Text files (`.txt`) → `texts/` folder
  - PDFs (`.pdf`) → `pdfs/` folder
- **Delete individual objects** from buckets
- **File validation** and error handling

### **User-friendly Interface:**

- **Interactive CLI menu** using questionary library
- **User-friendly prompts** and error messages
- **Comprehensive logging** to `aws.log` file
- **Graceful error recovery** with retry options

## 🚀 Installation

### **Prerequisites:**

- Python 3.7+ installed
- AWS account with S3 permissions
- AWS credentials configured (`aws configure`)

### **Setup:**

```bash
# Clone or download the project files
cd aws-S3-script

# Install dependencies
pip install -r requirements.txt

# Ensure AWS credentials are configured
aws configure
```

## 📖 Usage

### **Quick Start:**

```bash
python s3_operations.py (python3 if on mac)
```

### **Interactive Menu:**

The tool provides an intuitive menu interface:

```
Welcome to AWS S3 Operations Manager!
-------------------------------------
? What would you like to do?
❯ View all buckets
  Create new bucket
  Upload file
  View bucket contents
  Delete object
  Delete bucket
  Exit
```

### **Example Workflows:**

**1. Create and Upload:**

- Select "Create new bucket"
- Select "Upload file"
- Choose your new bucket and specify file path
- Files are automatically organized by type

**2. Manage Existing Buckets:**

- Select "View all buckets" to see your S3 resources
- Select "View bucket contents" to explore files
- Select "Delete object" to remove specific files
- Select "Delete bucket" to clean up (removes all objects first)

## 🛠️ Technical Implementation

### **Architecture:**

- **Modular design** with separate functions for each operation
- **Type hints** throughout for code clarity and IDE support
- **Comprehensive error handling** with specific AWS exception handling
- **Logging** with timestamps and structured messages

### **AWS Integration:**

- **boto3 client** for efficient AWS API communication
- **Region-aware** bucket creation (us-east-2)
- **Proper IAM integration** using AWS credential files
- **S3 best practices** including object key naming conventions

### **Code Quality:**

- **Docstrings** for all functions with parameter descriptions
- **Input validation** for file types and paths
- **Resource cleanup** ensuring no orphaned AWS resources
- **User experience focus** with clear prompts and feedback

## 📊 Project Structure

```
aws-S3-script/
├── s3_operations.py    # Main application code
├── requirements.txt    # Python dependencies
├── aws.log            # Application logs (generated)
└── README.md          # This documentation
```

## 🔧 Dependencies

- **boto3**: AWS SDK for Python
- **questionary**: Interactive command-line prompts
- **botocore**: Low-level AWS client library
- Standard library: `logging`, `datetime`, `os`, `typing`

## 🚀 Future Enhancements

Potential expansions for continued learning:

- Integration with other AWS services (Lambda, CloudWatch)
- Batch operations for large-scale file management
- Configuration management for multiple AWS accounts
- Integration with Infrastructure as Code (Terraform)

## 📝 Lessons Learned

- **Practical experience** reinforces theoretical cloud concepts
- **Error handling** is crucial for production-ready AWS automation
- **User experience** matters even for internal tools
- **Documentation** and code organization enable maintainable solutions
- **AWS APIs** are powerful but require careful attention to parameter details

---

_Built as part of Elsevier Systems Engineering interview preparation - demonstrating cloud expertise and professional development practices._
