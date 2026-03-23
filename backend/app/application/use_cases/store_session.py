# application/use_cases/store_session.py

class StoreSessionUseCase:

    async def execute(self, user_id: str, message: str, response: str):
        # aquí luego conectarás con Firebase
        print(f"[LOG] {user_id}: {message} -> {response}")