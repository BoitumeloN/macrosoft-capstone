# macrosoft-capstone
## View Storage Units
~/macrosoft-capstone/self-storage/storage_units$
export API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name self-storage-units --output text --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue')
curl $API_ENDPOINT/storage_units


#### ListUnits
curl $API_ENDPOINT/storage_units

#### List Units by availabilty
curl -X GET "$API_ENDPOINT/storage_units/status/Unavailable"

#### BookUnit 
curl -X PUT "$API_ENDPOINT/storage_units/3" -H "Content-Type: application/json" -d '{"unitid": "1"}'

#### Cancel Unit 
curl -X POST "$API_ENDPOINT/storage_units/2/cancel" -H "Content-Type: application/json" -d '{"unitid": "1"}'

#### Admin changes avaialability
curl -X PUT "$API_ENDPOINT/storage_units/1/status/Available" -H "Content-Type: application/json" -d '{"unitid": "1"}'


#### Admin changes avaialability -Unit 5
curl -X PUT "$API_ENDPOINT/storage_units/2/status/Available" -H "Content-Type: application/json" -d '{"unitid": "5"}'