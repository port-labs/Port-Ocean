from typing import AsyncIterator, Optional
import aioboto3


class AwsCredentials:
    def __init__(self, account_id: str, access_key_id: str, secret_access_key: str, session_token: Optional[str] = None):
        self.account_id = account_id
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        self.enabled_regions = []
    
    async def updateEnabledRegions(self):
        session = aioboto3.Session(self.access_key_id, self.secret_access_key, self.session_token)
        async with session.client("account") as account_client:
            response = await account_client.list_regions(RegionOptStatusContains=['ENABLED', 'ENABLED_BY_DEFAULT'])
            regions = response.get("Regions", [])
            self.enabled_regions = [region["RegionName"] for region in regions]

    def isRole(self):
        return self.session_token is not None
    
    async def createSession(self, region: Optional[str] = None) -> aioboto3.Session:
        if self.isRole():
            return aioboto3.Session(self.access_key_id, self.secret_access_key, self.session_token, region)
        else:
            return aioboto3.Session(aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_access_key, region_name=region)
        
    async def createSessionForEachRegion(self) -> AsyncIterator[aioboto3.Session]:
        for region in self.enabled_regions:
            yield self.createSession(region)