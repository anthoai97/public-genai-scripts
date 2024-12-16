import boto3
import pandas as pd

# Initialize AWS ACM client
acm_client = boto3.client('acm')

# Fetch list of certificates
def get_acm_certificates():
    paginator = acm_client.get_paginator('list_certificates')
    certs = []
    for page in paginator.paginate():
        certs.extend(page['CertificateSummaryList'])
    return certs

# Get detailed information for each certificate
def get_certificate_details(cert_arn):
    response = acm_client.describe_certificate(CertificateArn=cert_arn)
    return response['Certificate']

# Analyze ACM data
def analyze_acm_data():
    # Fetch all certificates
    certs = get_acm_certificates()
    
    # Create a DataFrame for summary data
    cert_df = pd.DataFrame(certs)
    
    # Fetch detailed data for analysis
    detailed_data = []
    for cert in certs:
        details = get_certificate_details(cert['CertificateArn'])
        detailed_data.append({
            "DomainName": details.get('DomainName'),
            "Status": details.get('Status'),
            "Type": details.get('Type'),
            "KeyAlgorithm": details.get('KeyAlgorithm'),
            "NotBefore": details.get('NotBefore'),
            "NotAfter": details.get('NotAfter'),
            "RenewalEligibility": details.get('RenewalEligibility'),
            "InUseBy": len(details.get('InUseBy', [])),  # Number of services using the certificate
            "AdditionalDomains": ", ".join(details.get('SubjectAlternativeNames', []))  # Additional domains
        })
    
    # Create a detailed DataFrame
    detailed_df = pd.DataFrame(detailed_data)
    
    # Analyze or visualize the data
    print("\nSummary:")
    print(detailed_df.describe())  # Basic stats
    
    print("\nCertificates Expiring Soon:")
    expiring_soon = detailed_df[detailed_df['NotAfter'] < pd.Timestamp.now() + pd.Timedelta(days=30)]
    print(expiring_soon)
    
    print("\nCertificates with Additional Domains:")
    print(detailed_df[['DomainName', 'AdditionalDomains']])
    
    # Save to CSV for further exploration
    detailed_df.to_csv("acm_analysis_with_additional_domains.csv", index=False)
    print("\nData saved to 'acm_analysis_with_additional_domains.csv'.")

# Execute the analysis
if __name__ == "__main__":
    analyze_acm_data()
