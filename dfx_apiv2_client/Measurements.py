import base64
from typing import Union

from dfx_apiv2_client import DfxApi


class Measurements(DfxApi):
    url_fragment = "measurements"
    @classmethod
    async def create(cls, session, study_id: str, resolution: int = 0, user_profile_id: str = ""):
        data = {
            "StudyID": study_id,
            "Resolution": resolution,
            "UserProfileId": user_profile_id,
        }
        url = f"{DfxApi.rest_url}/{cls.url_fragment}"
        async with session.post(url, json=data) as resp:
            body = await resp.json()
            if resp.status == 200:
                return body["ID"]

            raise ValueError((url, resp.status, body))

    @classmethod
    async def add_data(cls, session, measurement_id: str, chunk_order: Union[str, int], action: str, start_time: str,
                       end_time: str, metadata: Union[bytes, bytearray, memoryview,
                                                      str], payload: Union[bytes, bytearray, memoryview, str]):
        data = {
            "ChunkOrder": chunk_order,
            "Action": action,
            "StartTime": start_time,
            "EndTime": end_time,
            "Meta": str(metadata),
            "Payload": payload if type(payload) == str else base64.standard_b64encode(payload).decode('ascii')
        }
        url = f"{DfxApi.rest_url}/{cls.url_fragment}/{measurement_id}/data"
        async with session.post(url, json=data) as resp:
            body = await resp.json()
            if resp.status == 200:
                return body["ID"]

            raise ValueError((url, resp.status, body))

    @classmethod
    async def list(cls,
                   session,
                   date: str = "",
                   end_date: str = "",
                   user_profile_id: str = "",
                   user_profile_name: str = "",
                   study_id: str = "",
                   status_id: str = "",
                   limit: int = 50,
                   offset: int = 0):
        """[summary]

        Keyword Arguments:
            date {str} -- The date to return measurements for yyyy-mm-dd (default: {None})
            end_date {str} -- End date for range of measurements to receive (default: {None})
            user_profile_id {str} -- filter by a Profile ID (default: {None})
            user_profile_name {str} -- filter by a Profile Name (default: {None})
            study_id {str} -- filter by Study ID (default: {None})
            status_id {str} -- filter by measurement Status (default: {None})
            limit {int} -- Number of measurement records to return (default: {50})
            offset {int} -- Offset to specify the start of the count (default: {0})

        Returns:
            [type] -- [description]
        """
        params = {}
        if date:
            params["Date"] = date
        if end_date:
            params["EndDate"] = end_date
        if user_profile_id:
            params["UserProfileID"] = user_profile_id
        if user_profile_name:
            params["UserProfileName"] = user_profile_name
        if study_id:
            params["StudyID"] = study_id
        if status_id:
            params["StatusID"] = status_id
        if limit:
            params["Limit"] = limit
        if offset:
            params["Offset"] = offset

        url = f"{DfxApi.rest_url}/{cls.url_fragment}"
        async with session.get(url, params=params) as resp:
            body = await resp.json()
            if resp.status == 200:
                return body

            raise ValueError((url, resp.status, body))

    @classmethod
    async def retrieve(cls, session, measurement_id: str):
        url = f"{DfxApi.rest_url}/{cls.url_fragment}/{measurement_id}"
        async with session.get(url) as resp:
            body = await resp.json()
            if resp.status == 200:
                return body

            raise ValueError((url, resp.status, body))
