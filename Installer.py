import os

package = "flask_caching"

try:
    __import__package
except:
    os.system("pip install "+ package)
    
print("done")