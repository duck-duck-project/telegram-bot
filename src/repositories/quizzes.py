from enums import TruthOrDareQuestionType
from repositories import APIRepository

__all__ = ('QuizRepository',)


class QuizRepository(APIRepository):

    async def get_random_wish(self) -> str | None:
        response = await self._http_client.get('/quizzes/wishes/random/')

        if response.is_success:
            return response.json()['text']

        return None

    async def get_random_prediction(self) -> str | None:
        response = await self._http_client.get('/quizzes/predictions/random/')

        if response.is_success:
            return response.json()['text']

        return None

    async def get_random_truth_or_dare_question(
            self,
            *,
            question_type: TruthOrDareQuestionType | None = None,
    ) -> str | None:
        request_query_params = {}
        if question_type is not None:
            request_query_params['type'] = question_type

        response = await self._http_client.get(
            '/quizzes/truth-or-dare/random/',
            params=request_query_params,
        )

        if response.is_success:
            return response.json()['text']

        return None
