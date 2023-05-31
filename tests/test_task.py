from starlette.testclient import TestClient

from main import app
from src.ds import TriggerStatus

client = TestClient(app)


class TestTask:
    
    def test_task_imagine(self):
        data = client.post('/v1/discord/imagine', json={"prompt": "test"}).json()
        trigger_id = data['trigger_id']
        assert data['trigger_result'] == TriggerStatus.success
        
        # todo: 这里要填 task_id 还是 trigger_id
        data = client.get(f'/v1/task/{trigger_id}')
