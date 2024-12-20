from dotenv import load_dotenv
import pandas as pd
import boto3
import json
import sys
import os

load_dotenv()

scope = 'aws-controltower-ConfigAggregatorForOrganizations'

## Variáveis de ambientes diferente para essa etapa.

client = boto3.client('config',
                    verify=False,
                    aws_access_key_id=(os.environ["AWS_ACCESS_AWSCONFIG"]),
                    aws_secret_access_key=(os.environ["AWS_SECRET_AWSCONFIG"]),
                    region_name=(os.environ["REGION"])
                    )

query= """
SELECT 
    accountId, 
    resourceName,
    awsRegion, 
    configuration.databaseName, 
    configuration.endpoint.value, 
    configuration.port,
    configuration.engineVersion,
    tags
WHERE 
    resourceType = 'AWS::RDS::DBCluster'
"""


### Caso queria utilizar tratamento no campo tags
# def extract_key_value(tags):
#     sec_info = next((tag for tag in tags if tag['key']== 'OPS-DNS'), None)
#     if sec_info:
#         return pd.Series([sec_info['key'], sec_info['value']])
#     else:
#         return pd.Series(['OPS-DNS', 'EM IMPLANTACAO'])


def rds_list():
    response = client.select_aggregate_resource_config(
        ConfigurationAggregatorName=scope,
        Expression=query
    )


    # Alguns tratamentos para as consultas.
    results = [json.loads(result) for result in response['Results']]
    df = pd.DataFrame(results)
    configuration_df = df['configuration'].apply(pd.Series)

    if 'endpoint' in configuration_df.columns:
        endpoint_df = configuration_df['endpoint'].apply(pd.Series)
        configuration_df = pd.concat([configuration_df.drop(columns=['endpoint']), endpoint_df], axis=1)

    ##### Passo onde trás o ARN do banco, para versões anteriores ao 16, não fica configurado no próprio banco, trazendo valores N/A
    # if 'masterUserSecret' in configuration_df.columns:
    #     masterUserSecret_df = configuration_df['masterUserSecret'].apply(pd.Series)
    #     configuration_df = pd.concat([configuration_df.drop(columns=['masterUserSecret']), masterUserSecret_df], axis=1)

    
    # remoção da coluna configuration com o estado antigo pela nova.
    df_expanded = pd.concat([df.drop(columns=['configuration']), configuration_df], axis=1)

    #alteração de nome de coluna
    df_rename = df_expanded.rename(columns={'value':'endpoint'})
    df_rename = df_rename.rename(columns={'engineVersion':'version'})
    
    # df_rename[['keys', 'values']] = df_rename['tags'].apply(extract_key_value)
    df_rename['DNS'] = df_rename['resourceName']+ '.ipiranga.io'

    ###### alteração do DNS para atender o valor correto determinado no Route 53
    df_rename['DNS'] = df_rename['DNS'].replace(
        {
            'si-oraculo-aurps-dev.ipiranga.io': 'pc-oraculo-aurps-dev.ipiranga.io',
            'si-oraculo-aurps-hml.ipiranga.io': 'pc-oraculo-aurps-hml.ipiranga.io',
            'si-oraculo-aurps-prd.ipiranga.io': 'pc-oraculo-aurps-prd.ipiranga.io',
            'mk-consumidorfinal-aurps-devv.ipiranga.io': 'mk-consumidorfinal-aurps-dev.ipiranga.io'
        }
    )

    #### Remoção da coluna Tags
    # df_rename = df_rename.drop(columns=['tags'])

    # df_rename.to_csv('aws_config.csv', index=False)
    return df_rename

# def main():
#     args = sys.argv[1:]

#     if args and len(args) > 1:
#         print_usage()

#     if args:
#         query = args[0]
#     else:
#         query = sys.stdin.read().strip()

#     if not query:
#         print_usage()

# print(rds_list(query))

# if __name__ == "__main__":
#     main()
