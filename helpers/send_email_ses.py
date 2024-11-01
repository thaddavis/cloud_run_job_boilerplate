import os
import boto3

def send_email_ses(to_emails: list[str], body: str):
  try:
    client = boto3.client(
      'ses',
      region_name=os.getenv("AWS_REGION"),
      aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
      aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )

    response = client.send_email(
      Source='noreply@kalygo.io',
      Destination={
        'ToAddresses': to_emails
      },
      Message={
        'Subject': {
          'Data': 'Weekly Update from the "A.I. Research Crew"'
        },
        'Body': {
          'Html': {
            'Data': f"{body}"
          }
        }
      }
    )
    print(response)
  except Exception as e:
    print(e)

