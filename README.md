# Serverless Cloud Expense Tracker

**INFO 4110 — Cloud Computing | KPU Spring 2026**  
Group Project — Option 2: Implementation

---

## Overview

A fully serverless web application that allows users to submit, store, and analyze personal expenses using AWS cloud services. Built entirely within the AWS Free Tier.

---

## Architecture

```
Browser (S3)  →  API Gateway  →  Lambda (Python)  →  DynamoDB
                                      ↓
                                 CloudWatch Logs
```

| AWS Service | Role |
|---|---|
| AWS Lambda | Runs Python backend — saves and retrieves expenses |
| Amazon API Gateway | HTTP entry point — routes POST and GET requests to Lambda |
| Amazon DynamoDB | NoSQL database — stores all expense records |
| Amazon S3 | Hosts the HTML/JS web form (static website hosting) |
| AWS IAM | Least-privilege role — grants Lambda access to DynamoDB and CloudWatch |
| Amazon CloudWatch | Logs every Lambda invocation for monitoring and debugging |

---

## Features

- **Submit Expense** — Enter name, amount, and category (Food / Transport / Shopping / Other)
- **View All Expenses** — Table view of all stored records with dates
- **Spending Summary** — Analytics dashboard showing total spend per category

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/prod/expenses` | Save a new expense |
| GET | `/prod/expenses` | Retrieve all expenses |
| GET | `/prod/expenses?summary=true` | Get category spending totals |

**Base URL:** `https://59xle3sk0j.execute-api.us-east-1.amazonaws.com`

---

## Repository Structure

```
serverless-expense-tracker/
├── lambda_function.py   # Python Lambda backend
├── index.html           # Frontend web form (hosted on S3)
├── iam-policy.json      # IAM policy for Lambda execution role
└── README.md            # This file
```

---

## AWS Configuration

| Resource | Name |
|---|---|
| Lambda Function | ExpenseTrackerFunction |
| DynamoDB Table | ExpenseTracker |
| API Gateway | ExpenseTrackerAPI |
| S3 Bucket | expense-tracker-form |
| IAM Role | ExpenseTrackerLambdaRole |
| Region | us-east-1 |

---

## Course Coverage

| Course Topic | Implementation |
|---|---|
| Serverless Computing (Lecture 2) | AWS Lambda — no servers to manage |
| Containerization (Lecture 3) | Compared and justified serverless over Docker |
| Cloud Data Storage (Lectures 4 & 5) | DynamoDB as primary data store |
| Data Analytics (Lectures 9 & 10) | Category spending summary feature |
| Cloud Security (Lectures 11 & 12) | IAM least-privilege role |

---

## Free Tier Usage

All services used are within AWS Free Tier limits. Expected usage is well below thresholds for Lambda invocations, DynamoDB read/write units, API Gateway calls, and S3 storage.
