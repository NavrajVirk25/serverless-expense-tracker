import json
import boto3
import uuid
from datetime import datetime
import logging
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ExpenseTracker')

class DecimalEncoder(json.JSONEncoder):
    """Custom encoder to handle DynamoDB Decimal types for JSON serialization."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def lambda_handler(event, context):
    """
    Main Lambda handler for the Serverless Expense Tracker.
    Handles three operations:
    - POST /expenses       : Save a new expense to DynamoDB
    - GET  /expenses       : Retrieve all expenses from DynamoDB
    - GET  /expenses?summary=true : Return spending totals by category (analytics)
    """
    method = event.get('httpMethod', '')
    params = event.get('queryStringParameters') or {}

    # ── POST: Save a new expense ──────────────────────────────────────────────
    if method == 'POST':
        body = json.loads(event.get('body', '{}'))
        expense_name = body.get('name')
        amount = str(body.get('amount'))
        category = body.get('category')
        expense_id = str(uuid.uuid4())

        logger.info(f"Saving expense: {expense_name}, ${amount}, category={category}")

        table.put_item(Item={
            'expense_id': expense_id,
            'name': expense_name,
            'amount': amount,
            'category': category,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d')
        })

        logger.info("Expense saved successfully to DynamoDB")

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Expense saved!', 'id': expense_id})
        }

    # ── GET: Retrieve expenses or category summary ────────────────────────────
    elif method == 'GET':
        if params.get('summary') == 'true':
            # Analytics feature: total spending grouped by category
            logger.info("Fetching category summary")
            response = table.scan()
            items = response.get('Items', [])
            summary = {}
            for item in items:
                cat = item.get('category', 'Other')
                summary[cat] = round(summary.get(cat, 0) + float(item.get('amount', 0)), 2)
            logger.info(f"Category summary: {summary}")
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(summary)
            }
        else:
            # Return all expenses
            logger.info("Fetching all expenses")
            response = table.scan()
            items = response.get('Items', [])
            logger.info(f"Retrieved {len(items)} expenses from DynamoDB")
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(items, cls=DecimalEncoder)
            }
