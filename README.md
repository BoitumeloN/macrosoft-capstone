# macrosoft-capstone
## View Storage Units
~/macrosoft-capstone/self-storage/storage_units$
export API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name self-storage-units --output text --query 'Stacks[0].Outputs[?OutputKey==`APIEndpoint`].OutputValue')
curl $API_ENDPOINT/storage_units