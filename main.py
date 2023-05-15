import os
import json
import boto3

def main():
    secrets_manager_client = boto3.client('secretsmanager')
    next_token = None

    while True:
        if next_token:
            response = secrets_manager_client.list_secrets(
                NextToken = next_token,
                SortOrder = 'asc'
            )
        else:
            response = secrets_manager_client.list_secrets(
                SortOrder = 'asc'
            )

        secret_list = response['SecretList']
        try:
            next_token = response['NextToken']
        except:
            next_token = None

        for sec in secret_list:
            try:
                secret_response = secrets_manager_client.get_secret_value(
                    SecretId = sec['ARN']
                )

                secret_str = secret_response['SecretString']

                if 'mysql' in secret_str:                    
                    print(sec['Name'] + ' -> ' + secret_str)

                # if '.rds.' in secret_str:
                #     host_start = secret_str.index('"host":"') + len('"host":"')
                #     host_end = secret_str.index('"', host_start)
                #     print(sec['Name'] + ' -> ' + secret_str[host_start:host_end])
            except:
                pass

        if not next_token:
            break

if __name__ == '__main__':
    main()