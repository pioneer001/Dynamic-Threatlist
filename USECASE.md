🌐 Use Case: Low-Cost, Dynamic Threat Intelligence Integration
🧭 Overview

This solution demonstrates how Azure Functions and GitHub Actions can provide a cost-effective, scalable, and easily maintainable way to dynamically host and manage threat intelligence IP lists for integration into security platforms such as Cisco Secure Firewall Management Center (FMC), firewalls, or any system that can consume URL-based threat feeds.

By leveraging serverless infrastructure, there’s no need for expensive threat intel platforms or complex infrastructure to publish and maintain blocklists. Instead, security teams can easily update text files, push changes, and let automation handle the rest.

🏗️ Key Benefits

💰 Low cost — Uses serverless Azure Functions with minimal overhead

⚡ Real-time updates — Lists are instantly reflected after a commit

🧰 Easy integration — Compatible with FMC and other platforms supporting external threat feeds

🧑‍💻 Simple management — Add or modify IPs through GitHub

🔐 Secure — Built-in allowlisting and temporary runner IP access

🧰 How It Works

Security teams update .txt or .html threat lists in the repo.

GitHub Actions:

Regenerates MD5 hash files

Deploys lists to Azure Function App

Enforces IP allowlists

FMC or other platforms consume these lists via URL.

Optional MD5 verification ensures feed integrity.

sequenceDiagram
    participant Sec as Security Analyst
    participant GH as GitHub Actions
    participant AZ as Azure Function
    participant FMC as Cisco FMC

    Sec->>GH: Commit updated threat list
    GH->>AZ: Deploy & enforce allowlist
    FMC->>AZ: Pull updated list
    FMC->>FMC: Enforce block/SI policy

🌐 Example Threat List URLs
https://<functionapp>.azurewebsites.net/api/getThreatList?filename=threats.txt
https://<functionapp>.azurewebsites.net/api/getThreatList?filename=threats-md5.html

🔥 Cisco FMC Integration

Go to Objects → Object Management → External Block Lists

Add External Block List:

Name: IP-Threat-List

Type: IP

URL:

https://<functionapp>.azurewebsites.net/api/getThreatList?filename=threats.txt


Refresh Interval: 30 min

Add the object to a Security Intelligence (SI) or Block Policy.

FMC will automatically refresh and enforce updates.

flowchart LR
    T[threats.txt] --> H[Azure Function]
    H --> FMC[Cisco FMC External Block List]
    FMC --> P[Policy Enforcement: SI or Block Policy]

🧭 Integration with Other Platforms

Because the list is served over HTTPS, any platform capable of ingesting external feeds can use it:

NGFWs with external blocklist support

SOAR / SIEM platforms pulling feeds

Custom security enforcement scripts

🛡️ IP Allowlist Management

accessWhitelist.txt defines trusted IPs or networks allowed to access the feed.

GitHub Actions enforces IP rules during deployment.

GitHub runner IPs are temporarily added and removed afterward.

Example:

122.2.150.244.76 # Security Team
192.168.10.0/24 # HQ
103.0.112.65 # SOC

🧠 Why This Works
Traditional Hosting	This Solution
Dedicated servers or appliances	Serverless functions
Manual updates	Automated deployment
Costly to scale	Scales cheaply
Platform-specific	Works with any URL-based consumer

🚀 Future Enhancements

🔄 Automatic refresh from upstream feeds

🧰 Support for multiple formats (e.g., STIX/TAXII)

🛡️ Webhook alerts for changes

🧠 SIEM/SOAR integration for automation

✅ Result:
A lightweight, inexpensive, and secure method for dynamically distributing threat intelligence feeds to FMC or any compatible platform. This approach replaces costly infrastructure with simple automation and serverless hosting, while keeping security controls and integrity in place.