# RedNoSQL Tool V1.0 - (https://github.com/redx-player/rednosql)

This tool was designed to find and detect nosql injection in any form
<br>by trying random payloads and comparing the results with default response length (This tool is in progress)

### How the tool works
* Get default response length
* Using rendom payloads with parameters
* Trying to bypass authentication by using {$ne, $gt, $regex, $lt, $nin}
* Tyring bruteforce blind nosqli

### Installation:
```
git clone https://github.com/redx-player/rednosql.git
cd rednosql
pip3 install -r requirments.txt
```
### Running:
```
python3 rednosql.py -u <url-without-prameter>  -m <post|get> -d <parameter spareterd with , and set FUZZ to check>
```
### Version
RedNoSQL Tool v1.0
