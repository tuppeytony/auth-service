from uuid import uuid4


database_data = [
    {
        'email': 'lol@mail.ru',
        'password': '1234',
    },
    {
        'email': 'checkcheck@mail.ru',
        'password': 'abc!23',
    },
]

claims_data = [
    {
        'claim_name': 'test_claim',
        'claim_value': 'test_claim_value',
    },
    {
        'claim_name': 'test_claim2',
        'claim_value': 'test_claim_value2',
    },
    {
        'claim_name': 'test_claim2' * 3,
        'claim_value': 'test_claim_value2' * 3,
    },
    {
        'claim_name': 'test_claim2',
    },
    {
        'claim_value': 'test_claim_value2',
    },
    {
        'claim_name': 'test_claim3',
        'claim_value': 'test_claim_value3',
        'user_id': str(uuid4()),
    },
]
