# Self-Storage Solution Project -MACROSOFT

Welcome to the **Self-Storage Solution for the Digital Age** project! This README outlines the project's specifications, architecture, technologies, and implementation requirements.

---

## Project Overview

This project aims to build a next-generation self-storage solution, offering:
- **Flexible Rentals**: From short-term to indefinite bookings.
- **Seamless Management**: Digital app-based operations.
- **Next-Gen Security**: Secure, app-controlled access.

---

## Features

### Convenient Self-Storage
- Explore available storage options via a web app.
- Facilities in multiple towns with units ranging from locker to single-garage sizes.
- Instant booking with flexible durations (minimum 1 day to indefinite).

### Payment and Billing
- **Billing Options**: Pre-pay or Recurring (monthly/yearly).
- **Payment Methods**: Card, EFT.
- **Discounts**: Facility-specific, seasonal, or marketing campaigns.
- Customers can manage their payment methods.

### Storage Security
- Unlock facilities and units via the app.
- Share unit access (permanent or time-bound).
- Notifications for unit access events.

### Rental Management
- Cancel rentals with minimum notice periods (based on duration/billing options).
- [Optional] Recurring invoices emailed to customers.

### Customer Support
- Support staff can manage storage units and statuses:
  - Available, Reserved, Cancelling, Problem, Unavailable.
- Update unit statuses (Available ↔ Unavailable).

---

## Our Mission

### Backend Implementation
- Design and implement the business logic using a **serverless architecture**.
- Provide a robust **API** for the app to manage self-storage units.
- Authenticate the API using **AWS Cognito**.

### API Development
- Fulfill requirements through well-defined API endpoints on **AWS API Gateway**.
- Use **AWS Lambda** for small, focused business logic handlers.

### Web App
- Build a simple web app to book and manage storage units.
- Host the web app as a static site on **AWS S3** and distribute via **Amazon CloudFront**.
- Use **AWS Amplify SDK** for Cognito-based authentication.

### Infrastructure as Code
- Deploy backend and frontend using **CloudFormation** and **SAM**.
- Included a deployment diagram showcasing architecture for API and web app.

### Features
- Implement a fake invoice service using **AWS SES**.
- Utilize **AWS SES** for notifications (keep SES in sandbox mode).

---

## Technologies

### AWS Services
- **API Gateway**: For API endpoints.
- **Cognito**: For authentication.
- **Lambda**: For business logic.
- **DynamoDB**: As a NoSQL database.
- **SQS & EventBridge**: For asynchronous communications.
- **SES**: For customer notifications.
- **S3 & CloudFront**: For web app hosting and distribution.

### Programming Languages
- **Python** for Lambda functions.
- **JavaScript** for web app development.

### Infrastructure Tools
- **CloudFormation**, **SAM** for IaC.

---

<!-- Run Units Tests -->
python -m pytest tests/unit -v


### Get URL:
export API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name self-storage-units --output text --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue')
curl $API_ENDPOINT/storage_units

#### ListUnits
curl $API_ENDPOINT/storage_units

#### List Units by availabilty
curl -X GET "$API_ENDPOINT/storage_units/status/Reserved"

#### BookUnit 
curl -X PUT "$API_ENDPOINT/storage_units/2" -H "Content-Type: application/json" -d '{"unitid": "1"}'

#### Cancel Unit 
curl -X POST "$API_ENDPOINT/storage_units/2/cancel" -H "Content-Type: application/json" -d '{"unitid": "1"}'

#### Admin changes avaialability
curl -X PUT "$API_ENDPOINT/storage_units/1/status/Available" -H "Content-Type: application/json" -d '{"unitid": "1"}'


#### Admin changes avaialability -Unit 5
curl -X PUT "$API_ENDPOINT/storage_units/2/status/Reserved" -H "Content-Type: application/json" -d '{"unitid": "5"}'


1. chmod +x cognito-auth.sh

2. source ./cognito-auth.sh

3. curl -X PUT "$API_ENDPOINT/storage_units/2" \
    -H "Authorization: Bearer $ID_TOKEN" \
    -H "Content-Type: application/json"